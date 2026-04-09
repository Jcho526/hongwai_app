const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { query } = require("../db");
const { authRequired } = require("../middlewares/auth");
const { jwtSecret, jwtExpiresIn } = require("../config");

const router = express.Router();

async function getUserTableName() {
  try {
    await query("SELECT 1 FROM users LIMIT 1");
    return "users";
  } catch (e) {}

  try {
    await query("SELECT 1 FROM `user` LIMIT 1");
    return "user";
  } catch (e) {}

  // 两个表都不存在，尝试创建 users 表
  console.log("未找到用户表，正在创建...");
  try {
    await query(`CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(64) NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      nickname VARCHAR(64) DEFAULT '',
      status TINYINT NOT NULL DEFAULT 1 COMMENT '1=正常,0=禁用',
      created_at BIGINT NOT NULL,
      updated_at BIGINT NOT NULL,
      UNIQUE KEY uk_username (username)
    )`);
    console.log("users 表创建成功");
    return "users";
  } catch (createError) {
    console.error("创建 users 表失败:", createError.message);
    throw new Error("未找到 users/user 用户表，且无法创建");
  }
}

async function verifyPassword(inputPassword, storedValue) {
  const stored = String(storedValue || "");
  if (!stored) return false;

  // bcrypt hash
  if (stored.startsWith("$2a$") || stored.startsWith("$2b$") || stored.startsWith("$2y$")) {
    return bcrypt.compare(inputPassword, stored);
  }

  // 兼容手动插入明文密码
  return inputPassword === stored;
}

router.post("/register", async (req, res, next) => {
  try {
    const table = await getUserTableName();
    const username = String(req.body.username || "").trim();
    const password = String(req.body.password || "").trim();
    const nickname = String(req.body.nickname || username).trim();

    if (username.length < 3) {
      return res.status(400).json({ code: 400, message: "用户名至少3位", data: null });
    }
    if (password.length < 6) {
      return res.status(400).json({ code: 400, message: "密码至少6位", data: null });
    }

    const existing = await query(`SELECT id FROM ${table === "user" ? "`user`" : "users"} WHERE username = ? LIMIT 1`, [username]);
    if (existing.length > 0) {
      return res.status(409).json({ code: 409, message: "用户名已存在", data: null });
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const now = Date.now();

    let result;
    if (table === "users") {
      result = await query(
        "INSERT INTO users (username, password_hash, nickname, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        [username, passwordHash, nickname, now, now]
      );
    } else {
      // 兼容旧表结构（password 字段）
      result = await query(
        "INSERT INTO `user` (username, password, nickname, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        [username, passwordHash, nickname, now, now]
      );
    }

    return res.json({
      code: 0,
      message: "ok",
      data: {
        id: result.insertId,
        username,
        nickname
      }
    });
  } catch (e) {
    next(e);
  }
});

router.post("/login", async (req, res, next) => {
  try {
    const table = await getUserTableName();
    const username = String(req.body.username || "").trim();
    const password = String(req.body.password || "").trim();

    if (!username || !password) {
      return res.status(400).json({ code: 400, message: "账号或密码不能为空", data: null });
    }

    const tableName = table === "user" ? "`user`" : "users";
    const rows = await query(`SELECT * FROM ${tableName} WHERE username = ? LIMIT 1`, [username]);

    if (rows.length === 0) {
      return res.status(401).json({ code: 401, message: "账号或密码错误", data: null });
    }

    const user = rows[0];
    const status = Number(user.status == null ? 1 : user.status);
    if (status !== 1) {
      return res.status(403).json({ code: 403, message: "账号已被禁用", data: null });
    }

    const ok = await verifyPassword(password, user.password_hash || user.password);
    if (!ok) {
      return res.status(401).json({ code: 401, message: "账号或密码错误", data: null });
    }

    const token = jwt.sign(
      {
        uid: user.id,
        username: user.username
      },
      jwtSecret,
      { expiresIn: jwtExpiresIn }
    );

    return res.json({
      code: 0,
      message: "ok",
      data: {
        token,
        user: {
          id: user.id,
          username: user.username,
          nickname: user.nickname
        }
      }
    });
  } catch (e) {
    next(e);
  }
});

router.get("/me", authRequired, async (req, res, next) => {
  try {
    const table = await getUserTableName();
    const tableName = table === "user" ? "`user`" : "users";
    const rows = await query(`SELECT id, username, nickname, status FROM ${tableName} WHERE id = ? LIMIT 1`, [req.user.uid]);
    if (rows.length === 0) {
      return res.status(404).json({ code: 404, message: "用户不存在", data: null });
    }
    return res.json({ code: 0, message: "ok", data: rows[0] });
  } catch (e) {
    next(e);
  }
});

router.post("/logout", authRequired, async (req, res) => {
  return res.json({ code: 0, message: "ok", data: true });
});

router.post("/deactivate", authRequired, async (req, res, next) => {
  try {
    const table = await getUserTableName();
    const tableName = table === "user" ? "`user`" : "users";
    const uid = req.user.uid;
    const now = Date.now();
    await query(`UPDATE ${tableName} SET status = 0, updated_at = ? WHERE id = ?`, [now, uid]);
    return res.json({ code: 0, message: "ok", data: true });
  } catch (e) {
    next(e);
  }
});

// 初始化路由 - 创建默认管理员用户
router.post("/init", async (req, res, next) => {
  try {
    const table = await getUserTableName();
    const tableName = table === "user" ? "`user`" : "users";
    
    // 检查是否已有用户
    const existing = await query(`SELECT COUNT(*) as cnt FROM ${tableName}`);
    if (existing[0].cnt > 0) {
      return res.json({ code: 0, message: "系统已初始化，用户已存在", data: null });
    }

    // 创建默认管理员用户
    const defaultUsername = "admin";
    const defaultPassword = "123456";
    const passwordHash = await bcrypt.hash(defaultPassword, 10);
    const now = Date.now();

    let result;
    if (table === "users") {
      result = await query(
        "INSERT INTO users (username, password_hash, nickname, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        [defaultUsername, passwordHash, "管理员", now, now]
      );
    } else {
      result = await query(
        "INSERT INTO `user` (username, password, nickname, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        [defaultUsername, passwordHash, "管理员", now, now]
      );
    }

    console.log("✓ 默认管理员用户已创建");
    console.log("  用户名: admin");
    console.log("  密码: 123456");

    return res.json({
      code: 0,
      message: "初始化成功",
      data: {
        id: result.insertId,
        username: defaultUsername,
        nickname: "管理员",
        password: defaultPassword // 仅在初始化时返回
      }
    });
  } catch (e) {
    next(e);
  }
});

module.exports = router;
