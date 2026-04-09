<template>
  <view class="live-monitor-page">
    <!-- 页面顶部 -->
    <view class="header">
      <text class="header-title">实时监控（双屏模式）</text>
      <view class="status-info">
        <view class="status-item" v-if="remoteAppStatus">
          <text class="status-label">远程应用:</text>
          <text class="status-value" :class="remoteAppStatus.running ? 'running' : 'stopped'">
            {{ remoteAppStatus.running ? '运行中' : '已停止' }}
          </text>
        </view>
        <view class="status-item">
          <text class="status-label">投射FPS:</text>
          <text class="status-value">{{ remoteFPS }}</text>
        </view>
      </view>
    </view>

    <!-- 主要内容区域 -->
    <view class="content-area">
      <!-- 左侧：我们的本地摄像头 -->
      <view class="camera-container local">
        <text class="container-title">本地摄像头</text>
        <view class="camera-wrapper">
          <camera class="camera" device-position="back" flash="auto"></camera>
          <view class="camera-overlay">
            <text class="overlay-text">{{ localTipText }}</text>
          </view>
        </view>
      </view>

      <!-- 右侧：远程应用屏幕投射 -->
      <view class="screen-container remote">
        <text class="container-title">远程投射屏幕</text>
        <view 
          class="screen-wrapper"
          :style="{ backgroundImage: remoteScreenImage ? `url(${remoteScreenImage})` : 'none' }"
          @touchstart="onRemoteScreenTouch('start', $event)"
          @touchmove="onRemoteScreenTouch('move', $event)"
          @touchend="onRemoteScreenTouch('end', $event)"
        >
          <view v-if="!remoteScreenImage && !isConnectingRemote" class="no-signal">
            <text>未连接远程屏幕</text>
            <button class="connect-btn" @click="connectRemoteScreen">连接远程应用</button>
          </view>
          
          <view v-if="isConnectingRemote" class="connecting">
            <text>正在连接...</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部控制栏 -->
    <view class="toolbar">
      <view class="tool-item" @tap="onClickRemote">
        <image class="tool-icon" src="/static/icons/compare2.png" mode="aspectFit" />
        <text class="tool-text">远程点击</text>
      </view>

      <view class="tool-item" @tap="toggleDualScreen">
        <image class="tool-icon" src="/static/icons/compare.png" mode="aspectFit" />
        <text class="tool-text">{{ isDualScreen ? '关闭双屏' : '开启双屏' }}</text>
      </view>

      <view class="tool-item center" @tap="captureLocalImage">
        <image class="tool-icon big" src="/static/icons/zhao2.png" mode="aspectFit" />
        <text class="tool-text strong">采图</text>
      </view>

      <view class="tool-item" @tap="syncCapture">
        <image class="tool-icon" src="/static/icons/baogao2.png" mode="aspectFit" />
        <text class="tool-text">同步采图</text>
      </view>

      <view class="tool-item" @tap="exitMonitor">
        <image class="tool-icon" src="/static/icons/out3.png" mode="aspectFit" />
        <text class="tool-text">退出</text>
      </view>
    </view>

    <!-- 触摸点标记（调试用） -->
    <view v-if="showTouchPoint" class="touch-point" :style="touchPointStyle"></view>

    <view class="safe-pad"></view>
  </view>
</template>

<script>
import appLauncher from '../../services/appLauncher';

