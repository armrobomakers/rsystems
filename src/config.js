const fs = require("node:fs");
const path = require("node:path");
require("dotenv").config();

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function parseApiId(value) {
  const apiId = Number.parseInt(value, 10);
  if (!Number.isInteger(apiId) || apiId <= 0) {
    throw new Error("TG_API_ID must be a positive integer");
  }
  return apiId;
}

function resolveProjectPath(inputPath) {
  return path.isAbsolute(inputPath) ? inputPath : path.resolve(process.cwd(), inputPath);
}

function loadConfig() {
  const apiId = parseApiId(requireEnv("TG_API_ID"));
  const apiHash = requireEnv("TG_API_HASH").trim();
  const sessionFile = resolveProjectPath(process.env.TG_SESSION_FILE || ".data/telegram.session");
  const targetBotUsername = (process.env.TG_TARGET_BOT_USERNAME || "ARM_PAMM_bot").trim();
  const sessionDir = path.dirname(sessionFile);

  if (!fs.existsSync(sessionDir)) {
    fs.mkdirSync(sessionDir, { recursive: true });
  }

  return {
    apiId,
    apiHash,
    sessionFile,
    targetBotUsername,
  };
}

module.exports = {
  loadConfig,
};
