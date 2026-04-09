# 📋 实施清单与配置指南

## ✅ 完整集成检查清单

### 第一阶段：基础配置（0.5小时）

- [ ] 1.1 确认远程App的实际包名
  ```bash
  # 在平板上运行此命令
  adb shell pm list packages | grep -i thermal
  ```

- [ ] 1.2 确认远程App的主Activity
  ```bash
  adb shell dumpsys package com.thermal.health | grep -A 1 "android.intent.action.MAIN"
  ```

- [ ] 1.3 修改 `services/appLauncher.js` 中的包名和Activity
  ```javascript
  this.targetAppPackage = 'actual.package.name';
  this.targetAppActivity = 'actual.package.name.MainActivity';
  ```

- [ ] 1.4 测试ADB连接
  ```bash
  adb devices
  ```

### 第二阶段：UI集成（1小时）

- [ ] 2.1 确认 `pages/capture/liveMonitor.vue` 已创建
  ```bash
  ls -la pages/capture/liveMonitor.vue
  ```

- [ ] 2.2 在 `pages.json` 中注册新页面
  ```json
  {
    "path": "pages/capture/liveMonitor",
    "style": {
      "navigationStyle": "custom"
    }
  }
  ```

- [ ] 2.3 修改 `pages/main/main.vue` 中的 `goToLive()` 方法
  ```javascript
  goToLive() {
    uni.navigateTo({
      url: '/pages/capture/liveMonitor'
    });
  }
  ```

- [ ] 2.4 测试导航
  - 登录应用 → 进入主菜单 → 点击"实时监控" → 应该进入新页面

### 第三阶段：自动启动测试（1小时）

- [ ] 3.1 测试launchTargetApp()函数
  ```javascript
  // 在浏览器控制台或App中运行
  import appLauncher from './services/appLauncher';
  await appLauncher.launchTargetApp();
  ```

- [ ] 3.2 观察：
  - [ ] 远程App是否启动了？
  - [ ] 是否自动勾选了同意按钮？
  - [ ] 是否自动点击了登录按钮？

- [ ] 3.3 如果自动点击不工作，调整坐标
  ```javascript
  // 使用ADB获取屏幕尺寸
  adb shell wm size
  
  // 截屏查看具体位置
  adb shell screencap -p /sdcard/screen.png
  adb pull /sdcard/screen.png
  ```

### 第四阶段：屏幕投射测试（1.5小时）

- [ ] 4.1 测试startScreencast()函数
  ```javascript
  await appLauncher.startScreencast();
  ```

- [ ] 4.2 观察：
  - [ ] 右侧是否显示了远程应用的屏幕？
  - [ ] 屏幕是否定期更新？
  - [ ] 是否能看到FPS显示？

- [ ] 4.3 如果不工作，检查：
  ```bash
  # 检查截屏权限
  adb shell pm dump com.thermal.health | grep SCREENSHOT
  
  # 或者尝试WebRTC方案（需要信令服务器）
  ```

### 第五阶段：触摸转发测试（1小时）

- [ ] 5.1 在右侧屏幕上点击
  - [ ] 是否在屏幕上看到红点标记？
  - [ ] 远程应用是否响应了点击？

- [ ] 5.2 如果触摸不响应，调整坐标缩放
  ```javascript
  // 在remoteScreenDisplay.js或liveMonitor.vue中
  // 获取实际的远程分辨率
  const actualRemoteWidth = 1080;  // 改为实际值
  const actualRemoteHeight = 1920; // 改为实际值
  ```

### 第六阶段：完整流程测试（2小时）

- [ ] 6.1 完整流程测试
  ```
  1. 打开我们的App
  2. 登录
  3. 进入主菜单
  4. 点击"实时监控"
  5. 等待页面加载
  6. 观察：
     ✓ 左侧显示本地摄像头
     ✓ 右侧显示远程应用的屏幕
     ✓ 远程App已自动启动和登录
  7. 在右侧屏幕上点击"实时监控"按钮
  8. 观察远程App进入实时监控页面
  9. 在左侧采图，观察数据
  ```

- [ ] 6.2 记录任何问题并调整

- [ ] 6.3 在多个平板上测试以确保兼容性

### 第七阶段：性能优化（1小时）

- [ ] 7.1 监控资源占用
  ```bash
  adb shell dumpsys meminfo com.thermal.health
  adb shell top -n 1
  ```

- [ ] 7.2 如果资源占用过高，调整：
  - 增加截屏间隔（减少帧率）
  - 压缩截屏图像质量
  - 限制内存缓存

- [ ] 7.3 测试长时间运行（至少30分钟）
  - 观察是否有内存泄漏
  - 观察屏幕投射是否仍然流畅

### 第八阶段：错误处理（1小时）

- [ ] 8.1 测试异常情况
  - [ ] 远程App崩溃时是否自动重启？
  - [ ] 网络断开时是否有错误提示？
  - [ ] 权限不足时是否有友好提示？

