<template>
  <div class="login-container">
    <a-card class="login-card" title="管理员登录">
      <!-- 用户名输入框 -->
      <a-form :model="formState" @finish="handleLogin">
        <a-form-item
          label="用户名"
          name="username"
          :rules="[{ required: true, message: '请输入用户名' }]"
        >
          <a-input v-model:value="formState.username" placeholder="请输入用户名" />
        </a-form-item>

        <!-- 密码输入框 -->
        <a-form-item
          label="密码"
          name="password"
          :rules="[{ required: true, message: '请输入密码' }]"
        >
          <a-input-password v-model:value="formState.password" placeholder="请输入密码" />
        </a-form-item>

        <!-- 登录按钮 -->
        <a-form-item>
          <a-button type="primary" html-type="submit" block :loading="loading">登录</a-button>
        </a-form-item>
      </a-form>

      <!-- 返回普通用户登录按钮 -->
      <div class="back-to-user-login">
        <a href="/login">返回普通用户登录</a>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import {  ref } from 'vue'
import { message } from 'ant-design-vue';
import { useAuthStore } from '@/stores/authStore.ts'
import router from '@/router'

const authStore = useAuthStore();

// 表单数据
const formState = ref({
  username: '',
  password: '',
});
const loading = ref(false);


async function handleLogin() {
  loading.value = true;
  try {
    const success = await authStore.login(formState.value.username, formState.value.password);
    if (success) {
      // location.href="/"
      router.push('/admin');
      message.success('登录成功！');
    } else {
      message.error('登录失败，请检查用户名和密码！');
    }
  } catch (err) {
    message.error('登录失败，请稍后重试！' + err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 使容器占满整个视口高度 */
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2); /* 背景渐变 */
}

.login-card {
  width: 400px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 卡片阴影 */
}

.back-to-user-login {
  text-align: center;
  margin-top: 16px;
}
</style>
