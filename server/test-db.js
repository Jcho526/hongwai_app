const mysql = require("mysql2/promise");

async function testConnection() {
  try {
    console.log("尝试连接到MySQL...");
    const connection = await mysql.createConnection({
      host: "127.0.0.1",
      port: 3306,
      user: "root",
      waitForConnections: true,
      connectionLimit: 1,
      queueLimit: 0
    });
    
    const [rows] = await connection.execute("SELECT 1");
    console.log("连接成功！");
    console.log(rows);
    
    await connection.end();
  } catch (e) {
    console.error("连接失败:", e.code, e.message);
  }
}

testConnection();
