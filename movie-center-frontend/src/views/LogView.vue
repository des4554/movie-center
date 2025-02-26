<template>
  <a-row type="flex" justify="center" align="middle" style="height: 100vh; background: linear-gradient(135deg, #6a11cb, #2575fc);">
    <a-col :xs="22" :sm="16" :md="12" :lg="8" :xl="6">
      <a-card :bordered="false" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
        <h2 style="text-align: center; margin-bottom: 24px; color: #1890ff;">电影推荐系统</h2>
        <a-form :model="formState" @finish="handleLogin">
          <a-form-item
            name="username"
            :rules="[{ required: true, message: '请输入用户名！' }]"
          >
            <a-input
              v-model:value="formState.username"
              placeholder="用户名"
              size="large"
            >
              <template #prefix>
                <UserOutlined style="color: rgba(0, 0, 0, 0.25)" />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item
            name="password"
            :rules="[{ required: true, message: '请输入密码！' }]"
          >
            <a-input-password
              v-model:value="formState.password"
              placeholder="密码"
              size="large"
            >
              <template #prefix>
                <LockOutlined style="color: rgba(0, 0, 0, 0.25)" />
              </template>
            </a-input-password>
          </a-form-item>

          <a-form-item>
            <div class="button-group">
              <a-button
                type="primary"
                html-type="submit"
                block
                :loading="loading"
                class="login-button"
              >
                登录
              </a-button>
              <a-button
                type="default"
                block
                class="register-button"
                href="/register"
              >
                注册
              </a-button>
            </div>
          </a-form-item>
        </a-form>
        <a href="/admin/login">管理员登录入口</a>
      </a-card>
    </a-col>
  </a-row>
</template>

<script setup>
import { ref } from 'vue';
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router'

const authStore = useAuthStore();
const router = useRouter();
const loading = ref(false);
const formState = ref({
  username: '',
  password: '',
});

async function handleLogin() {
  loading.value = true;
  try {
    const success = await authStore.login(formState.value.username, formState.value.password);
    if (success) {
      // location.href="/"
      router.push('/');
      message.success('登录成功！');
    } else {
      message.error('登录失败，请检查用户名和密码！');
    }
  } catch (error) {
    message.error('登录失败，请稍后重试！');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* 自定义样式 */
.ant-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}
.ant-form-item-label label {
  font-weight: bold;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 16px; /* 按钮之间的间距 */
}

.login-button {
  background-color: #1890ff; /* 主按钮背景色 */
  border-color: #1890ff; /* 主按钮边框色 */
  color: #fff; /* 主按钮文字颜色 */
}

.register-button {
  background-color: #fff; /* 次按钮背景色 */
  border-color: #d9d9d9; /* 次按钮边框色 */
  color: rgba(0, 0, 0, 0.85); /* 次按钮文字颜色 */
}

/* 鼠标悬停效果 */
.login-button:hover {
  background-color: #40a9ff;
  border-color: #40a9ff;
}

.register-button:hover {
  background-color: #f5f5f5;
  border-color: #d9d9d9;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .button-group {
    gap: 12px; /* 在小屏幕上减少间距 */
  }
}
</style>
