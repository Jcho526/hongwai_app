const jwt = require("jsonwebtoken");
const { jwtSecret } = require("../config");

function authRequired(req, res, next) {
  const authHeader = req.headers.authorization || "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : "";

  if (!token) {
    return res.status(401).json({ code: 401, message: "未登录或登录已过期", data: null });
  }

  try {
    const payload = jwt.verify(token, jwtSecret);
    req.user = payload;
    next();
  } catch (e) {
    return res.status(401).json({ code: 401, message: "登录令牌无效", data: null });
  }
}

module.exports = {
  authRequired
};
