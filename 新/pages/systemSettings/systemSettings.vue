<template>
  <view class="page">
    <view class="topbar">
      <view class="top-left" @tap="goBack">‹</view>
      <text class="top-title">系统设置</text>
      <view class="top-right" @tap="logout">退出</view>
    </view>

    <scroll-view class="content" scroll-y>
      <view class="row two-col">
        <text class="label">序列号：{{ form.serialNo }}</text>
        <text class="label">报告类型：{{ form.reportType }}</text>
      </view>

      <view class="row two-col">
        <text class="label">设备型号：{{ form.deviceModel }}</text>
        <text class="label">到期时间：{{ form.expireTime }}</text>
      </view>

      <view class="row two-col">
        <text class="label">版本号：{{ form.version }}</text>
        <view class="report-col">
          <text class="label">出报告总次：{{ form.reportTotal }}次</text>
          <text class="label">西医：{{ form.reportXiYi }}次</text>
          <text class="label">中医：{{ form.reportZhongYi }}次</text>
          <text class="label">面诊：{{ form.reportMianZhen }}次</text>
          <text class="label">单项：{{ form.reportDanXiang }}次</text>
        </view>
      </view>

      <view class="link-row" @tap="onChangePassword">修改密码</view>
      <view class="link-row" @tap="deactivateAccount">注销用户</view>

      <view class="agreement-row">
        <text class="agreement-link" @tap="openAgreement('user')">《用户协议》</text>
        <text class="label"> 和 </text>
        <text class="agreement-link" @tap="openAgreement('privacy')">《隐私协议》</text>
      </view>

      <view class="input-row">
        <text class="label">图片保存的位置：</text>
        <input class="line-input" v-model="form.imageSavePath" />
      </view>

      <view class="switch-row" @tap="form.reversePortraitImage = !form.reversePortraitImage">
        <text class="label">竖屏时成像是否反向</text>
        <switch :checked="form.reversePortraitImage" color="#00c4b8" />
      </view>

      <view class="set-row">
        <view class="input-row small">
          <text class="label">报告次数提示：</text>
          <input class="line-input" type="number" v-model="form.reportCountHint" />
        </view>
        <view class="input-row small">
          <text class="label">报告天数提示：</text>
          <input class="line-input" type="number" v-model="form.reportDayHint" />
        </view>
        <button class="set-btn" @tap="saveSettings" :loading="saving">设置</button>
      </view>

      <view class="qr-box">
        <view class="qr-placeholder">
          <text class="qr-txt">二维码区域</text>
        </view>
        <text class="qr-desc">扫码添加人员</text>
      </view>

      <view class="switch-row" @tap="form.screenCaptureEnable = !form.screenCaptureEnable">
        <text class="label">是否横屏拍照</text>
        <switch :checked="form.screenCaptureEnable" color="#00c4b8" />
      </view>

      <view class="switch-row" @tap="form.typecCameraEnable = !form.typecCameraEnable">
        <text class="label">是否Type-c线式连接热成像设备</text>
        <switch :checked="form.typecCameraEnable" color="#00c4b8" />
      </view>

      <button class="version-btn" @tap="checkVersion" :loading="checkingVersion">版本检查更新</button>
    </scroll-view>
  </view>
</template>

<script>
import {
  getSystemSettings,
  saveSystemSettings,
  logoutRequest,
  deactivateAccountRequest,
  checkVersionRequest
} from "../../services/systemSettings";
import { clearAuthToken } from "../../services/http";

