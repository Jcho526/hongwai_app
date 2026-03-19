<template>
  <view class="page">
    <!-- 顶部信息 -->
    <view class="header">
      <text class="title">已采集 {{ session.images.length }} / {{ session.max }} 张</text>
    </view>

    <!-- 图片列表 -->
    <scroll-view class="list" scroll-y>
      <view class="img-grid">
        <view
          class="img-item"
          v-for="(img, idx) in session.images"
          :key="idx"
        >
          <image class="img" :src="img.path" mode="aspectFill" />
          <view class="del" @tap="remove(idx)">×</view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部操作 -->
    <view class="bottom">
      <view
        class="btn"
        :class="{ disabled: !canCapture }"
        @tap="onCapture"
      >
        继续采图
      </view>

      <view class="btn primary" @tap="onReport">
        生成报告
      </view>
    </view>
  </view>
</template>

<script>
const SESSION_KEY = 'capture_session';

export default {
  data() {
    return {
      session: {
        images: [],
        max: 0
      }
    };
  },
  onShow() {
    const s = uni.getStorageSync(SESSION_KEY);
    if (s) this.session = s;
  },
  computed: {
    canCapture() {
      return this.session.images.length < this.session.max;
    }
  },
  methods: {
    // 删除某一张
    remove(idx) {
      this.session.images.splice(idx, 1);
      uni.setStorageSync(SESSION_KEY, this.session);
    },

    // 继续采图
    onCapture() {
      const SESSION_KEY = "capture_session";
      const TEMP_KEY = "capture_temp";
    
      // 1️⃣ 读取采集会话
      const session = uni.getStorageSync(SESSION_KEY);
    
      if (!session || !Array.isArray(session.images)) {
        uni.showToast({ title: "采集会话异常", icon: "none" });
        return;
      }
    
      // 2️⃣ 判断是否超过上限
      if (session.images.length >= session.max) {
        uni.showToast({
          title: `已达到最大采集数量（${session.max} 张）`,
          icon: "none"
        });
        return;
      }
    
      // ======================
      // 3️⃣ H5：生成模拟图片
      // ======================
      // #ifdef H5
      const index = session.images.length + 1;
      const symbolMap = ["①", "②", "③", "④"];
      const symbol = symbolMap[index - 1] || "✓";
    
      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200">
          <rect width="100%" height="100%" fill="#000"/>
          <text x="50%" y="45%" text-anchor="middle"
                dominant-baseline="middle"
                font-size="260"
                fill="#22c1be">${symbol}</text>
          <text x="50%" y="60%" text-anchor="middle"
                dominant-baseline="middle"
                font-size="40"
                fill="#fff">
            Mock Image ${index} / ${session.max}
          </text>
        </svg>
      `.trim();
    
      const dataUrl =
        "data:image/svg+xml;base64," +
        btoa(unescape(encodeURIComponent(svg)));
    
      uni.setStorageSync(TEMP_KEY, dataUrl);
    
      uni.showToast({
        title: `已采集 ${index} / ${session.max}`,
        icon: "none"
      });
    
      // 👉 如果你有预览页，打开它
      // uni.navigateTo({ url: "/pages/capturePreview/capturePreview" });
    
      return;
      // #endif
    
      // ======================
      // 4️⃣ 真机：调用相机
      // ======================
      const ctx = uni.createCameraContext();
      ctx.takePhoto({
        quality: "high",
        success: (res) => {
          uni.setStorageSync(TEMP_KEY, res.tempImagePath);
    
          uni.showToast({
            title: `已采集 ${session.images.length + 1} / ${session.max}`,
            icon: "none"
          });
    
          // uni.navigateTo({ url: "/pages/capturePreview/capturePreview" });
        },
        fail: (err) => {
          uni.showToast({
            title: "采图失败",
            icon: "none"
          });
          console.error(err);
        }
      });
    },


    // 生成报告（占位）
    onReport() {
      uni.showToast({ title: '生成报告（待接入）', icon: 'none' });
    }
  }
};
</script>

<style scoped>
.page {
  height: 100vh;
  background: #000;
  display: flex;
  flex-direction: column;
}

.header {
  height: 90rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
}

.list {
  flex: 1;
}

.img-grid {
  display: flex;
  flex-wrap: wrap;
  padding: 20rpx;
  gap: 20rpx;
}

.img-item {
  width: calc(50% - 10rpx);
  height: 260rpx;
  position: relative;
}

.img {
  width: 100%;
  height: 100%;
  border-radius: 10rpx;
}

.del {
  position: absolute;
  right: 8rpx;
  top: 8rpx;
  width: 40rpx;
  height: 40rpx;
  border-radius: 20rpx;
  background: rgba(0,0,0,.6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
}

.bottom {
  height: 140rpx;
  display: flex;
  gap: 20rpx;
  padding: 20rpx;
  box-sizing: border-box;
}

.btn {
  flex: 1;
  height: 100rpx;
  border-radius: 12rpx;
  background: #666;
  color: #fff;
  font-size: 32rpx;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn.primary {
  background: #22c1be;
}

.btn.disabled {
  opacity: 0.4;
}
</style>
