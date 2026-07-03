const fs = require("node:fs/promises");
const childProcess = require("node:child_process");
const path = require("node:path");
const readline = require("node:readline/promises");
const { stdin, stdout } = require("node:process");

const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");

async function prompt(message) {
  const rl = readline.createInterface({ input: stdin, output: stdout });
  try {
    return await rl.question(message);
  } finally {
    rl.close();
  }
}

async function readSession(sessionFile) {
  try {
    const raw = await fs.readFile(sessionFile);
    if (raw.length >= 16 && raw.subarray(0, 15).toString("utf8") === "SQLite format 3") {
      return readSqliteSession(sessionFile);
    }
    return raw.toString("utf8").trim();
  } catch (error) {
    if (error && error.code === "ENOENT") {
      return "";
    }
    throw error;
  }
}

function readSqliteSession(sessionFile) {
  const python = process.env.PYTHON || "python";
  const script = String.raw`
import base64
import json
import sqlite3
import sys

db_path = sys.argv[1]
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
row = conn.execute(
    "SELECT dc_id, server_address, port, auth_key, takeout_id FROM sessions ORDER BY dc_id DESC LIMIT 1"
).fetchone()
if row is None:
    raise SystemExit(2)
auth_key = row["auth_key"]
if isinstance(auth_key, memoryview):
    auth_key = auth_key.tobytes()
elif not isinstance(auth_key, (bytes, bytearray)):
    auth_key = bytes(auth_key)
payload = {
    "dc_id": row["dc_id"],
    "server_address": row["server_address"],
    "port": row["port"],
    "auth_key_b64": base64.b64encode(auth_key).decode("ascii"),
}
sys.stdout.write(json.dumps(payload))
`;

  const stdoutText = childProcess.execFileSync(python, ["-c", script, sessionFile], {
    encoding: "utf8",
  });
  const payload = JSON.parse(stdoutText);
  const dcId = Number.parseInt(String(payload.dc_id), 10);
  const serverAddress = String(payload.server_address || "");
  const port = Number.parseInt(String(payload.port), 10);
  const authKey = Buffer.from(String(payload.auth_key_b64 || ""), "base64");

  if (!Number.isInteger(dcId) || !serverAddress || !Number.isInteger(port) || authKey.length === 0) {
    throw new Error(`Invalid SQLite session payload in ${sessionFile}`);
  }

  const dcBuffer = Buffer.from([dcId]);
  const addressBuffer = Buffer.from(serverAddress);
  const addressLengthBuffer = Buffer.alloc(2);
  addressLengthBuffer.writeInt16BE(addressBuffer.length, 0);
  const portBuffer = Buffer.alloc(2);
  portBuffer.writeInt16BE(port, 0);

  return `1${Buffer.concat([
    dcBuffer,
    addressLengthBuffer,
    addressBuffer,
    portBuffer,
    authKey,
  ]).toString("base64")}`;
}

async function writeSession(sessionFile, sessionString) {
  await fs.mkdir(path.dirname(sessionFile), { recursive: true });
  await fs.writeFile(sessionFile, sessionString, "utf8");
}

async function readUtf8TextFile(filePath) {
  const contents = await fs.readFile(filePath, "utf8");
  return contents.replace(/^\uFEFF/, "");
}

async function createClient({ apiId, apiHash, sessionFile }) {
  const sessionString = await readSession(sessionFile);
  const client = new TelegramClient(new StringSession(sessionString), apiId, apiHash, {
    connectionRetries: 5,
  });
  return client;
}

async function login({ apiId, apiHash, sessionFile }) {
  const client = await createClient({ apiId, apiHash, sessionFile });
  await client.start({
    phoneNumber: async () => prompt("Номер телефона: "),
    password: async () => prompt("Пароль 2FA: "),
    phoneCode: async () => prompt("Код из Telegram: "),
    onError: (error) => {
      console.error("Ошибка авторизации:", error);
    },
  });

  await writeSession(sessionFile, client.session.save());
  return client;
}

async function connect({ apiId, apiHash, sessionFile }) {
  const client = await createClient({ apiId, apiHash, sessionFile });
  await client.connect();
  if (!(await client.checkAuthorization())) {
    throw new Error("Session is not authorized. Run `npm run login` first.");
  }

  return client;
}

