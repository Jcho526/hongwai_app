# 🔧 App启动器 - 技术实现指南

## 快速开始

### 1. 安装依赖

```bash
# 在项目根目录执行
cd c:\Users\1\Desktop\新

# 如果使用npm
npm install

# 如果使用yarn
yarn install
```

### 2. 导入服务

在你的Vue组件中：

```javascript
import appLauncher from '../../services/appLauncher';

export default {
  methods: {
    async startRemoteApp() {
      try {
        // 启动远程应用
        await appLauncher.launchTargetApp();
        
        // 启动屏幕投射
        await appLauncher.startScreencast();
      } catch (error) {
        console.error('启动失败:', error);
      }
    }
  }
}
```

### 3. 使用远程屏幕显示

```vue
<template>
  <view class="app-container">
    <!-- 远程屏幕显示区域 -->
    <view 
      class="remote-screen"
      :style="{ backgroundImage: `url(${remoteScreenImage})` }"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
    </view>
  </view>
</template>

<script>
import appLauncher from '../../services/appLauncher';

export default {
  data() {
    return {
      remoteScreenImage: null
    };
  },
  mounted() {
    // 监听屏幕更新
    uni.$on('screencast-update', (data) => {
      if (data.imageBase64) {
        this.remoteScreenImage = 'data:image/png;base64,' + data.imageBase64;
      }
    });
  }
}
</script>
```

---

## 核心API文档

### appLauncher.launchTargetApp()

**功能**：启动目标应用并自动登录

**语法**：
```javascript
await appLauncher.launchTargetApp();
```

**返回值**：Promise<boolean>

**示例**：
```javascript
try {
  const result = await appLauncher.launchTargetApp();
  console.log('应用启动成功');
} catch (error) {
  console.error('启动失败:', error.message);
}
```

**内部流程**：
1. 检查ADB可用性
2. 通过ADB或Deep Link启动应用
3. 等待3秒（应用加载）
4. 自动点击"同意"按钮
5. 自动点击"登录"按钮
6. 等待2秒（登录完成）

---

### appLauncher.startScreencast()

**功能**：启动屏幕投射

**语法**：
```javascript
await appLauncher.startScreencast();
```

**返回值**：Promise<boolean>

**优先级**：
1. WebRTC (最佳)
2. ADB截屏轮询 (良好)
3. 摄像头直播 (可用)

**事件监听**：
```javascript
uni.$on('screencast-update', (data) => {
  // data.imageBase64 - 截屏的base64编码
  // data.timestamp - 更新时间戳
});
```

---

### appLauncher.clickRemoteMonitor()

**功能**：在远程应用中点击"实时监控"按钮

**语法**：
```javascript
await appLauncher.clickRemoteMonitor();
```

---

### appLauncher.isTargetAppRunning()

**功能**：检查目标应用是否在运行

**语法**：
```javascript
const isRunning = await appLauncher.isTargetAppRunning();
if (isRunning) {
  console.log('应用正在运行');
}
```

**返回值**：Promise<boolean>

---

### appLauncher.stopScreencast()

**功能**：停止屏幕投射

**语法**：
```javascript
await appLauncher.stopScreencast();
```

---

### appLauncher.killTargetApp()

**功能**：关闭目标应用

**语法**：
```javascript
await appLauncher.killTargetApp();
```

---

## 事件系统

### screencast-update 事件

**触发频率**：每500ms（ADB方案）或实时（WebRTC方案）

**事件数据**：
```javascript
{
  imageBase64: '...',  // 截屏的base64编码
  timestamp: 1234567890,  // 时间戳（毫秒）
  streamData: null  // WebRTC流数据
}
```

**监听示例**：
```javascript
uni.$on('screencast-update', (data) => {
  console.log('收到屏幕更新:', data);
  this.updateScreenDisplay(data.imageBase64);
});

// 清理监听
uni.$off('screencast-update', handler);
```

---

## 配置说明

### 修改目标应用信息

编辑 `services/appLauncher.js` 第8-9行：

```javascript
this.targetAppPackage = 'com.thermal.health';  // ← 包名
this.targetAppActivity = 'com.thermal.health.LoginActivity';  // ← Activity
```

### 修改自动点击的坐标

ADB方案依赖屏幕坐标，需要根据实际应用界面调整：

