const fs = require("node:fs");
const fsPromises = require("node:fs/promises");
const http = require("node:http");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const port = Number.parseInt(process.env.PORT || "4173", 10);

const mimeTypes = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".svg", "image/svg+xml"],
  [".ico", "image/x-icon"],
]);

function safeJoin(base, target) {
  const normalized = path.normalize(target).replace(/^([/\\])+/, "");
  const resolved = path.resolve(base, normalized);
  if (!resolved.startsWith(base)) {
    return null;
  }
  return resolved;
}

async function serveFile(filePath, res) {
  try {
    const stat = await fsPromises.stat(filePath);
    if (stat.isDirectory()) {
      return serveFile(path.join(filePath, "index.html"), res);
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes.get(ext) || "application/octet-stream";
    res.writeHead(200, {
      "Content-Type": contentType,
      "Content-Length": stat.size,
    });
    fs.createReadStream(filePath).pipe(res);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
  }
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", "http://localhost");
    const pathname = url.pathname === "/" ? "/index.html" : url.pathname;
    const filePath = safeJoin(root, pathname);
    if (!filePath) {
      res.writeHead(400, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Bad request");
      return;
    }
    await serveFile(filePath, res);
  } catch (error) {
    res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
    res.end(error?.message || "Internal server error");
  }
});

server.listen(port, () => {
  console.log(`R Systems site running at http://localhost:${port}`);
  console.log(`Serving: ${root}`);
});
