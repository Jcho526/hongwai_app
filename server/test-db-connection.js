const mysql = require("mysql2/promise");

async function testConnection() {
  console.log("测试MySQL连接...\n");

  const configs = [
    {
      name: "默认配置（密码: 111111）",
      host: "127.0.0.1",
      port: 3306,
      user: "root",
      password: "111111"
    },
    {
      name: "无密码配置",
      host: "127.0.0.1",
      port: 3306,
      user: "root",
      password: ""
    },
    {
      name: "localhost配置（密码: 111111）",
      host: "localhost",
      port: 3306,
      user: "root",
      password: "111111"
    },
    {
      name: "localhost配置（无密码）",
      host: "localhost",
      port: 3306,
      user: "root",
      password: ""
    }
  ];

  for (const config of configs) {
    try {
      console.log(`尝试: ${config.name}`);
      const connection = await mysql.createConnection({
        host: config.host,
        port: config.port,
        user: config.user,
        password: config.password,
        waitForConnections: true,
        enableKeepAlive: true,
        keepAliveInitialDelayMs: 0
      });

      const [result] = await connection.execute("SELECT 1");
      console.log("✓ 连接成功！");
      
      // 尝试显示现有数据库
      const [databases] = await connection.execute("SHOW DATABASES");
      console.log("  已有数据库:", databases.map(d => d.Database).join(", "));
      
      await connection.end();
      console.log("\n✓ 推荐使用这个配置！\n");
      
      // 保存成功的配置
      return config;
    } catch (e) {
      console.log(`✗ 失败: ${e.message}\n`);
    }
  }

  console.log("所有配置都失败了，请检查MySQL状态和用户设置。");
}

testConnection();
