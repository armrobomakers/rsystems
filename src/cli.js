#!/usr/bin/env node

const { ensureUtf8Console } = require("./encoding");
ensureUtf8Console();

const { loadConfig } = require("./config");
const {
  broadcastMessages,
  ensureClient,
  exportDialogArchive,
  formatMessageLine,
  listDialogs,
  getRecentMessages,
  login,
  readPeerList,
  readUtf8TextFile,
  runInteractiveShell,
  sendMessage,
  sendMessageFromFile,
  sendMessageAndWaitForReply,
  showWhoAmI,
} = require("./telegram");

function parseArgs(args) {
  const options = { _: [] };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];

    if (arg === "--apply") {
      options.apply = true;
    } else if (arg === "--dry-run") {
      options.apply = false;
    } else if (arg === "--file" || arg === "-f") {
      options.file = args[++index];
    } else if (arg.startsWith("--file=")) {
      options.file = arg.slice("--file=".length);
    } else if (arg.startsWith("file=")) {
      options.file = arg.slice("file=".length);
    } else if (arg === "--peers") {
      options.peers = args[++index];
    } else if (arg.startsWith("--peers=")) {
      options.peers = arg.slice("--peers=".length);
    } else if (arg.startsWith("peers=")) {
      options.peers = arg.slice("peers=".length);
    } else if (arg === "--delay-ms") {
      options.delayMs = Number.parseInt(args[++index] || "", 10);
    } else if (arg.startsWith("--delay-ms=")) {
      options.delayMs = Number.parseInt(arg.slice("--delay-ms=".length), 10);
    } else {
      options._.push(arg);
    }
  }

  return options;
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  const config = loadConfig();

  switch (command) {
    case "login": {
      const client = await login(config);
      await showWhoAmI(client);
      await client.disconnect();
      break;
    }

    case "whoami": {
      const client = await ensureClient(config);
      await showWhoAmI(client);
      await client.disconnect();
      break;
    }

    case "dialogs": {
      const client = await ensureClient(config);
      const limit = Number.parseInt(args[0] || "10", 10);
      await listDialogs(client, Number.isFinite(limit) && limit > 0 ? limit : 10);
      await client.disconnect();
      break;
    }

    case "archive": {
      const client = await ensureClient(config);
      const limit = Number.parseInt(args[0] || "200", 10);
      const messageLimit = Number.parseInt(args[1] || "250", 10);
      const scope = (args[2] || "private").toLowerCase();
      const outputDir = args[3];
      const archiveLimit = Number.isFinite(limit) && limit > 0 ? limit : 200;
      await exportDialogArchive(client, {
        limit: archiveLimit,
        messageLimit: Number.isFinite(messageLimit) && messageLimit > 0 ? messageLimit : 250,
        scope,
        outputDir,
      });
      await client.disconnect();
      break;
    }

    case "send": {
      const client = await ensureClient(config);
      const options = parseArgs(args);
      const [peer, ...messageParts] = options._;
      if (!peer) {
        throw new Error("Usage: npm run send -- <peer> <message> | npm run send -- <peer> file=message.txt");
      }

      if (options.file) {
        await sendMessageFromFile(client, peer, options.file);
      } else if (messageParts.length > 0 && messageParts[0].startsWith("file=")) {
        await sendMessageFromFile(client, peer, messageParts[0].slice("file=".length));
      } else if (messageParts.length > 0) {
        await sendMessage(client, peer, messageParts.join(" "));
      } else {
        throw new Error("Usage: npm run send -- <peer> <message> | npm run send -- <peer> file=message.txt");
      }
      await client.disconnect();
      break;
    }

    case "broadcast": {
      const client = await ensureClient(config);
      const options = parseArgs(args);
      let peersFile = options.peers;
      let messageSource = options.file;
      const positional = options._;
      let apply = Boolean(options.apply);
      let delayMs = Number.isFinite(options.delayMs) ? options.delayMs : 1500;

      if (!peersFile && positional.length > 0) {
        peersFile = positional[0];
      }
      if (!messageSource && positional.length > 1) {
        messageSource = positional[1].startsWith("@") ? positional[1].slice(1) : positional[1];
      }
      if (!apply) {
        apply = positional.slice(2).some((token) => token === "apply");
      }

      if (!peersFile || !messageSource) {
        throw new Error("Usage: npm run broadcast -- peers=peers.txt file=message.txt [apply]");
      }

      const peers = await readPeerList(peersFile);
      const message = await readUtf8TextFile(messageSource);
      if (!apply) {
        console.log(`[dry-run] message bytes: ${Buffer.byteLength(message, "utf8")}`);
        console.log(`[dry-run] recipients: ${peers.length}`);
        for (const peer of peers) {
          console.log(`  ${peer}`);
        }
      } else {
        await broadcastMessages(client, peers, message, {
          dryRun: false,
          delayMs,
        });
      }
      await client.disconnect();
      break;
    }

    case "bottest": {
      const client = await ensureClient(config);
      if (args.length === 0) {
        throw new Error("Usage: npm run bottest -- [/bot_username] <message>");
      }

      const targetPeer =
        args.length > 1 && !args[0].startsWith("/")
          ? args[0]
          : config.targetBotUsername;
      const messageParts = targetPeer === args[0] ? args.slice(1) : args;
      if (messageParts.length === 0) {
        throw new Error("Usage: npm run bottest -- [/bot_username] <message>");
      }

      const message = messageParts.join(" ");
      const result = await sendMessageAndWaitForReply(client, targetPeer, message, {
        timeoutMs: 20000,
        pollIntervalMs: 1000,
        limit: 10,
      });

      console.log(`Sent to ${targetPeer}: ${message}`);
      console.log(formatMessageLine(result.sent));
      if (result.replies.length === 0) {
        console.log("No reply received within timeout.");
      } else {
        console.log("Replies:");
        for (const reply of result.replies) {
          console.log(`  ${formatMessageLine(reply)}`);
        }
      }
      await client.disconnect();
      break;
    }

    case "botlog": {
      const client = await ensureClient(config);
      const peer = args[0] || config.targetBotUsername;
      const limit = Number.parseInt(args[1] || "10", 10);
      const messages = await getRecentMessages(
        client,
        peer,
        Number.isFinite(limit) && limit > 0 ? limit : 10,
      );
      console.log(`Recent messages with ${peer}:`);
      for (const message of messages) {
        console.log(formatMessageLine(message));
      }
      await client.disconnect();
      break;
    }

    case "agent": {
      const client = await ensureClient(config);
      await runInteractiveShell(client);
      await client.disconnect();
      break;
    }

    default:
      console.log("Команды:");
      console.log("  npm run login");
      console.log("  npm run whoami");
      console.log("  npm run dialogs -- 10");
      console.log("  npm run archive -- 200 250 private");
      console.log("  npm run send -- me \"hello\"");
      console.log("  npm run send -- me file=.tmp/message.txt");
      console.log("  npm run broadcast -- peers=.tmp/peers.txt file=.tmp/message.txt");
      console.log("  npm run broadcast -- peers=.tmp/peers.txt file=.tmp/message.txt apply");
      console.log("  npm run bottest -- /start");
      console.log("  npm run bottest -- ARM_PAMM_bot \"/start\"");
      console.log("  npm run botlog -- ARM_PAMM_bot 10");
      console.log("  npm run agent");
  }
}

main().catch((error) => {
  console.error(error.message || error);
  process.exitCode = 1;
});
