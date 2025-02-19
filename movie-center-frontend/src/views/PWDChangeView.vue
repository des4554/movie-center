<template>
  <div>
    <h2>密码修改</h2>
    <a-form :model="formData" @finish="handleSubmit" @finish-failed="handleSubmitFailed" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <a-form-item label="旧密码" :rules="[{ required: true, message: '请输入旧密码' }]">
        <a-input-password v-model:value="formData.oldPassword" placeholder="请输入旧密码" />
      </a-form-item>
      <a-form-item label="新密码" :rules="[{ required: true, message: '请输入新密码' }, { min: 6, message: '密码长度不能少于 6 位' }]">
        <a-input-password v-model:value="formData.newPassword" placeholder="请输入新密码" />
      </a-form-item>
      <a-form-item label="确认新密码" :rules="[{ required: true, message: '请确认新密码' }, { validator: validateConfirmPassword }]">
        <a-input-password v-model:value="formData.confirmPassword" placeholder="请再次输入新密码" />
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 14, offset: 6 }">
        <a-button type="primary" html-type="submit">提交</a-button>
        <a-button style="margin-left: 8px" @click="resetForm">清空</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Form, Input, Button, InputPassword } from 'ant-design-vue';

const formData = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const validateConfirmPassword = (rule, value) => {
  if (value !== formData.value.newPassword) {
    return Promise.reject('两次输入的密码不一致');
  }
  return Promise.resolve();
};

const handleSubmit = (values) => {
  console.log('提交的表单数据：', values);
  // 这里可添加实际的密码修改逻辑，如发送请求到后端
};

const handleSubmitFailed = (errorInfo) => {
  console.log('提交失败：', errorInfo);
};

const resetForm = () => {
  formData.value.oldPassword = '';
  formData.value.newPassword = '';
  formData.value.confirmPassword = '';
};
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
