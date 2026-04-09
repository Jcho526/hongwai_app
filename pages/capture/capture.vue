<template>
  <view class="cap-page">
    <view class="preview">
      <camera class="camera" device-position="back" flash="auto"></camera>

      <view class="tip">
        <text class="tip-text">{{ tipText }}</text>
      </view>
    </view>

    <view class="toolbar">
      <view class="tool-item" @tap.stop="onCompare">
        <image class="tool-icon" src="/static/icons/compare2.png" mode="aspectFit" />
        <text class="tool-text">对比</text>
      </view>

      <view class="tool-item" @tap.stop="onExit">
        <image class="tool-icon" src="/static/icons/out3.png" mode="aspectFit" />
        <text class="tool-text">退出</text>
      </view>

      <view class="tool-item center" @tap.stop="onCapture">
        <image class="tool-icon big" src="/static/icons/zhao2.png" mode="aspectFit" />
        <text class="tool-text strong">采图</text>
      </view>

      <view class="tool-item" @tap.stop="onGenReport">
        <image class="tool-icon" src="/static/icons/baogao2.png" mode="aspectFit" />
        <text class="tool-text">生成报告</text>
      </view>
    </view>

    <view class="safe-pad"></view>
  </view>
</template>

<script>
const SESSION_KEY = "capture_session";
const TEMP_KEY = "capture_temp";

// API 配置（内联）
const API_CONFIG = {
  baseUrl: 'http://localhost:5000',
  timeout: 300000
};
function getApiUrl() {
  return API_CONFIG.baseUrl + '/api/v1/generate-pdf';
}
function getApiTimeout() {
  return API_CONFIG.timeout;
}

function pad2(n) {
  return n < 10 ? "0" + n : "" + n;
}
function fmtTime(ts) {
  const d = new Date(ts);
  return (
    d.getFullYear() +
    "-" + pad2(d.getMonth() + 1) +
    "-" + pad2(d.getDate()) +
    " " + pad2(d.getHours()) +
    ":" + pad2(d.getMinutes()) +
    ":" + pad2(d.getSeconds())
  );
}

