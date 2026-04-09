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

      <!-- API 配置部分 -->
      <view class="section-divider">
        <text class="section-title">🔥 API 服务配置</text>
      </view>

      <view class="input-row">
        <text class="label">API 服务地址：</text>
        <input class="line-input" v-model="apiConfig.baseUrl" placeholder="e.g. http://localhost:5000" />
      </view>

      <view class="status-box" :class="{ 'status-online': apiStatus === 'connected', 'status-offline': apiStatus === 'disconnected' }">
        <text class="status-icon">{{ apiStatus === 'connected' ? '🟢' : '🔴' }}</text>
        <text class="status-text">API 状态: {{ apiStatus === 'connected' ? '已连接' : apiStatus === 'checking' ? '检查中...' : '未连接' }}</text>
        <button class="check-btn" @tap="checkApiConnection" :loading="checkingApi">检查连接</button>
      </view>

      <view v-if="apiStatusInfo" class="api-info-box">
        <text class="info-title">📊 API 信息：</text>
        <text class="info-text">• 服务: {{ apiStatusInfo.service }}</text>
        <text class="info-text">• 版本: {{ apiStatusInfo.version }}</text>
        <text class="info-text">• 输出目录: {{ apiStatusInfo.output_folder }}</text>
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
import { getApiConfig, checkApiHealth, getApiStatus } from "../../services/apiConfig.js";

export default {
  data() {
    return {
      loading: false,
      saving: false,
      checkingVersion: false,
      checkingApi: false,
      apiStatus: 'checking', // 'checking', 'connected', 'disconnected'
      apiStatusInfo: null,
      apiConfig: {
        baseUrl: 'http://localhost:5000'
      },
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
    this.checkApiConnection(); // 检查 API 连接
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
    },
    async checkApiConnection() {
      this.checkingApi = true;
      this.apiStatus = 'checking';
      
      try {
        // 检查 API 健康状态
        const isHealthy = await checkApiHealth();
        
        if (isHealthy) {
          // 获取 API 详细状态
          this.apiStatusInfo = await getApiStatus();
          this.apiStatus = 'connected';
          uni.showToast({ title: "✅ API 已连接", icon: "success" });
        } else {
          this.apiStatus = 'disconnected';
          uni.showToast({ title: "❌ 无法连接到 API 服务", icon: "none" });
        }
      } catch (error) {
        this.apiStatus = 'disconnected';
        console.error('API 连接检查失败:', error);
        uni.showToast({ 
          title: "❌ 连接失败，请确保 API 已启动", 
          icon: "none" 
        });
      } finally {
        this.checkingApi = false;
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

/* API 配置样式 */
.section-divider {
  margin: 40rpx 0 20rpx 0;
  padding-bottom: 15rpx;
  border-bottom: 2rpx solid rgba(255, 255, 255, 0.3);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
}

.status-box {
  display: flex;
  align-items: center;
  gap: 15rpx;
  margin: 20rpx 0;
  padding: 20rpx;
  border-radius: 12rpx;
  background: rgba(0, 0, 0, 0.2);
  border: 1rpx solid rgba(255, 255, 255, 0.3);
}

.status-box.status-online {
  background: rgba(76, 175, 80, 0.2);
  border-color: #4CAF50;
}

.status-box.status-offline {
  background: rgba(244, 67, 54, 0.2);
  border-color: #F44336;
}

.status-icon {
  font-size: 40rpx;
  min-width: 50rpx;
}

.status-text {
  flex: 1;
  font-size: 32rpx;
  color: #fff;
}

.check-btn {
  padding: 12rpx 20rpx;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 8rpx;
  font-size: 28rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.5);
}

.api-info-box {
  margin: 20rpx 0;
  padding: 20rpx;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 12rpx;
  border-left: 4rpx solid #4CAF50;
}

.info-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
  color: #fff;
}

.info-text {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  margin: 8rpx 0;
  word-break: break-all;
}
</style>

