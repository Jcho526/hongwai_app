<template>
  <view class="container">
    <!-- 建议输入框 -->
    <view class="input-area">
      <textarea
        v-model="suggestion"
        placeholder="请输入您的建议"
        auto-height
        maxlength="-1"
        class="textarea"
      ></textarea>
    </view>

    <!-- 联系方式输入框 -->
    <view class="contact-area">
      <text class="label">联系方式：</text>
      <input
        v-model="contact"
        type="text"
        placeholder="输入您的手机号或邮箱等联系方式"
        class="contact-input"
      />
    </view>

    <!-- 提交按钮 -->
    <button class="submit-btn" @click="submitFeedback">
      提交
    </button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      suggestion: '',
      contact: ''
    };
  },
  methods: {
    submitFeedback() {
      if (!this.suggestion.trim()) {
        uni.showToast({
          title: '请填写建议内容',
          icon: 'none'
        });
        return;
      }
      if (!this.contact.trim()) {
        uni.showToast({
          title: '请输入联系方式',
          icon: 'none'
        });
        return;
      }

      // 模拟提交
      uni.showToast({
        title: '提交成功！',
        icon: 'success'
      });

      this.suggestion = '';
      this.contact = '';
    }
  }
}
</script>

<style scoped>
.container {
  background-color: #f5f5f5;
  padding: 30rpx;
  height: 100vh;
}

.input-area {
  padding: 40rpx;
  background-color: white;
  border-radius: 10rpx;
  margin-bottom: 30rpx;
}

.textarea {
  width: 100%;
  height: 400rpx;
  border: 1rpx solid #ccc;
  border-radius: 10rpx;
  padding: 20rpx;
  font-size: 32rpx;
  line-height: 1.5;
  background-color: #fafafa;
}

.contact-area {
  padding: 30rpx;
  background-color: white;
  border-radius: 10rpx;
  margin-bottom: 40rpx;
  display: flex;
  align-items: center;
}

.label {
  color: #e74c3c;
  font-size: 32rpx;
  margin-right: 10rpx;
}

.contact-input {
  flex: 1;
  height: 60rpx;
  border: 1rpx solid #ccc;
  border-radius: 10rpx;
  padding: 0 20rpx;
  font-size: 32rpx;
  background-color: #fafafa;
}

.submit-btn {
  width: 600rpx;
  height: 80rpx;
  background-color: #00c4b8;
  color: white;
  font-size: 36rpx;
  margin: 0 auto;
  border-radius: 40rpx;
  line-height: 80rpx;
  text-align: center;
}
</style>