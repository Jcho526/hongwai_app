<template>
  <view class="main-container">
    <!-- 顶部状态栏：摄像头图标和版本号 -->
    <image
      src="/static/icons/camera.png"
      mode="aspectFit"
      class="camera-icon-top"
      @tap="takePhoto"
    ></image>

    <text class="version-top">v1.0.36</text>
    <text class="title">红外热成像健康管理系统</text>

    <!-- 环形菜单图 -->
    <view class="menu-circle-wrapper" @tap="handleMenuClick">
      <view class="menu-circle-inner"></view>
    </view>

    <!-- 底部九宫格按钮 -->
    <view class="bottom-buttons">
      <view class="btn-item" @tap="goToPerson">
        <image src="/static/icons/user.png" class="btn-icon"></image>
        <text class="btn-text">人员管理</text>
      </view>

      <!-- ✅ 记录管理：直接跳到第二张图页面 -->
      <view class="btn-item" @tap="goRecordManage">
        <image src="/static/icons/record.png" class="btn-icon"></image>
        <text class="btn-text">记录管理</text>
      </view>

      <view class="btn-item" @tap="goToLive">
        <image src="/static/icons/live.png" class="btn-icon"></image>
        <text class="btn-text">实时监控</text>
      </view>

      <view class="btn-item" @tap="goToSystem">
        <image src="/static/icons/settings.png" class="btn-icon"></image>
        <text class="btn-text">系统设置</text>
      </view>

      <view class="btn-item" @tap="goToCompare">
        <image src="/static/icons/compare.png" class="btn-icon"></image>
        <text class="btn-text">对比</text>
      </view>

      <view class="btn-item" @tap="goToFeedback">
        <image src="/static/icons/feedback.png" class="btn-icon"></image>
        <text class="btn-text">意见反馈</text>
      </view>
    </view>

    <button class="logout-btn" @tap="logout">退出</button>
  </view>
</template>

<script>
import { logout as logoutRequest } from "../../services/auth";

export default {
  methods: {
    // 顶部摄像头图标
    takePhoto() {
      // TODO：跳转到拍照页面（你后续接 capture/checkItems 都行）
      uni.showToast({ title: "拍照（待接入）", icon: "none" });
    },

    goToPerson() {
      uni.navigateTo({ url: "/pages/person/person" });
    },

    // ✅ 核心：记录管理跳转
    goRecordManage() {
      // ⚠️ 如果你记录管理页面路径不是这个，把下面 url 改成你 pages.json 对应的 path
      const url = "/pages/recordManage/recordManage";

      uni.navigateTo({
        url,
        fail: (err) => {
          const msg = (err && err.errMsg) ? err.errMsg : "";
          // 如果它被你配置成 tabBar 页面，需要 switchTab
          if (msg.includes("tabbar")) {
            uni.switchTab({ url });
            return;
          }
          console.error("goRecordManage fail:", err);
          uni.showToast({ title: "跳转失败：" + msg, icon: "none" });
        }
      });
    },

    goToLive() {
      uni.showToast({ title: "实时监控（待接入）", icon: "none" });
    },

    goToSystem() {
      uni.navigateTo({ url: "/pages/systemSettings/systemSettings" });
    },

    goToCompare() {
      uni.showToast({ title: "对比（待接入）", icon: "none" });
    },

    goToFeedback() {
      uni.navigateTo({ url: "/pages/feedback/feedback" });
    },

    logout() {
      uni.showModal({
        title: "提示",
        content: "确定要退出登录吗？",
        success: async (res) => {
          if (res.confirm) {
            try {
              await logoutRequest();
            } catch (e) {}
            uni.reLaunch({
              url: "/pages/index/index"
            });
          }
        }
      });
    },

    handleMenuClick() {
      uni.showToast({
        title: "点击了环形菜单",
        icon: "none"
      });
    }
  }
};
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background-color: #00c4b8;
  padding: 20rpx;
  position: relative;
}

/* 摄像头图标 */
.camera-icon-top {
  width: 100rpx;
  height: 100rpx;
  position: absolute;
  top: 10rpx;
  left: 10rpx;
  z-index: 100;
}

/* 版本号 */
.version-top {
  font-size: 32rpx;
  color: white;
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  z-index: 100;
}

.title {
  font-size: 50rpx;
  color: white;
  font-weight: bold;
  margin-top: 140rpx;
  margin-bottom: 30rpx;
}

/* 环形菜单 */
.menu-circle-wrapper {
  width: 600px;
  height: 600px;
  margin: 40rpx auto;
  border-radius: 50%;
  background-image: url("/static/icons/1.png");
  background-size: contain;
  background-position: center;
  box-shadow: 0 0 30rpx rgba(0, 0, 0, 0.4);
  z-index: 50;
  transition: transform 0.3s ease;
}
.menu-circle-wrapper:active {
  transform: scale(1.03);
}
.menu-circle-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: transparent;
}

.bottom-buttons {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30rpx;
  position: absolute;
  bottom: 600rpx;
  left: 0;
  right: 0;
  margin: 0 auto;
}

.btn-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30rpx;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  color: white;
  font-size: 36rpx;
}

.btn-icon {
  width: 60rpx;
  height: 60rpx;
  margin-bottom: 15rpx;
}

.btn-text {
  color: #fff;
  font-size: 36rpx;
}

.logout-btn {
  position: absolute;
  bottom: 200rpx;
  left: 50%;
  transform: translateX(-50%);
  background-color: #f44336;
  color: white;
  font-size: 36rpx;
  padding: 25rpx 40rpx;
  border-radius: 20rpx;
  width: 240rpx;
}
</style>
