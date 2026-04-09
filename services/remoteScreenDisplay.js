/**
 * 远程屏幕投射组件
 * 用于在我们的App中显示目标应用的屏幕
 */

export default {
  name: 'RemoteScreenDisplay',
  props: {
    // 显示模式: 'embedded'(嵌入式) 或 'fullscreen'(全屏)
    mode: {
      type: String,
      default: 'embedded'
    },
    // 是否启用触摸控制转发
    enableTouchForward: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      screenImage: null,
      isLoading: false,
      error: null,
      touchStartX: 0,
      touchStartY: 0,
      fps: 0,
      fpsCounter: 0,
      lastFpsTime: 0,
      isScreencastActive: false,
    };
  },
  computed: {
    displayStyle() {
      if (this.mode === 'fullscreen') {
        return 'width: 100%; height: 100%;';
      }
      return 'width: 100%; height: 500px;';
    }
  },
  mounted() {
    this.initScreencast();
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    /**
     * 初始化屏幕投射
     */
    async initScreencast() {
      try {
        this.isLoading = true;
        
        // 监听屏幕更新事件
        uni.$on('screencast-update', this.onScreencastUpdate);
        
        this.isScreencastActive = true;
        this.isLoading = false;
      } catch (error) {
        this.error = error.message;
        this.isLoading = false;
      }
    },

    /**
     * 处理屏幕投射更新
     */
    onScreencastUpdate(data) {
      if (data.imageBase64) {
        // 更新图像
        this.screenImage = 'data:image/png;base64,' + data.imageBase64;
        this.updateFPS();
      } else if (data.streamData) {
        // 处理流数据（如WebRTC）
        this.handleStreamData(data.streamData);
      }
    },

    /**
     * 处理流数据
     */
    handleStreamData(streamData) {
      // 这里处理WebRTC或其他流格式的数据
      // 可以使用HTML5 Canvas或video标签进行解码
      console.log('处理流数据:', streamData);
    },

    /**
     * 更新FPS计数
     */
    updateFPS() {
      this.fpsCounter++;
      const now = Date.now();
      
      if (now - this.lastFpsTime >= 1000) {
        this.fps = this.fpsCounter;
        this.fpsCounter = 0;
        this.lastFpsTime = now;
      }
    },

    /**
     * 处理触摸事件（转发到目标应用）
     */
    onTouchStart(event) {
      if (!this.enableTouchForward || !this.isScreencastActive) return;
      
      const touch = event.touches[0];
      this.touchStartX = touch.clientX;
      this.touchStartY = touch.clientY;
      
      this.forwardTouchToRemote('start', touch.clientX, touch.clientY);
    },

    onTouchMove(event) {
      if (!this.enableTouchForward || !this.isScreencastActive) return;
      
      const touch = event.touches[0];
      this.forwardTouchToRemote('move', touch.clientX, touch.clientY);
    },

    onTouchEnd(event) {
      if (!this.enableTouchForward || !this.isScreencastActive) return;
      
      const touch = event.changedTouches[0];
      this.forwardTouchToRemote('end', touch.clientX, touch.clientY);
    },

    /**
     * 将触摸事件转发到远程应用
     */
    forwardTouchToRemote(type, x, y) {
      try {
        // 缩放坐标到目标应用的分辨率
        const scaledX = Math.floor(x * (1920 / this.$el.offsetWidth));
        const scaledY = Math.floor(y * (1080 / this.$el.offsetHeight));
        
        const adbModule = uni.requireNativePlugin('thermal-adb-module');
        
        if (adbModule && type === 'start') {
          adbModule.touchDown({
            x: scaledX,
            y: scaledY,
          });
        } else if (adbModule && type === 'move') {
          adbModule.touchMove({
            x: scaledX,
            y: scaledY,
          });
        } else if (adbModule && type === 'end') {
          adbModule.touchUp({
            x: scaledX,
            y: scaledY,
          });
        }
      } catch (error) {
        console.error('触摸转发失败:', error);
      }
    },

    /**
     * 清理资源
     */
    cleanup() {
      uni.$off('screencast-update', this.onScreencastUpdate);
      this.isScreencastActive = false;
    }
  }
};