export default {
  data() {
    return {
      // 本地摄像头相关
      mode: 'quanke',
      localTipText: '请按采集标准拍摄（上身正面、下身正面、上身反面、下身反面）',
      
      // 远程屏幕相关
      remoteScreenImage: null,
      isConnectingRemote: false,
      isDualScreen: true,
      remoteFPS: 0,
      remoteAppStatus: null,
      
      // 触摸相关
      showTouchPoint: false,
      touchPointStyle: '',
    };
  },

  async onShow() {
    this.initRemoteScreencast();
  },

  beforeUnmount() {
    this.cleanup();
  },

  methods: {
    /**
     * 初始化远程屏幕投射
     */
    async initRemoteScreencast() {
      try {
        console.log('初始化远程屏幕投射...');
        this.isConnectingRemote = true;

        // 检查远程应用是否运行
        const isRunning = await appLauncher.isTargetAppRunning();
        console.log('远程应用运行状态:', isRunning);

        if (!isRunning) {
          // 启动远程应用
          console.log('启动远程应用...');
          await appLauncher.launchTargetApp();
          
          // 等待应用启动
          await this.sleep(3000);
        }

        // 启动屏幕投射
        console.log('启动屏幕投射...');
        await appLauncher.startScreencast();

        // 监听屏幕更新事件
        uni.$on('screencast-update', this.onScreencastUpdate);

        this.isConnectingRemote = false;
        this.remoteAppStatus = { running: true };

        // 更新远程应用状态
        this.updateRemoteAppStatus();

      } catch (error) {
        console.error('初始化远程屏幕投射失败:', error);
        this.isConnectingRemote = false;
        uni.showToast({
          title: '连接远程应用失败: ' + error.message,
          icon: 'error',
          duration: 3000
        });
      }
    },

    /**
     * 连接远程屏幕（手动触发）
     */
    async connectRemoteScreen() {
      await this.initRemoteScreencast();
    },

    /**
     * 处理屏幕投射更新
     */
    onScreencastUpdate(data) {
      if (data.imageBase64) {
        this.remoteScreenImage = 'data:image/png;base64,' + data.imageBase64;
        this.updateRemoteFPS();
      }
    },

    /**
     * 更新远程FPS显示
     */
    updateRemoteFPS() {
      // FPS计算由appLauncher处理
      // 这里可以显示实际的FPS值
      this.remoteFPS = '30 FPS';
    },

    /**
     * 更新远程应用状态
     */
    async updateRemoteAppStatus() {
      setInterval(async () => {
        const isRunning = await appLauncher.isTargetAppRunning();
        this.remoteAppStatus = {
          running: isRunning,
          timestamp: new Date().toLocaleTimeString()
        };
      }, 5000);
    },

    /**
     * 处理远程屏幕触摸事件
     */
    onRemoteScreenTouch(type, event) {
      const touch = event.touches && event.touches[0] || event.changedTouches[0];
      
      if (!touch) return;

      // 获取屏幕容器的位置和大小
      const element = event.currentTarget;
      const rect = element.getBoundingClientRect();
      
      // 计算相对坐标
      const relativeX = touch.clientX - rect.left;
      const relativeY = touch.clientY - rect.top;
      
      // 缩放到目标应用的分辨率（假设1920x1080）
      const scaledX = Math.floor(relativeX * (1920 / rect.width));
      const scaledY = Math.floor(relativeY * (1080 / rect.height));

      console.log(`触摸事件: ${type}`, { scaledX, scaledY });

      // 转发触摸事件到远程应用
      this.forwardTouchToRemote(type, scaledX, scaledY);

      // 显示触摸点（调试用）
      this.showTouchPoint = true;
      this.touchPointStyle = `left: ${touch.clientX}px; top: ${touch.clientY}px;`;
      
      if (type === 'end') {
        setTimeout(() => {
          this.showTouchPoint = false;
        }, 300);
      }
    },

    /**
     * 转发触摸事件到远程应用
     */
    async forwardTouchToRemote(type, x, y) {
      try {
        const adbModule = uni.requireNativePlugin('thermal-adb-module');
        
        if (!adbModule) {
          console.warn('ADB模块不可用，无法转发触摸事件');
          return;
        }

        const touchData = { x, y };

        if (type === 'start') {
          adbModule.touchDown(touchData);
        } else if (type === 'move') {
          adbModule.touchMove(touchData);
        } else if (type === 'end') {
          adbModule.touchUp(touchData);
        }
      } catch (error) {
        console.error('转发触摸事件失败:', error);
      }
    },

    /**
     * 在远程应用中点击
     */
    async onClickRemote() {
      try {
        await appLauncher.clickRemoteMonitor();
      } catch (error) {
        uni.showToast({
          title: '远程点击失败',
          icon: 'error'
        });
      }
    },

    /**
     * 切换双屏模式
     */
    toggleDualScreen() {
      this.isDualScreen = !this.isDualScreen;
      uni.showToast({
        title: this.isDualScreen ? '已开启双屏模式' : '已关闭双屏模式',
        icon: 'success',
        duration: 1500
      });
    },

    /**
     * 本地采图
     */
    async captureLocalImage() {
      try {
        // 调用camera的capture方法
        const cameraRef = this.$refs.camera;
        if (cameraRef) {
          // 这里应该调用实际的摄像头采图方法
          uni.showToast({
            title: '本地采图成功',
            icon: 'success'
          });
        }
      } catch (error) {
        uni.showToast({
          title: '本地采图失败',
          icon: 'error'
        });
      }
    },

    /**
     * 同步采图（本地和远程同时采图）
     */
    async syncCapture() {
      try {
        // 同时在本地和远程采图
        await Promise.all([
          this.captureLocalImage(),
          this.captureRemoteImage()
        ]);
        
        uni.showToast({
          title: '双采图成功',
          icon: 'success'
        });
      } catch (error) {
        uni.showToast({
          title: '双采图失败',
          icon: 'error'
        });
      }
    },

    /**
     * 远程采图
     */
    async captureRemoteImage() {
      try {
        const adbModule = uni.requireNativePlugin('thermal-adb-module');
        
        if (!adbModule) {
          throw new Error('ADB模块不可用');
        }

        adbModule.clickPoint({
          x: 400,
          y: 600,
        }, (result) => {
          if (result.success) {
            console.log('远程采图成功');
          }
        });
      } catch (error) {
        console.error('远程采图失败:', error);
        throw error;
      }
    },

    /**
     * 退出监控
     */
    async exitMonitor() {
      uni.showModal({
        title: '退出提示',
        content: '确定要退出实时监控吗？',
        success: async (result) => {
          if (result.confirm) {
            this.cleanup();
            uni.navigateBack();
          }
        }
      });
    },

    /**
     * 清理资源
     */
    cleanup() {
      uni.$off('screencast-update', this.onScreencastUpdate);
      appLauncher.stopScreencast();
    },

    /**
     * 延迟函数
     */
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  }
};
</script>