export default {
  data() {
    return {
      loading: false,
      saving: false,
      checkingVersion: false,
      form: {
        serialNo: "",
        deviceModel: "",
        version: "",
        reportType: "",
        expireTime: "",
        reportTotal: 0,
        reportXiYi: 0,
        reportZhongYi: 0,
        reportMianZhen: 0,
        reportDanXiang: 0,
        imageSavePath: "",
        reversePortraitImage: false,
        reportCountHint: 20,
        reportDayHint: 10,
        screenCaptureEnable: false,
        typecCameraEnable: false,
        qrCodeUrl: ""
      }
    };
  },
  onShow() {
    this.loadSettings();
  },
  methods: {
    async loadSettings() {
      this.loading = true;
      try {
        const data = await getSystemSettings();
        this.form = { ...this.form, ...data };
      } catch (e) {
        uni.showToast({ title: "加载设置失败", icon: "none" });
      } finally {
        this.loading = false;
      }
    },
    goBack() {
      uni.navigateBack({ delta: 1 });
    },
    async saveSettings() {
      this.saving = true;
      try {
        const payload = {
          ...this.form,
          reportCountHint: Number(this.form.reportCountHint || 0),
          reportDayHint: Number(this.form.reportDayHint || 0)
        };
        const saved = await saveSystemSettings(payload);
        this.form = { ...this.form, ...saved };
        uni.showToast({ title: "设置成功", icon: "success" });
      } catch (e) {
        uni.showToast({ title: "设置失败", icon: "none" });
      } finally {
        this.saving = false;
      }
    },
    async logout() {
      try {
        await logoutRequest();
      } catch (e) {}
      clearAuthToken();
      uni.reLaunch({ url: "/pages/index/index" });
    },
    async deactivateAccount() {
      uni.showModal({
        title: "提示",
        content: "确认注销当前用户？",
        success: async (res) => {
          if (!res.confirm) return;
          try {
            await deactivateAccountRequest();
            uni.showToast({ title: "已注销", icon: "success" });
          } catch (e) {
            uni.showToast({ title: "注销失败", icon: "none" });
          }
        }
      });
    },
    onChangePassword() {
      uni.showToast({ title: "修改密码接口待接入", icon: "none" });
    },
    openAgreement(type) {
      const text = type === "user" ? "用户协议" : "隐私协议";
      uni.showToast({ title: `${text}待接入`, icon: "none" });
    },
    async checkVersion() {
      this.checkingVersion = true;
      try {
        const res = await checkVersionRequest();
        if (res && res.hasNewVersion) {
          uni.showModal({
            title: "发现新版本",
            content: `最新版本：${res.latestVersion || "未知"}`,
            showCancel: false
          });
        } else {
          uni.showToast({ title: "当前已是最新版本", icon: "none" });
        }
      } catch (e) {
        uni.showToast({ title: "检查失败", icon: "none" });
      } finally {
        this.checkingVersion = false;
      }
    }
  }
};
</script>

<style scoped>
.page {
  height: 100vh;
  background: #22c1be;
  color: #fff;
}

.topbar {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24rpx;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.35);
}

.top-left,
.top-right {
  width: 120rpx;
  font-size: 34rpx;
}

.top-right {
  text-align: right;
  font-size: 30rpx;
}

.top-title {
  font-size: 36rpx;
  font-weight: 600;
}

.content {
  height: calc(100vh - 88rpx);
  padding: 26rpx;
  box-sizing: border-box;
}

.row {
  margin-bottom: 22rpx;
}

.two-col {
  display: flex;
  justify-content: space-between;
  gap: 20rpx;
}

.report-col {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.label {
  font-size: 34rpx;
  line-height: 1.6;
}

.link-row {
  font-size: 40rpx;
  margin: 20rpx 0;
}

.agreement-row {
  display: flex;
  align-items: center;
  margin: 30rpx 0;
}

.agreement-link {
  font-size: 36rpx;
  color: #ff2a2a;
}

.input-row {
  display: flex;
  align-items: center;
  margin: 20rpx 0;
}

.line-input {
  flex: 1;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.8);
  color: #fff;
  font-size: 34rpx;
  padding: 8rpx 12rpx;
}

.switch-row {
  margin: 34rpx 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.set-row {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin: 30rpx 0;
}

.small {
  flex: 1;
  margin: 0;
}

.set-btn {
  width: 180rpx;
  height: 86rpx;
  line-height: 86rpx;
  background: rgba(0, 0, 0, 0.15);
  color: #fff;
  border-radius: 12rpx;
  font-size: 34rpx;
}

.set-btn::after,
.version-btn::after {
  border: none;
}

.qr-box {
  margin: 34rpx 0;
  width: 260rpx;
  text-align: center;
}

.qr-placeholder {
  width: 260rpx;
  height: 260rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-txt {
  color: #999;
  font-size: 24rpx;
}

.qr-desc {
  margin-top: 12rpx;
  font-size: 32rpx;
}

.version-btn {
  margin-top: 30rpx;
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background: rgba(0, 0, 0, 0.15);
  color: #fff;
  border-radius: 12rpx;
  font-size: 38rpx;
}
</style>
