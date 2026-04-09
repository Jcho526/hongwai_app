<template>
  <view class="login-container">
    <!-- 标题 -->
    <text class="title">红外热成像健康管理系统</text>

    <!-- 登录表单 -->
    <view class="form-box">
      <!-- 用户名 -->
      <view class="input-group">
        <text class="label">用户名</text>
        <view class="input-item">
          <image src="/static/icons/user.png" class="icon"></image>
          <input 
            type="text" 
            v-model="username" 
            placeholder="请输入3位及以上的用户名"
            maxlength="20"
          />
        </view>
      </view>

      <!-- 密码 -->
      <view class="input-group">
        <text class="label">密 码</text>
        <view class="input-item">
          <image src="/static/icons/user.png" class="icon"></image>
          <input 
            type="password" 
            v-model="password" 
            placeholder="请输入6位及以上的密码"
            maxlength="20"
          />
        </view>
      </view>

      <!-- 验证码 -->
      <view class="input-group">
        <text class="label">验证码</text>
        <view class="verify-box">
          <view class="calc">{{ calc }}</view>
          <input 
            type="number" 
            v-model="verifyCode" 
            placeholder="请输入验证码"
            maxlength="3"
          />
        </view>
      </view>

      <!-- 记住密码 & 忘记密码 -->
      <view class="remember-box">
        <view class="remember">
          <checkbox :checked="rememberMe" @change="rememberMe = !rememberMe" style="transform: scale(0.8); margin-right: 5px;" />
          <text>记住密码</text>
        </view>
        <text class="forgot-password" @click="goForgotPassword">忘记密码？</text>
      </view>

      <!-- 协议勾选 -->
      <view class="agreement">
        <radio :checked="agree" @change="agree = !agree" style="transform: scale(0.8); margin-right: 5px;" />
        <text>我已阅读 <text class="protocol-text">《用户协议》</text> 和 <text class="protocol-text">《隐私协议》</text></text>
      </view>

      <!-- 登录按钮 -->
      <button class="login-btn" :disabled="!canLogin" @click="login">登录</button>
    </view>
  </view>
</template>

<script>
import { loginByPassword } from "../../services/auth";

export default {
  data() {
    return {
      username: '',
      password: '',
      verifyCode: '',
      rememberMe: false,
      agree: false,
      calc: '8 - 5 = ?',
      correctAnswer: 0,
    }
  },
  computed: {
    // 移除所有验证逻辑，登录按钮始终可用
    canLogin() {
      return true;
    }
  },
  methods: {
    async login() {
      const username = String(this.username || "").trim();
      const password = String(this.password || "").trim();

      if (!username) {
        return uni.showToast({ title: "请输入用户名", icon: "none" });
      }
      if (!password) {
        return uni.showToast({ title: "请输入密码", icon: "none" });
      }

      try {
        await loginByPassword({ username, password });
        uni.showToast({ title: "登录成功", icon: "success" });
        uni.reLaunch({ url: "/pages/main/main" });
      } catch (e) {
        uni.showToast({ title: e.message || "登录失败", icon: "none" });
      }
    },
    goForgotPassword() {
      uni.navigateTo({
        url: '/pages/forgotPassword/forgotPassword'
      });
    },
    generateCalc() {
      let a = Math.floor(Math.random() * 10) + 1;
      let b = Math.floor(Math.random() * 10) + 1;
      let result = 0;
      let op = '';
      if (Math.random() > 0.5) {
        op = '+';
        result = a + b;
      } else {
        op = '-';
        if (a >= b) {
          result = a - b;
        } else {
          [a, b] = [b, a];
          result = a - b;
        }
      }

      this.calc = `${a} ${op} ${b} = ?`;
      this.correctAnswer = result;
    }
  },
  onLoad() {
    this.generateCalc();
  }
}
</script>
<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #00c4b8;
  padding: 20rpx;
}

.title {
  font-size: 40rpx;
  color: white;
  font-weight: bold;
  margin-bottom: 50rpx;
}

.form-box {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 30rpx;
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 30rpx;
  color: #fff;
  margin-bottom: 10rpx;
}

.input-item {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 15rpx;
  padding: 15rpx;
  box-shadow: 0 2rpx 5rpx rgba(0,0,0,0.1);
}

.icon {
  width: 30rpx;
  height: 30rpx;
  margin-right: 15rpx;
}

input {
  flex: 1;
  font-size: 30rpx;
  border: none;
  outline: none;
  background: transparent;
}

.verify-box {
  display: flex;
  gap: 20rpx;
}

.calc {
  background-color: white;
  border-radius: 15rpx;
  padding: 15rpx;
  font-size: 30rpx;
  text-align: center;
  width: 180rpx;
  box-shadow: 0 2rpx 5rpx rgba(0,0,0,0.1);
}

.remember-box {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
  font-size: 28rpx;
  color: white;
}

.forgot-password {
  color: #fff;
  text-decoration: underline;
}

.agreement {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
  font-size: 28rpx;
  color: white;
}

.protocol-text {
  color: red;
}

.login-btn {
  width: 100%;
  background-color: #009688;
  color: white;
  font-size: 32rpx;
  border-radius: 15rpx;
  padding: 20rpx;
  margin-top: 20rpx;
}
</style>