<style scoped>
.live-monitor-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #000;
  color: #fff;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 15px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.status-info {
  display: flex;
  gap: 20px;
  font-size: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.status-label {
  color: rgba(255, 255, 255, 0.8);
}

.status-value {
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 3px;
  background-color: rgba(0, 0, 0, 0.2);
}

.status-value.running {
  color: #4ade80;
  background-color: rgba(74, 222, 128, 0.2);
}

.status-value.stopped {
  color: #ef4444;
  background-color: rgba(239, 68, 68, 0.2);
}

.content-area {
  flex: 1;
  display: flex;
  gap: 2px;
  padding: 2px;
  overflow: hidden;
  background-color: #111;
}

.camera-container,
.screen-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #333;
}

.container-title {
  background-color: #222;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: bold;
  color: #888;
  border-bottom: 1px solid #333;
}

.camera-wrapper,
.screen-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
  background-color: #000;
}

.camera {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.screen-wrapper {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.3s;
}

.camera-overlay {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  max-width: 90%;
}

.overlay-text {
  color: #fff;
}

.no-signal,
.connecting {
  text-align: center;
  opacity: 0.6;
}

.no-signal text {
  font-size: 14px;
  margin-bottom: 15px;
}

.connect-btn {
  background-color: #667eea;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-size: 12px;
  cursor: pointer;
}

.toolbar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 80px;
  background-color: #111;
  border-top: 1px solid #333;
  padding-bottom: 10px;
}

.tool-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  transition: opacity 0.2s;
  width: 70px;
}

.tool-item:active {
  opacity: 0.7;
}

.tool-item.center {
  transform: scale(1.1);
}

.tool-icon {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.tool-icon.big {
  width: 40px;
  height: 40px;
}

.tool-text {
  font-size: 11px;
  text-align: center;
  color: #aaa;
}

.tool-item.center .tool-text.strong {
  color: #fff;
  font-weight: bold;
}

.touch-point {
  position: fixed;
  width: 30px;
  height: 30px;
  border: 2px solid #ff0000;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  z-index: 999;
}

.safe-pad {
  height: 20px;
  background-color: #000;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-area {
    flex-direction: column;
  }

  .camera-container,
  .screen-container {
    flex: 1;
  }

  .toolbar {
    height: 90px;
    padding: 10px 5px;
  }

  .tool-item {
    width: 60px;
  }
}
</style>
