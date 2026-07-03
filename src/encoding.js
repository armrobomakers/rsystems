const childProcess = require("node:child_process");

function ensureUtf8Console() {
  if (process.platform !== "win32") {
    return;
  }

  try {
    childProcess.execSync("chcp 65001 >NUL", { stdio: "ignore" });
  } catch {
    // Best effort only. If the console cannot switch code page, keep going.
  }

  if (typeof process.stdin.setEncoding === "function") {
    process.stdin.setEncoding("utf8");
  }

  if (typeof process.stdout.setDefaultEncoding === "function") {
    process.stdout.setDefaultEncoding("utf8");
  }

  if (typeof process.stderr.setDefaultEncoding === "function") {
    process.stderr.setDefaultEncoding("utf8");
  }
}

module.exports = {
  ensureUtf8Console,
};
