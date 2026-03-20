const express = require("express");
const { query } = require("../db");
const { authRequired } = require("../middlewares/auth");

const router = express.Router();

router.use(authRequired);

router.get("/", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const page = Math.max(1, Number(req.query.page || 1));
    const pageSize = Math.max(1, Number(req.query.pageSize || 20));
    const offset = (page - 1) * pageSize;
    const keyword = String(req.query.keyword || "").trim();
    const searchType = String(req.query.searchType || "name");

    const where = ["user_id = ?"];
    const params = [uid];

    if (keyword) {
      if (searchType === "phone") {
        where.push("(phone1 LIKE ? OR phone2 LIKE ? OR phone3 LIKE ? OR relative_phone LIKE ?)");
        const likeKw = `%${keyword}%`;
        params.push(likeKw, likeKw, likeKw, likeKw);
      } else {
        where.push("name LIKE ?");
        params.push(`%${keyword}%`);
      }
    }

    const whereSql = where.length ? `WHERE ${where.join(" AND ")}` : "";

    const totalRows = await query(`SELECT COUNT(*) AS total FROM persons ${whereSql}`, params);
    const total = Number(totalRows[0]?.total || 0);

    // 某些 MySQL 版本/驱动组合下，LIMIT ?, ? 预编译参数会触发 ER_WRONG_ARGUMENTS
    // 这里将已校验的数字直接拼接到 SQL，避免新增后列表查询 500。
    const rows = await query(
      `SELECT id, name, gender, age, phone1, phone2, phone3, relative_phone, id_card, created_at, updated_at
       FROM persons
       ${whereSql}
       ORDER BY created_at DESC
       LIMIT ${offset}, ${pageSize}`,
      params
    );

    const list = rows.map((r) => ({
      id: String(r.id),
      name: r.name,
      gender: r.gender,
      age: Number(r.age || 0),
      phone1: r.phone1 || "",
      phone2: r.phone2 || "",
      phone3: r.phone3 || "",
      relativePhone: r.relative_phone || "",
      idCard: r.id_card || "",
      createdAt: Number(r.created_at || 0),
      updatedAt: Number(r.updated_at || 0)
    }));

    return res.json({
      code: 0,
      message: "ok",
      data: {
        list,
        total,
        page,
        pageSize
      }
    });
  } catch (e) {
    next(e);
  }
});

router.post("/", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const name = String(req.body.name || "").trim();
    const gender = String(req.body.gender || "男").trim() || "男";
    const age = Number(req.body.age || 0);
    const phone1 = String(req.body.phone1 || "").trim();
    const phone2 = String(req.body.phone2 || "").trim();
    const phone3 = String(req.body.phone3 || "").trim();
    const relativePhone = String(req.body.relativePhone || "").trim();
    const idCard = String(req.body.idCard || "").trim();

    if (!name) {
      return res.status(400).json({ code: 400, message: "姓名不能为空", data: null });
    }

    const now = Date.now();

    const result = await query(
      `INSERT INTO persons (user_id, name, gender, age, phone1, phone2, phone3, relative_phone, id_card, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [uid, name, gender, age, phone1, phone2, phone3, relativePhone, idCard, now, now]
    );

    return res.json({
      code: 0,
      message: "ok",
      data: {
        id: String(result.insertId),
        name,
        gender,
        age,
        phone1,
        phone2,
        phone3,
        relativePhone,
        idCard,
        createdAt: now,
        updatedAt: now
      }
    });
  } catch (e) {
    next(e);
  }
});

router.put("/:id", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const id = Number(req.params.id);
    const name = String(req.body.name || "").trim();
    const gender = String(req.body.gender || "男").trim() || "男";
    const age = Number(req.body.age || 0);
    const phone1 = String(req.body.phone1 || "").trim();
    const phone2 = String(req.body.phone2 || "").trim();
    const phone3 = String(req.body.phone3 || "").trim();
    const relativePhone = String(req.body.relativePhone || "").trim();
    const idCard = String(req.body.idCard || "").trim();
    const now = Date.now();

    if (!id) {
      return res.status(400).json({ code: 400, message: "无效id", data: null });
    }
    if (!name) {
      return res.status(400).json({ code: 400, message: "姓名不能为空", data: null });
    }

    const result = await query(
      `UPDATE persons
       SET name = ?, gender = ?, age = ?, phone1 = ?, phone2 = ?, phone3 = ?, relative_phone = ?, id_card = ?, updated_at = ?
       WHERE id = ? AND user_id = ?`,
      [name, gender, age, phone1, phone2, phone3, relativePhone, idCard, now, id, uid]
    );

    if (!result.affectedRows) {
      return res.status(404).json({ code: 404, message: "人员不存在", data: null });
    }

    return res.json({
      code: 0,
      message: "ok",
      data: {
        id: String(id),
        name,
        gender,
        age,
        phone1,
        phone2,
        phone3,
        relativePhone,
        idCard,
        updatedAt: now
      }
    });
  } catch (e) {
    next(e);
  }
});

router.delete("/:id", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const id = Number(req.params.id);

    if (!id) {
      return res.status(400).json({ code: 400, message: "无效id", data: null });
    }

    const result = await query("DELETE FROM persons WHERE id = ? AND user_id = ?", [id, uid]);
    if (!result.affectedRows) {
      return res.status(404).json({ code: 404, message: "人员不存在", data: null });
    }

    return res.json({ code: 0, message: "ok", data: true });
  } catch (e) {
    next(e);
  }
});

module.exports = router;
