const express = require("express");
const cors = require("cors");
const path = require("path");
const { port } = require("./config");
const authRouter = require("./routes/auth");
const personsRouter = require("./routes/persons");
const systemRouter = require("./routes/system");

const app = express();

app.use(cors());
app.use(express.json());
app.use("/static", express.static(path.resolve(__dirname, "../../static")));

app.get("/api/health", (req, res) => {
  res.json({ code: 0, message: "ok", data: { status: "up" } });
});

app.use("/api/auth", authRouter);
app.use("/api/persons", personsRouter);
app.use("/api/system", systemRouter);

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ code: 500, message: "服务器内部错误", data: null });
});

app.listen(port, () => {
  console.log(`hongwai backend listening on http://localhost:${port}`);
});