```javascript
// autoClickAgree() 方法中
adbModule.clickPoint({
  x: 100,  // ← 根据实际界面调整
  y: 600   // ← 根据实际界面调整
}, callback);

// autoClickLogin() 方法中
adbModule.clickPoint({
  x: 400,  // ← 根据实际界面调整
  y: 700   // ← 根据实际界面调整
}, callback);
```

**获取正确坐标的方法**：
1. 使用ADB命令截屏：`adb shell screencap -p /sdcard/screen.png`
2. 用图像编辑器打开，测量按钮位置
3. 或使用Android开发者工具查看层级

---

## 高级功能

### 自定义登录流程

```javascript
// 如果默认的自动登录不工作，可以自定义
async customAutoLogin() {
  const adbModule = uni.requireNativePlugin('thermal-adb-module');
  
  // 1. 输入验证码（假设有输入框）
  adbModule.clickPoint({ x: 200, y: 500 });  // 点击验证码输入框
  await this.sleep(300);
  
  adbModule.inputText({
    text: '123'  // 输入验证码
  });
  
  // 2. 勾选同意
  adbModule.clickPoint({ x: 100, y: 600 });
  
  // 3. 点击登录
  adbModule.clickPoint({ x: 400, y: 700 });
}
```

### 监控远程应用状态

```javascript
// 定期检查应用状态
setInterval(async () => {
  const isRunning = await appLauncher.isTargetAppRunning();
  if (!isRunning) {
    console.warn('远程应用已停止，自动重启');
    await appLauncher.launchTargetApp();
  }
}, 10000);  // 每10秒检查一次
```

### 触摸事件的高级处理

```javascript
// 计算精确的触摸坐标
function calculateTouchCoordinates(event, containerElement) {
  const touch = event.touches[0];
  const rect = containerElement.getBoundingClientRect();
  
  // 容器内的相对坐标
  const relativeX = touch.clientX - rect.left;
  const relativeY = touch.clientY - rect.top;
  
  // 缩放到目标分辨率
  const targetWidth = 1920;
  const targetHeight = 1080;
  
  const scaledX = Math.floor(relativeX * (targetWidth / rect.width));
  const scaledY = Math.floor(relativeY * (targetHeight / rect.height));
  
  return { scaledX, scaledY };
}
```

---

## 故障排查

### 调试模式

启用详细日志：

```javascript
// 在appLauncher.js文件开头添加
const DEBUG = true;

function log(message, data = null) {
  if (DEBUG) {
    console.log(`[AppLauncher] ${message}`, data || '');
  }
}

// 使用log函数代替console.log
log('启动应用中...');
```

### 常见错误及解决方案

#### 错误1：ADB模块未找到

```
Error: ADB模块未找到，请确保已安装原生插件
```

**解决方案**：
1. 确认已在 `plugin.json` 中声明ADB插件
2. 确认ADB插件已正确安装
3. 重新编译项目

```bash
# 重新编译
npm run build

# 或使用HBuilderX重新编译项目
```

#### 错误2：应用启动失败

```
Error: launchApp failed: {error}
```

**解决方案**：
1. 检查包名是否正确
2. 确认应用已安装在设备上
3. 检查ADB连接状态

```bash
# 列出已安装的应用
adb shell pm list packages | grep thermal

# 测试启动应用
adb shell am start -n com.thermal.health/.LoginActivity
```

#### 错误3：屏幕投射不工作

```
Error: 屏幕投射启动失败
```

**解决方案**：
1. 确认目标应用已进入摄像头界面
2. 增加启动延迟

```javascript
// 增加等待时间
await this.sleep(5000);  // 改为5秒
await appLauncher.startScreencast();
```

3. 检查截屏权限

```bash
# 检查权限
adb shell pm dump com.thermal.health | grep android.permission.
```

### 性能优化

#### 降低屏幕投射的资源占用

```javascript
// 在startScreencastADB()中修改刷新间隔
this.screenshotInterval = setInterval(() => {
  // ...
}, 1000);  // 改为1000ms（每秒一次）而不是500ms
```

#### 压缩截屏图像

```javascript
// 在处理imageBase64时压缩
onScreencastUpdate(data) {
  if (data.imageBase64) {
    // 压缩base64图像
    const compressed = compressImage(data.imageBase64);
    this.screenImage = 'data:image/png;base64,' + compressed;
  }
}

function compressImage(base64) {
  // 使用canvas压缩
  const img = new Image();
  img.src = 'data:image/png;base64,' + base64;
  
  const canvas = document.createElement('canvas');
  canvas.width = img.width * 0.8;  // 缩小20%
  canvas.height = img.height * 0.8;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  
  return canvas.toDataURL('image/png').split(',')[1];
}
```