export default {
  data() {
    return {
      personId: "",
      mode: "quanke",
      max: 4,
      imagesCount: 0
    };
  },

  computed: {
    tipText() {
      if (this.mode === "mianzhen") {
        return "请按采集标准拍照（拍照顺序为头正面一张，抬头一张）";
      }
      return "请按采集标准拍摄（按照上身正面，下身正面，上身反面，下身反面顺序）";
    }
  },

  onShow() {
    this.syncSession();
  },

  methods: {
    syncSession() {
      const s = uni.getStorageSync(SESSION_KEY);
      if (s && typeof s === "object") {
        this.personId = String(s.personId || "");
        this.mode = s.mode || "quanke";
        this.max = Number(s.max || (this.mode === "mianzhen" ? 2 : 4));
        this.imagesCount = Array.isArray(s.images) ? s.images.length : 0;
        return;
      }

      const fallback = {
        personId: this.personId || "",
        mode: this.mode,
        max: this.mode === "mianzhen" ? 2 : 4,
        images: []
      };
      uni.setStorageSync(SESSION_KEY, fallback);
      this.max = fallback.max;
      this.imagesCount = 0;
    },

    saveToPersonStore(path) {
      const pid = this.personId;
      if (!pid) return;

      const key = `person_photos_${pid}`;
      let arr = [];
      try {
        const old = uni.getStorageSync(key);
        if (Array.isArray(old)) arr = old;
      } catch (e) {}

      const ts = Date.now();
      const item = {
        id: String(ts) + "_" + Math.random().toString(16).slice(2),
        path,
        ts,
        timeText: fmtTime(ts)
      };

      arr.unshift(item);

      try {
        uni.setStorageSync(key, arr);
      } catch (e) {}
    },

    pushToSession(path) {
      const s = uni.getStorageSync(SESSION_KEY) || {};
      if (!Array.isArray(s.images)) s.images = [];
      s.images.push({ path, ts: Date.now() });
      uni.setStorageSync(SESSION_KEY, s);

      this.imagesCount = s.images.length;
      this.max = Number(s.max || this.max);
      this.mode = s.mode || this.mode;
      this.personId = String(s.personId || this.personId);
    },

    onCompare() {
      uni.showToast({ title: "对比（待接入）", icon: "none" });
    },

    onExit() {
      uni.navigateBack();
    },

    onCapture() {
      const session = uni.getStorageSync(SESSION_KEY);

      if (!session || !Array.isArray(session.images)) {
        uni.showToast({ title: "采集会话异常", icon: "none" });
        this.syncSession();
        return;
      }

      this.personId = String(session.personId || "");
      this.mode = session.mode || this.mode;
      this.max = Number(session.max || (this.mode === "mianzhen" ? 2 : 4));
      this.imagesCount = session.images.length;

      //上限限制
      if (this.imagesCount >= this.max) {
        uni.showToast({ title: `已达到上限（${this.max}张）`, icon: "none" });
        return;
      }

     
      // 生成的假照片方便用来测试（后期要进行更改）
      // #ifdef H5
      const idx = this.imagesCount + 1;
      const symbolMap = ["①", "②", "③", "④"];
      const symbol = symbolMap[idx - 1] || "✓";
      const nowText = fmtTime(Date.now());

      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200">
          <rect width="100%" height="100%" fill="#111"/>
          <text x="50%" y="45%" text-anchor="middle" dominant-baseline="middle"
                font-size="260" fill="#22c1be" font-family="Arial">${symbol}</text>
          <text x="50%" y="60%" text-anchor="middle" dominant-baseline="middle"
                font-size="44" fill="#ffffff" font-family="Arial">Mock ${idx}/${this.max}</text>
          <text x="50%" y="70%" text-anchor="middle" dominant-baseline="middle"
                font-size="34" fill="#bdbdbd" font-family="Arial">${nowText}</text>
        </svg>
      `.trim();

      const dataUrl =
        "data:image/svg+xml;base64," +
        btoa(unescape(encodeURIComponent(svg)));

      uni.setStorageSync(TEMP_KEY, dataUrl);

      //保存拍的（无论用户之后是否退出，符合说明书上写的）
      this.saveToPersonStore(dataUrl);
      this.pushToSession(dataUrl);

      uni.showToast({ title: `已采集 ${this.imagesCount}/${this.max}`, icon: "none" });
      return;
      // #endif

      const ctx = uni.createCameraContext();
      ctx.takePhoto({
        quality: "high",
        success: (res) => {
          const tempPath = res.tempImagePath;

          uni.saveFile({
            tempFilePath: tempPath,
            success: (r) => {
              const savedPath = r.savedFilePath || tempPath;
              uni.setStorageSync(TEMP_KEY, savedPath);

              this.saveToPersonStore(savedPath);
              this.pushToSession(savedPath);

              uni.showToast({ title: `已采集 ${this.imagesCount}/${this.max}`, icon: "none" });
            },
            fail: () => {
              
              uni.setStorageSync(TEMP_KEY, tempPath);

              this.saveToPersonStore(tempPath);
              this.pushToSession(tempPath);

              uni.showToast({ title: `已采集 ${this.imagesCount}/${this.max}`, icon: "none" });
            }
          });
        },
        fail: (err) => {
          console.error("takePhoto fail:", err);
          uni.showToast({ title: "采图失败：" + (err.errMsg || ""), icon: "none" });
        }
      });
    },

    async onGenReport() {
      // 检查是否有采集的图片
      const session = uni.getStorageSync(SESSION_KEY);
      if (!session || !Array.isArray(session.images) || session.images.length === 0) {
        uni.showToast({ title: "请先采集图片", icon: "none" });
        return;
      }

      // 获取最后一张图片
      const lastImage = session.images[session.images.length - 1];
      if (!lastImage || !lastImage.path) {
        uni.showToast({ title: "图片数据异常", icon: "none" });
        return;
      }

      uni.showLoading({ title: "正在生成报告..." });

      try {
        // 读取图片文件
        const imageData = await this.readImageAsBase64(lastImage.path);
        
        // 调用 PDF 生成 API
        const result = await this.callGeneratePdfApi(imageData, session);
        
        if (result.success) {
          uni.hideLoading();
          uni.showToast({ 
            title: "✅ 报告生成成功！",
            icon: "success",
            duration: 2000
          });
          
          // 保存 PDF 信息到本地
          this.savePdfInfo(result);
          
          // 2秒后跳转到报告列表
          setTimeout(() => {
            uni.navigateTo({
              url: `/pages/photoRecords/photoRecords?personId=${session.personId}`
            });
          }, 2000);
        } else {
          throw new Error(result.error || "API 返回失败");
        }
      } catch (error) {
        uni.hideLoading();
        console.error("生成报告失败:", error);
        uni.showToast({ 
          title: "❌ 生成失败: " + (error.message || "未知错误"),
          icon: "none",
          duration: 3000
        });
      }
    },

    readImageAsBase64(imagePath) {
      return new Promise((resolve, reject) => {
        // 如果是 data URL（H5 开发环境），直接返回
        if (imagePath.startsWith('data:')) {
          resolve(imagePath);
          return;
        }

        // 真机环境：读取文件转换为 base64
        uni.getFileInfo({
          filePath: imagePath,
          success: (res) => {
            uni.readFile({
              filePath: imagePath,
              encoding: 'base64',
              success: (fileRes) => {
                // 返回 base64 编码的图片数据
                resolve('data:image/png;base64,' + fileRes.data);
              },
              fail: (err) => {
                reject(new Error("读取图片失败: " + err.errMsg));
              }
            });
          },
          fail: (err) => {
            reject(new Error("获取文件信息失败: " + err.errMsg));
          }
        });
      });
    },

    async callGeneratePdfApi(imageBase64Data, session) {
      // 获取 API URL 和超时时间
      const apiUrl = getApiUrl();
      const timeout = getApiTimeout();
      
      // 从 session 中获取患者信息
      const patientName = session.patientName || "未命名患者";
      const patientAge = session.patientAge || 0;
      const patientGender = session.patientGender || "未知";
      const patientId = session.personId || "";
      
      try {
        // 使用 uni.request 上传 base64 图片
        return new Promise((resolve, reject) => {
          uni.request({
            url: apiUrl,
            method: 'POST',
            header: {
              'Content-Type': 'application/json'
            },
            data: {
              image_base64: imageBase64Data,  // base64 编码的图片
              patient_name: patientName,
              patient_age: patientAge,
              patient_gender: patientGender,
              patient_id: patientId,
              template: 'universal'
            },
            timeout: timeout,  // 使用配置的超时时间
            success: (res) => {
              console.log("API 响应状态码:", res.statusCode);
              
              // 检查响应状态
              if (res.statusCode === 200) {
                // API 返回 DOCX 文件（二进制）或附件
                // 文件内容在 res.data 中
                console.log("✅ 报告生成成功");
                
                resolve({
                  success: true,
                  data: res.data,  // 二进制数据
                  filename: res.header['content-disposition'] || 'report.docx',
                  statusCode: res.statusCode,
                  error: null
                });
              } else if (res.statusCode >= 400) {
                // API 返回错误信息（JSON）
                try {
                  const errorData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
                  const errorMsg = errorData?.error || "生成报告失败";
                  reject(new Error(errorMsg));
                } catch (e) {
                  reject(new Error("生成报告失败（错误代码：" + res.statusCode + "）"));
                }
              } else {
                reject(new Error("未知错误（状态码：" + res.statusCode + "）"));
              }
            },
            fail: (err) => {
              console.error("请求失败:", err);
              
              // 检查是否是网络连接问题
              if (err.errMsg.includes('timeout')) {
                reject(new Error("请求超时，请检查网络连接或增加超时时间"));
              } else if (err.errMsg.includes('connect')) {
                reject(new Error("❌ 无法连接到 API 服务\n请确保已启动 API:\npython thermal_api.py"));
              } else if (err.errMsg.includes('ECONNREFUSED')) {
                reject(new Error("❌ API 连接被拒绝\n请确保 API 已启动"));
              } else {
                reject(new Error("网络请求失败: " + err.errMsg));
              }
            }
          });
        });
      } catch (error) {
        console.error("API 调用错误:", error);
        throw error;
      }
    },

    savePdfInfo(result) {
      // 保存生成的报告信息到本地存储
      const session = uni.getStorageSync(SESSION_KEY);
      const pid = session.personId;
      
      if (!pid) return;

      const key = `person_reports_${pid}`;
      let reports = [];
      
      try {
        const old = uni.getStorageSync(key);
        if (Array.isArray(old)) reports = old;
      } catch (e) {
        console.error("读取报告列表失败:", e);
      }

      // 生成报告对象
      const report = {
        id: String(Date.now()) + "_" + Math.random().toString(16).slice(2),
        name: `热图分析报告_${session.patientName || '患者'}_${fmtTime(Date.now())}`,
        docxData: result.data,  // 二进制 DOCX 文件数据
        ts: Date.now(),
        timeText: fmtTime(Date.now()),
        patientName: session.patientName || "未命名患者",
        patientAge: session.patientAge || 0,
        patientGender: session.patientGender || "未知",
        patientId: pid,
        status: 'generated'
      };

      // 添加到报告列表（最新的在最前）
      reports.unshift(report);

      // 限制保存的报告数量（避免本地存储过大）
      if (reports.length > 100) {
        reports = reports.slice(0, 100);
      }

      try {
        uni.setStorageSync(key, reports);
        console.log("✅ 报告信息已保存", key);
      } catch (e) {
        console.error("❌ 保存报告信息失败:", e);
      }
    }
  }
};
</script>

<style scoped>
.cap-page { height: 100vh; background: #000; display: flex; flex-direction: column; }
.preview { flex: 1; position: relative; background: #000; }
.camera { width: 100%; height: 100%; }
.tip { position: absolute; left: 0; right: 0; bottom: 18rpx; display: flex; justify-content: center; }
.tip-text { color: #d11; font-size: 30rpx; font-weight: 800; padding: 10rpx 18rpx; border-radius: 8rpx; background: rgba(0,0,0,.35); }

.toolbar {
  height: 240rpx; background: #000;
  display: flex; align-items: center; justify-content: space-around;
  padding: 0 22rpx 30rpx; box-sizing: border-box;
  position: relative; z-index: 9999;
}
.tool-item { width: 150rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10rpx; }
.tool-icon { width: 76rpx; height: 76rpx; }
.tool-icon.big { width: 110rpx; height: 110rpx; }
.tool-text { color: #fff; font-size: 26rpx; }
.tool-text.strong { font-size: 30rpx; font-weight: 900; }
.tool-item.center { transform: translateY(-14rpx); }

.safe-pad { height: env(safe-area-inset-bottom); background: #000; }
</style>
