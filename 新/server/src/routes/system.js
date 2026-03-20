const express = require("express");
const { query } = require("../db");
const { authRequired } = require("../middlewares/auth");

const router = express.Router();

const defaultSettings = {
  serialNo: "1009Z0YGVM28",
  deviceModel: "IR-TD-206",
  version: "v1.0.74",
  reportType: "无",
  expireTime: "无",
  reportTotal: 0,
  reportXiYi: 0,
  reportZhongYi: 0,
  reportMianZhen: 0,
  reportDanXiang: 0,
  imageSavePath: "qa/qa_thermal",
  reversePortraitImage: 0,
  reportCountHint: 20,
  reportDayHint: 10,
  screenCaptureEnable: 0,
  typecCameraEnable: 0,
  qrCodeUrl: ""
};

router.use(authRequired);

router.get("/settings", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const rows = await query("SELECT * FROM system_settings WHERE user_id = ? LIMIT 1", [uid]);

    if (!rows.length) {
      return res.json({
        code: 0,
        message: "ok",
        data: defaultSettings
      });
    }

    const row = rows[0];
    return res.json({
      code: 0,
      message: "ok",
      data: {
        serialNo: row.serial_no,
        deviceModel: row.device_model,
        version: row.version,
        reportType: row.report_type,
        expireTime: row.expire_time,
        reportTotal: Number(row.report_total || 0),
        reportXiYi: Number(row.report_xiyi || 0),
        reportZhongYi: Number(row.report_zhongyi || 0),
        reportMianZhen: Number(row.report_mianzhen || 0),
        reportDanXiang: Number(row.report_danxiang || 0),
        imageSavePath: row.image_save_path || "",
        reversePortraitImage: Boolean(row.reverse_portrait_image),
        reportCountHint: Number(row.report_count_hint || 0),
        reportDayHint: Number(row.report_day_hint || 0),
        screenCaptureEnable: Boolean(row.screen_capture_enable),
        typecCameraEnable: Boolean(row.typec_camera_enable),
        qrCodeUrl: row.qr_code_url || ""
      }
    });
  } catch (e) {
    next(e);
  }
});

router.post("/settings", async (req, res, next) => {
  try {
    const uid = req.user.uid;
    const payload = {
      ...defaultSettings,
      ...req.body
    };
    const now = Date.now();

    await query(
      `INSERT INTO system_settings (
        user_id, serial_no, device_model, version, report_type, expire_time,
        report_total, report_xiyi, report_zhongyi, report_mianzhen, report_danxiang,
        image_save_path, reverse_portrait_image, report_count_hint, report_day_hint,
        screen_capture_enable, typec_camera_enable, qr_code_url, created_at, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE
        serial_no = VALUES(serial_no),
        device_model = VALUES(device_model),
        version = VALUES(version),
        report_type = VALUES(report_type),
        expire_time = VALUES(expire_time),
        report_total = VALUES(report_total),
        report_xiyi = VALUES(report_xiyi),
        report_zhongyi = VALUES(report_zhongyi),
        report_mianzhen = VALUES(report_mianzhen),
        report_danxiang = VALUES(report_danxiang),
        image_save_path = VALUES(image_save_path),
        reverse_portrait_image = VALUES(reverse_portrait_image),
        report_count_hint = VALUES(report_count_hint),
        report_day_hint = VALUES(report_day_hint),
        screen_capture_enable = VALUES(screen_capture_enable),
        typec_camera_enable = VALUES(typec_camera_enable),
        qr_code_url = VALUES(qr_code_url),
        updated_at = VALUES(updated_at)`,
      [
        uid,
        payload.serialNo,
        payload.deviceModel,
        payload.version,
        payload.reportType,
        payload.expireTime,
        Number(payload.reportTotal || 0),
        Number(payload.reportXiYi || 0),
        Number(payload.reportZhongYi || 0),
        Number(payload.reportMianZhen || 0),
        Number(payload.reportDanXiang || 0),
        payload.imageSavePath || "",
        payload.reversePortraitImage ? 1 : 0,
        Number(payload.reportCountHint || 0),
        Number(payload.reportDayHint || 0),
        payload.screenCaptureEnable ? 1 : 0,
        payload.typecCameraEnable ? 1 : 0,
        payload.qrCodeUrl || "",
        now,
        now
      ]
    );

    return res.json({ code: 0, message: "ok", data: payload });
  } catch (e) {
    next(e);
  }
});

router.get("/version/check", async (req, res) => {
  return res.json({
    code: 0,
    message: "ok",
    data: {
      hasNewVersion: false,
      latestVersion: "v1.0.74",
      downloadUrl: ""
    }
  });
});

module.exports = router;