---

## 测试步骤

### 集成测试

```javascript
// test-appLauncher.js
async function testAppLauncher() {
  try {
    // 测试1：启动应用
    console.log('测试1：启动应用');
    await appLauncher.launchTargetApp();
    await sleep(5000);
    
    // 测试2：检查应用状态
    console.log('测试2：检查应用状态');
    const isRunning = await appLauncher.isTargetAppRunning();
    console.assert(isRunning, '应用应该在运行');
    
    // 测试3：启动屏幕投射
    console.log('测试3：启动屏幕投射');
    await appLauncher.startScreencast();
    await sleep(2000);
    
    // 测试4：模拟触摸
    console.log('测试4：模拟触摸');
    await appLauncher.clickRemoteMonitor();
    
    // 测试5：停止屏幕投射
    console.log('测试5：停止屏幕投射');
    await appLauncher.stopScreencast();
    
    console.log('✅ 所有测试通过');
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### 在平板上测试

1. 连接平板到电脑（USB调试模式）
2. 打开应用
3. 导航到实时监控页面
4. 观察：
   - ✅ 远程应用是否自动启动
   - ✅ 是否自动登录
   - ✅ 屏幕是否投射成功
   - ✅ 触摸事件是否转发

---

## 原生模块的Java实现示例

### ThermalAdbModule.kt

```kotlin
package com.thermal.adb

import android.content.Context
import io.dcloud.feature.uniapp.annotation.UniJSMethod
import io.dcloud.feature.uniapp.common.UniModule

class ThermalAdbModule(context: Context) : UniModule(context) {
    
    private val adbBridge = AdbBridge()
    
    @UniJSMethod(uiThread = false)
    fun launchApp(options: JSONObject, callback: UniCallback) {
        val packageName = options.getString("packageName")
        val activity = options.getString("activity")
        
        try {
            adbBridge.launchApp(packageName, activity)
            
            val result = JSONObject()
            result.put("success", true)
            callback.invoke(result)
        } catch (e: Exception) {
            val result = JSONObject()
            result.put("success", false)
            result.put("error", e.message)
            callback.invoke(result)
        }
    }
    
    @UniJSMethod(uiThread = false)
    fun clickPoint(options: JSONObject, callback: UniCallback) {
        val x = options.getInt("x")
        val y = options.getInt("y")
        
        try {
            adbBridge.clickPoint(x, y)
            
            val result = JSONObject()
            result.put("success", true)
            callback.invoke(result)
        } catch (e: Exception) {
            val result = JSONObject()
            result.put("success", false)
            result.put("error", e.message)
            callback.invoke(result)
        }
    }
    
    @UniJSMethod(uiThread = false)
    fun takeScreenshot(options: JSONObject, callback: UniCallback) {
        val packageName = options.getString("packageName")
        
        try {
            val base64 = adbBridge.takeScreenshot()
            
            val result = JSONObject()
            result.put("success", true)
            result.put("imageBase64", base64)
            callback.invoke(result)
        } catch (e: Exception) {
            val result = JSONObject()
            result.put("success", false)
            result.put("error", e.message)
            callback.invoke(result)
        }
    }
    
    // ... 其他方法
}
```

---

## 常见问题FAQ

**Q: 为什么屏幕投射延迟这么高？**  
A: ADB截屏方案每500ms更新一次，延迟约200-500ms。可以使用WebRTC方案获得更低延迟。

**Q: 如何自定义自动登录的流程？**  
A: 修改 `autoClickAgree()` 和 `autoClickLogin()` 方法，调整坐标或添加额外的点击步骤。

**Q: 支持多个远程应用同时投射吗？**  
A: 当前不支持，可扩展 `appLauncher.js` 来支持多个应用配置。

**Q: 如何在后台保持屏幕投射？**  
A: 使用 `isBackground: true` 的后台任务，定期更新屏幕。

**Q: 触摸事件的坐标如何精确对应？**  
A: 根据远程应用的实际分辨率动态计算缩放比例。

---

## 参考资源

- [UniApp API文档](https://uniapp.dcloud.io/api/README)
- [Android ADB命令参考](https://developer.android.com/studio/command-line/adb)
- [UniApp原生插件开发](https://nativesupport.dcloud.net.cn/)
- [WebRTC API](https://webrtc.org/getting-started/overview)

---

**版本**: v1.0  
**最后更新**: 2026年3月22日