- [ ] 8.2 增加错误恢复机制
  ```javascript
  // 自动重启失败的组件
  setInterval(async () => {
    const isRunning = await appLauncher.isTargetAppRunning();
    if (!isRunning) {
      console.log('远程App已停止，自动重启');
      await appLauncher.launchTargetApp();
    }
  }, 30000);  // 每30秒检查一次
  ```

---

## 🔧 配置文件示例

### pages.json 配置

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "红外热成像健康管理系统"
      }
    },
    {
      "path": "pages/main/main",
      "style": {
        "navigationBarTitleText": ""
      }
    },
    {
      "path": "pages/capture/capture",
      "style": {
        "navigationStyle": "custom"
      }
    },
    {
      "path": "pages/capture/liveMonitor",
      "style": {
        "navigationStyle": "custom"
      }
    },
    {
      "path": "pages/capture/captureList",
      "style": {
        "navigationStyle": "custom"
      }
    },
    {
      "path": "pages/capture/capturePreview",
      "style": {
        "navigationStyle": "custom"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "uni-app",
    "navigationBarBackgroundColor": "#F8F8F8",
    "backgroundColor": "#FFFFFF"
  }
}
```

### main.vue 配置示例

```vue
<script>
export default {
  methods: {
    goToLive() {
      // ✨ 新的实时监控页面（支持双屏和远程投射）
      uni.navigateTo({
        url: '/pages/capture/liveMonitor'
      });
      
      // 可选：旧的采图页面（仅本地摄像头）
      // uni.navigateTo({
      //   url: '/pages/capture/capture'
      // });
    },
    
    goRecordManage() {
      uni.navigateTo({
        url: '/pages/photoRecords/photoRecords'
      });
    }
  }
}
</script>
```

### appLauncher.js 配置示例

```javascript
export class AppLauncher {
  constructor() {
    // ⚙️ 需要修改以下配置
    this.targetAppPackage = 'com.example.thermalhealth';  // ← 改为实际包名
    this.targetAppActivity = 'com.example.thermalhealth.MainActivity';  // ← 改为实际Activity
    
    // 屏幕分辨率（根据实际调整）
    this.remoteScreenWidth = 1920;
    this.remoteScreenHeight = 1080;
    
    // 自动点击的坐标（需要根据UI调整）
    this.agreeButtonX = 100;
    this.agreeButtonY = 600;
    this.loginButtonX = 400;
    this.loginButtonY = 700;
    this.monitorButtonX = 400;
    this.monitorButtonY = 600;
    
    // 截屏间隔（毫秒）
    this.screenshotInterval = 500;  // 500ms = 2fps
    
    // WebRTC信令服务器（可选）
    this.signalServerUrl = 'wss://your-server.com:8443';
    
    this.adbConnected = false;
    this.screencastActive = false;
    this.wsConnection = null;
  }
  
  // ... 其他代码
}
```

---

## 📱 不同分辨率的屏幕坐标调整

### 获取正确坐标的步骤

```bash
# 1. 获取平板的屏幕分辨率
adb shell wm size

# 输出示例:
# Physical size: 1920x1200
# OR
# Physical size: 2560x1600

# 2. 截屏
adb shell screencap -p /sdcard/screenshot.png

# 3. 拉取截图到电脑
adb pull /sdcard/screenshot.png

# 4. 用图像编辑器打开，测量UI元素的坐标
```

### 常见分辨率的坐标参考

#### 1920x1200 (10英寸平板)

```javascript
{
  agreeButtonX: 100,      // 左侧
  agreeButtonY: 600,      // 中间略下
  loginButtonX: 400,      // 中心
  loginButtonY: 700,      // 下方
  monitorButtonX: 400,    // 中心
  monitorButtonY: 600     // 中间
}
```

#### 2560x1600 (大平板)

```javascript
{
  agreeButtonX: 150,      // 左侧
  agreeButtonY: 800,      // 中间略下
  loginButtonX: 500,      // 中心
  loginButtonY: 950,      // 下方
  monitorButtonX: 500,    // 中心
  monitorButtonY: 800     // 中间
}
```

#### 1080x1920 (手机竖屏)

```javascript
{
  agreeButtonX: 50,       // 左侧
  agreeButtonY: 1000,     // 中间略下
  loginButtonX: 200,      // 中心
  loginButtonY: 1200,     // 下方
  monitorButtonX: 200,    // 中心
  monitorButtonY: 1000    // 中间
}
```

---

## 🧪 测试脚本示例

### 自动化测试脚本

```javascript
// tests/testAppLauncher.js

import appLauncher from '../services/appLauncher';

class AppLauncherTests {
  constructor() {
    this.passed = 0;
    this.failed = 0;
  }

