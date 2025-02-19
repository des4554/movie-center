<template>
  <a-row type="flex" justify="center" align="middle" style="height: 100vh; background: linear-gradient(135deg, #6a11cb, #2575fc);">
    <a-col :xs="22" :sm="16" :md="12" :lg="8" :xl="6">
      <a-card :bordered="false" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
    <h2 style="text-align: center">注册</h2>
    <a-form
      :model="formState"
      name="register"
      layout="vertical"
      @finish="onFinish"
    >
      <a-form-item
        label="用户名"
        name="username"
        :rules="[{ required: true, message: '请输入用户名!' }]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        label="密码"
        name="password"
        :rules="[{ required: true, message: '请输入密码!' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item
        label="确认密码"
        name="confirmPassword"
        :rules="[
          { required: true, message: '请确认密码!' },
          { validator: validatePassword },
        ]"
      >
        <a-input-password v-model:value="formState.confirmPassword" />
      </a-form-item>

      <a-form-item>
        <div class="button-group">
          <a-button type="primary" html-type="submit" :loading="loading">
            确认
          </a-button>
          <a-button type="default" html-type="submit" :loading="loading" href="/login">
            取消
          </a-button>

        </div>

      </a-form-item>
    </a-form>
      </a-card>
    </a-col>
  </a-row>
</template>

<script lang="ts">
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { useAuthStore } from '@/stores/authStore.js'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const formState = reactive({
      username: '',
      password: '',
      confirmPassword: '',
    });

    const loading = ref(false);

    const validatePassword = async (_rule, value) => {
      if (value !== formState.password) {
        return Promise.reject('两次输入的密码不一致!');
      } else {
        return Promise.resolve();
      }
    };
    // 表单提交成功时的逻辑
    const onFinish = async (values) => {
      loading.value = true; // 显示加载状态
      if (formState.password === formState.confirmPassword) {
        formState.username = '';
        formState.password = '';
        formState.confirmPassword = '';
        const success = await authStore.register(values.username, values.password);
        if (success) {
          message.success('注册成功！');
        } else {
          message.error('注册失败，请检查用户名和密码！');
        }
      } else {
        message.error('两次输入的密码不一致！');
      }
      loading.value = false;
      // location.href="/login"
      router.push("/login")
    };
    return {
      formState,
      loading,
      validatePassword,
      onFinish,
    };
  },
};
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

</style>
