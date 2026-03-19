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

    onGenReport() {
      uni.showToast({ title: "生成报告（待接入）", icon: "none" });
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