  async assert(condition, message) {
    if (condition) {
      console.log(`✅ ${message}`);
      this.passed++;
    } else {
      console.error(`❌ ${message}`);
      this.failed++;
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async test1_LaunchApp() {
    console.log('\n📝 测试1：启动应用');
    try {
      await appLauncher.launchTargetApp();
      await this.sleep(5000);
      
      const isRunning = await appLauncher.isTargetAppRunning();
      await this.assert(isRunning, '应用应该在运行');
    } catch (error) {
      await this.assert(false, `启动应用异常: ${error.message}`);
    }
  }

  async test2_Screencast() {
    console.log('\n📝 测试2：屏幕投射');
    try {
      await appLauncher.startScreencast();
      await this.sleep(2000);
      
      // 监听屏幕更新
      let updateReceived = false;
      const handler = () => {
        updateReceived = true;
      };
      uni.$on('screencast-update', handler);
      
      await this.sleep(1000);
      uni.$off('screencast-update', handler);
      
      await this.assert(updateReceived, '应该收到屏幕更新事件');
    } catch (error) {
      await this.assert(false, `屏幕投射异常: ${error.message}`);
    }
  }

  async test3_ClickRemote() {
    console.log('\n📝 测试3：远程点击');
    try {
      await appLauncher.clickRemoteMonitor();
      await this.assert(true, '远程点击成功');
    } catch (error) {
      await this.assert(false, `远程点击异常: ${error.message}`);
    }
  }

  async test4_StopScreencast() {
    console.log('\n📝 测试4：停止投射');
    try {
      await appLauncher.stopScreencast();
      await this.assert(true, '停止投射成功');
    } catch (error) {
      await this.assert(false, `停止投射异常: ${error.message}`);
    }
  }

  async runAll() {
    console.log('🚀 开始运行测试套件...\n');
    
    await this.test1_LaunchApp();
    await this.test2_Screencast();
    await this.test3_ClickRemote();
    await this.test4_StopScreencast();
    
    console.log(`\n\n📊 测试结果:`);
    console.log(`✅ 通过: ${this.passed}`);
    console.log(`❌ 失败: ${this.failed}`);
    console.log(`总计: ${this.passed + this.failed}`);
  }
}

// 运行测试
const tests = new AppLauncherTests();
await tests.runAll();
```

### 运行测试

```bash
# 使用Node.js运行
node tests/testAppLauncher.js

# 或在Uni-app开发者工具中运行
# 在控制台执行上述代码
```

---

## 🎯 性能基准

### 预期的性能指标

| 指标 | 基准值 | 目标值 |
|------|--------|--------|
| 应用启动时间 | 3-5秒 | <5秒 ✅ |
| 自动登录时间 | 3-5秒 | <5秒 ✅ |
| 屏幕投射首帧延迟 | 1-2秒 | <2秒 ✅ |
| 屏幕投射帧率 | 2fps (500ms) | ≥2fps ✅ |
| 屏幕投射延迟 | 500-800ms | <1秒 |
| 触摸转发延迟 | 50-200ms | <200ms ✅ |
| 内存占用 | 100-200MB | <300MB ✅ |
| CPU占用 | 5-15% | <25% ✅ |

### 性能监控代码

```javascript
// 监控屏幕投射的帧率
let frameCount = 0;
let lastTime = Date.now();
let fps = 0;

uni.$on('screencast-update', () => {
  frameCount++;
  const now = Date.now();
  
  if (now - lastTime >= 1000) {
    fps = frameCount;
    console.log(`屏幕投射FPS: ${fps}`);
    frameCount = 0;
    lastTime = now;
  }
});

// 监控内存使用
setInterval(() => {
  const memInfo = uni.getMemoryInfo?.();
  if (memInfo) {
    console.log(`内存使用: ${(memInfo.currentMemoryUsage / 1024 / 1024).toFixed(2)}MB`);
  }
}, 5000);
```

---

## 📞 故障排查流程图

```
问题：屏幕没有投射
├─ 是否看到错误信息？
│  ├─ 是 → 检查错误日志 → 查看故障排查章节
│  └─ 否 → 继续
├─ 检查远程App是否运行
│  ├─ 否 → 检查启动是否失败
│  └─ 是 → 继续
├─ 检查截屏权限
│  ├─ 无权限 → 在AndroidManifest.xml中添加权限
│  └─ 有权限 → 继续
├─ 检查ADB连接
│  ├─ 未连接 → 重新连接设备
│  └─ 已连接 → 继续
└─ 尝试增加启动延迟
   ├─ 延迟5秒后重试
   └─ 仍未解决 → 联系支持
```

---

## 📚 相关文档链接

- [APP_LAUNCHER_INTEGRATION.md](./APP_LAUNCHER_INTEGRATION.md) - 集成方案总览
- [TECHNICAL_IMPLEMENTATION.md](./TECHNICAL_IMPLEMENTATION.md) - 技术实现指南
- [CHECKLIST.md](../CHECKLIST.md) - 项目检查清单

---

**最后更新**: 2026年3月22日  
**版本**: v1.0  
**适用于**: 红外热成像健康管理系统 v1.0+