async function ensureClient(config) {
  const sessionString = await readSession(config.sessionFile);
  if (!sessionString) {
    return login(config);
  }

  return connect(config);
}

async function showWhoAmI(client) {
  const me = await client.getMe();
  console.log("Аккаунт:");
  console.log(`  id: ${me.id}`);
  console.log(`  username: ${me.username || "-"}`);
  console.log(`  name: ${[me.firstName, me.lastName].filter(Boolean).join(" ") || "-"}`);
  console.log(`  phone: ${me.phone || "-"}`);
}

async function listDialogs(client, limit = 10) {
  const dialogs = await client.getDialogs({ limit });
  for (const dialog of dialogs) {
    console.log(`${dialog.id}\t${dialog.title}`);
  }
}

async function sendMessage(client, peer, message) {
  await client.sendMessage(peer, { message });
}

async function sendMessageFromFile(client, peer, filePath) {
  const message = await readUtf8TextFile(filePath);
  return sendMessage(client, peer, message);
}

async function readPeerList(filePath) {
  const contents = await readUtf8TextFile(filePath);
  return contents
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"));
}

async function broadcastMessages(client, peers, message, options = {}) {
  const delayMs = Number.isFinite(options.delayMs) && options.delayMs > 0 ? options.delayMs : 0;
  const dryRun = options.dryRun !== false;
  const results = [];

  for (let index = 0; index < peers.length; index += 1) {
    const peer = peers[index];

    if (dryRun) {
      console.log(`[dry-run] ${peer}`);
      results.push({ peer, status: "dry-run" });
    } else {
      try {
        const sent = await client.sendMessage(peer, { message });
        console.log(`Sent to ${peer}: ${sent.id}`);
        results.push({ peer, status: "sent", id: sent.id });
      } catch (error) {
        console.error(`Failed to send to ${peer}:`, error.message || error);
        results.push({ peer, status: "error", error: error.message || String(error) });
      }
    }

    if (delayMs > 0 && index < peers.length - 1) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  return results;
}

function sanitizeFileName(name) {
  return String(name || "chat")
    .replace(/[<>:"/\\|?*\u0000-\u001f]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\.+$/g, "")
    .slice(0, 120) || "chat";
}

function formatMessageLine(message) {
  const direction = message.out ? "out" : "in";
  const text = (message.message || "").trim();
  const date = message.date ? new Date(message.date).toISOString() : "-";
  return `[${direction}] ${date} #${message.id}: ${text || "<non-text message>"}`;
}

async function getRecentMessages(client, peer, limit = 10) {
  const messages = await client.getMessages(peer, { limit });
  return Array.isArray(messages) ? messages : Array.from(messages || []);
}

function messageToRecord(message) {
  const mediaType = message.media ? (message.media.className || message.media.constructor?.name || "media") : "";
  return {
    id: message.id,
    date: message.date ? new Date(message.date).toISOString() : null,
    out: Boolean(message.out),
    senderId: message.senderId ? String(message.senderId) : "",
    message: (message.message || "").trim(),
    mediaType,
    hasMedia: Boolean(message.media),
    replyTo: message.replyTo ? String(message.replyTo.replyToMsgId || "") : "",
  };
}

async function exportDialogArchive(client, options = {}) {
  const limit = Number.isFinite(options.limit) && options.limit > 0 ? options.limit : 200;
  const messageLimit = Number.isFinite(options.messageLimit) && options.messageLimit > 0 ? options.messageLimit : 250;
  const scope = (options.scope || "private").toString();
  const outputDir = options.outputDir || path.resolve(process.cwd(), "outputs", "telegram_archive");
  const dialogs = await client.getDialogs({ limit });
  await fs.mkdir(outputDir, { recursive: true });

  const index = [];
  for (const dialog of dialogs) {
    const entityType = dialog.entity?.className || dialog.entity?.constructor?.name || "";
    const isPrivate = entityType === "User" || Boolean(dialog.isUser);
    if (scope === "private" && !isPrivate) {
      continue;
    }
    if (scope === "group" && isPrivate) {
      continue;
    }

    const title = dialog.title || `dialog_${dialog.id}`;
    const safeTitle = sanitizeFileName(title);
    const folder = path.join(outputDir, `${safeTitle}__${String(dialog.id).replace(/[^0-9a-zA-Z_-]/g, "_")}`);
    await fs.mkdir(folder, { recursive: true });

    const fetched = await client.getMessages(dialog.entity, { limit: messageLimit });
    const rawMessages = Array.isArray(fetched) ? fetched : Array.from(fetched || []);
    const messages = rawMessages.reverse().map(messageToRecord);

    const textLines = [];
    for (const item of messages) {
      const prefix = item.out ? "OUT" : "IN";
      const body = item.message || (item.hasMedia ? `<${item.mediaType || "media"}>` : "<non-text message>");
      textLines.push(`${item.date || "-"} [${prefix}] #${item.id}: ${body}`);
    }

    await fs.writeFile(path.join(folder, "meta.json"), JSON.stringify({
      id: dialog.id,
      title,
      folder,
      messageCount: messages.length,
    }, null, 2), "utf8");
    await fs.writeFile(path.join(folder, "messages.json"), JSON.stringify(messages, null, 2), "utf8");
    await fs.writeFile(path.join(folder, "messages.txt"), textLines.join("\n"), "utf8");

    index.push({
      id: dialog.id,
      title,
      scope: entityType || "unknown",
      folder: path.relative(process.cwd(), folder),
      messageCount: messages.length,
    });

    console.log(`${title}\t${messages.length}\t${folder}`);
  }

  await fs.writeFile(path.join(outputDir, "_index.json"), JSON.stringify(index, null, 2), "utf8");
  return index;
}

async function sendMessageAndWaitForReply(client, peer, message, options = {}) {
  const {
    limit = 10,
    timeoutMs = 15000,
    pollIntervalMs = 1000,
  } = options;

  const sent = await client.sendMessage(peer, { message });
  const deadline = Date.now() + timeoutMs;
  let lastSeenId = sent.id || 0;

  while (Date.now() < deadline) {
    const recent = await getRecentMessages(client, peer, limit);
    const incoming = recent
      .filter((item) => item && !item.out && typeof item.id === "number" && item.id > lastSeenId)
      .sort((a, b) => a.id - b.id);

    if (incoming.length > 0) {
      return {
        sent,
        replies: incoming,
      };
    }

    await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
  }

  return {
    sent,
    replies: [],
  };
}

async function runInteractiveShell(client) {
  console.log("Локальный агент готов.");
  console.log("Команды: whoami, dialogs [n], send <peer> <text>, exit");

  const rl = readline.createInterface({ input: stdin, output: stdout, prompt: "> " });
  rl.prompt();

  rl.on("line", async (line) => {
    const trimmed = line.trim();

    try {
      if (!trimmed || trimmed === "help") {
        console.log("whoami | dialogs [n] | send <peer> <text> | exit");
      } else if (trimmed === "exit" || trimmed === "quit") {
        rl.close();
        return;
      } else if (trimmed === "whoami") {
        await showWhoAmI(client);
      } else if (trimmed.startsWith("dialogs")) {
        const [, rawLimit] = trimmed.split(/\s+/, 2);
        const limit = Number.parseInt(rawLimit || "10", 10);
        await listDialogs(client, Number.isFinite(limit) && limit > 0 ? limit : 10);
      } else if (trimmed.startsWith("send ")) {
        const match = trimmed.match(/^send\s+(\S+)\s+([\s\S]+)$/);
        if (!match) {
          console.log("Формат: send <peer> <text>");
        } else {
          const [, peer, text] = match;
          await sendMessage(client, peer, text);
          console.log("Сообщение отправлено.");
        }
      } else {
        console.log("Неизвестная команда. Напишите help.");
      }
    } catch (error) {
      console.error("Ошибка:", error.message || error);
    } finally {
      if (!rl.closed) {
        rl.prompt();
      }
    }
  });

  await new Promise((resolve) => {
    rl.on("close", resolve);
  });
}

module.exports = {
  connect,
  formatMessageLine,
  ensureClient,
  getRecentMessages,
  listDialogs,
  exportDialogArchive,
  login,
  readPeerList,
  readUtf8TextFile,
  runInteractiveShell,
  sendMessage,
  sendMessageFromFile,
  broadcastMessages,
  sendMessageAndWaitForReply,
  showWhoAmI,
};
