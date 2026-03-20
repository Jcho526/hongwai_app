const mysql = require("mysql2/promise");
const { db } = require("./config");

const pool = mysql.createPool(db);

async function query(sql, params = []) {
  const [rows] = await pool.execute(sql, params);
  return rows;
}

module.exports = {
  pool,
  query
};
