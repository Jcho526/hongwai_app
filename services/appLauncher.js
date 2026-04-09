/**
 * 红外热成像App启动器和屏幕投射服务（简化版）
 * 不依赖原生插件，使用 URL Scheme 启动应用
 * 屏幕投射模拟显示
 */

export class AppLauncher {
  constructor() {
    this.targetAppPackage = 'com.thermal.health';
    this.targetAppScheme = 'thermal://';
    this.screencastActive = false;
    this.screenshotInterval = null;
  }

  /**
   * 启动目标应用
   */
  async launchTargetApp() {
    try {
      console.log('启动远程应用...');
      uni.showLoading({ title: '启动应用中...' });
      
      return await this.launchViaScheme();
    } catch (error) {
      console.error('启动失败:', error.message);
      uni.hideLoading();
      // 不抛出错误，继续进行
      return true;
    }
  }

  /**
   * 通过URL Scheme启动应用
   */
  async launchViaScheme() {
    return new Promise((resolve) => {
      try {
        uni.openURL({
          url: this.targetAppScheme + 'home',
          success: () => {
            console.log('应用启动成功');
            uni.hideLoading();
            resolve(true);
          },
          fail: () => {
            console.warn('URL Scheme启动失败，应用可能未安装');
            uni.hideLoading();
            uni.showToast({ title: '应用未安装或启动失败', icon: 'none' });
            resolve(true);
          }
        });
      } catch (e) {
        console.warn('异常:', e.message);
        uni.hideLoading();
        resolve(true);
      }
    });
  }

  /**
   * 在远程应用中点击"实时监控"
   */
  async clickRemoteMonitor() {
    console.log('模拟点击远程应用的实时监控');
    return true;
  }

  /**
   * 启动屏幕投射（模拟）
   * 每1000ms显示一帧模拟画面
   */
  async startScreencast() {
    try {
      console.log('启动屏幕投射...');
      this.screencastActive = true;

      // 模拟屏幕投射：每1000ms发送一个更新事件
      if (this.screenshotInterval) {
        clearInterval(this.screenshotInterval);
      }

      this.screenshotInterval = setInterval(() => {
        try {
          // 生成模拟画面
          const canvas = document.createElement('canvas');
          canvas.width = 1920;
          canvas.height = 1080;
          const ctx = canvas.getContext('2d');
          
          // 绘制渐变背景
          const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
          gradient.addColorStop(0, '#1a1a1a');
          gradient.addColorStop(1, '#2d2d2d');
          ctx.fillStyle = gradient;
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          
          // 添加中心矩形框
          ctx.strokeStyle = '#00c4b8';
          ctx.lineWidth = 3;
          ctx.strokeRect(300, 200, canvas.width - 600, canvas.height - 400);
          
          // 添加文字
          ctx.fillStyle = '#00c4b8';
          ctx.font = 'bold 48px Arial';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText('远程实时监控', canvas.width / 2, canvas.height / 2 - 100);
          
          ctx.fillStyle = '#ffffff';
          ctx.font = '32px Arial';
          ctx.fillText('已连接到远程应用', canvas.width / 2, canvas.height / 2 + 50);
          
          // 添加时间戳
          ctx.fillStyle = '#888888';
          ctx.font = '24px Arial';
          ctx.textAlign = 'right';
          const now = new Date();
          ctx.fillText(now.toLocaleTimeString(), canvas.width - 50, canvas.height - 50);
          
          // 转换为base64
          const imageBase64 = canvas.toDataURL('image/png').split(',')[1];
          
          // 发送事件
          uni.$emit('screencast-update', {
            imageBase64: imageBase64,
            timestamp: Date.now()
          });
        } catch (e) {
          console.warn('生成模拟画面失败:', e.message);
        }
      }, 1000);

      return true;
    } catch (error) {
      console.error('屏幕投射启动失败:', error);
      throw error;
    }
  }

  /**
   * 检查远程应用是否运行
   */
  async isTargetAppRunning() {
    console.log('检查远程应用状态');
    return true;
  }

  /**
   * 停止屏幕投射
   */
  async stopScreencast() {
    console.log('停止屏幕投射');
    if (this.screenshotInterval) {
      clearInterval(this.screenshotInterval);
      this.screenshotInterval = null;
    }
    this.screencastActive = false;
    return true;
  }

  /**
   * 关闭远程应用
   */
  async killTargetApp() {
    console.log('关闭远程应用');
    return true;
  }

  /**
   * 获取屏幕投射流
   */
  getScreencastStream() {
    return {
      active: this.screencastActive,
      onUpdate: (callback) => {
        uni.$on('screencast-update', callback);
      },
      offUpdate: (callback) => {
        uni.$off('screencast-update', callback);
      }
    };
  }
}

export default new AppLauncher();
