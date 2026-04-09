const mysql = require("mysql2/promise");
const { db } = require("./config");

// 增加连接超时和重试配置
const poolConfig = {
  ...db,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelayMs: 0,
  charset: 'utf8mb4'
};

let pool;

async function initPool() {
  try {
    pool = mysql.createPool(poolConfig);
    
    // 测试连接
    const connection = await pool.getConnection();
    console.log("✓ 数据库连接成功");
    connection.release();
    
    return pool;
  } catch (error) {
    console.error("✗ 数据库连接失败:", error.message);
    console.error("  配置:", {
      host: db.host,
      port: db.port,
      user: db.user,
      database: db.database
    });
    
    // 重新尝试连接
    setTimeout(initPool, 5000);
  }
}

async function query(sql, params = []) {
  if (!pool) {
    pool = await initPool();
  }
  
  const [rows] = await pool.execute(sql, params);
  return rows;
}

module.exports = {
  pool,
  query,
  initPool
};
