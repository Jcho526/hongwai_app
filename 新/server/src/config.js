const path = require("path");
const dotenv = require("dotenv");

// 优先读取 server/.env，避免从项目根目录启动时拿不到数据库配置
const envPathCandidates = [
  path.resolve(__dirname, "../.env"),
  path.resolve(process.cwd(), ".env")
];

for (const p of envPathCandidates) {
  const loaded = dotenv.config({ path: p });
  if (!loaded.error) break;
}

module.exports = {
  port: Number(process.env.PORT || 3000),
  db: {
    host: process.env.DB_HOST || "127.0.0.1",
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD || "",
    database: process.env.DB_NAME || "hongwai",
    connectionLimit: 10
  },
  jwtSecret: process.env.JWT_SECRET || "please_change_this_secret",
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || "7d"
};
