const mysql = require("mysql2/promise");
const fs = require("fs");
const path = require("path");

async function initDatabase() {
  const sqlFile = path.resolve(__dirname, "./sql/init.sql");
  const sql = fs.readFileSync(sqlFile, "utf8");

  const connection = await mysql.createConnection({
    host: "127.0.0.1",
    port: 3306,
    user: "root",
    password: ""
  });

  const statements = sql.split(";").filter(s => s.trim());
  
  for (const statement of statements) {
    if (statement.trim()) {
      try {
        await connection.execute(statement);
        console.log("✓", statement.substring(0, 50) + "...");
      } catch (e) {
        console.error("✗", statement.substring(0, 50) + "...", e.message);
      }
    }
  }

  await connection.end();
  console.log("\n数据库初始化完成！");
}

initDatabase().catch(e => {
  console.error("初始化失败:", e.message);
  process.exit(1);
});
