<template>
  <div>
    <h2>修改用户信息</h2>
    <a-form :model="formData" @finish="handleSubmit" @finish-failed="handleSubmitFailed" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <a-form-item label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
        <a-input v-model:value="formData.username" placeholder="请输入用户名" />
      </a-form-item>
      <a-form-item label="头像">
        <div>
          <!-- 显示当前头像 -->
          <img v-if="formData.avatar" :src="formData.avatar" alt="当前头像" style="width: 100px; height: 100px; object-fit: cover; margin-bottom: 10px;" />
          <!-- 上传头像按钮 -->
          <a-upload
            :action="uploadUrl"
            :show-upload-list="false"
            :before-upload="beforeAvatarUpload"
            @change="handleAvatarChange"
          >
            <a-button>选择文件上传</a-button>
          </a-upload>
        </div>
      </a-form-item>
      <a-form-item label="电话" name="phone" :rules="[
        { required: true, message: '请输入电话号码' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码' }
      ]">
        <a-input v-model:value="formData.phone" placeholder="请输入电话号码" />
      </a-form-item>
      <a-form-item label="邮箱" name="email" :rules="[
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入正确的邮箱地址' }
      ]">
        <a-input v-model:value="formData.email" placeholder="请输入邮箱" />
      </a-form-item>
      <a-form-item label="年龄" name="age" :rules="[
        { required: true, message: '请输入年龄' },
        { type: 'number', min: 0, max: 150, message: '年龄必须在0到150之间' }
      ]">
        <a-input-number v-model:value="formData.age" placeholder="请输入年龄" />
      </a-form-item>
      <a-form-item label="性别" :rules="[{ required: true, message: '请选择性别' }]">
        <a-radio-group v-model:value="formData.gender">
          <a-radio value="男">男</a-radio>
          <a-radio value="女">女</a-radio>
        </a-radio-group>
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 14, offset: 6 }">
        <a-button type="primary" html-type="submit">提交</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import { useAuthStore } from '@/stores/authStore.js'
import axios from 'axios'

const authStore = useAuthStore()

const formData = ref({
  userid: authStore.user?.userid,
  username: authStore.user?.username,
  avatar: authStore.user?.avatar_url,
  phone: authStore.user?.phone,
  email: authStore.user?.email,
  age: authStore.user?.age,
  gender: authStore.user?.gender
});

const handleSubmit = () => {
  //先更新前端user，再发送给后端
  authStore.user = {
    ...authStore.user, // 保留原有字段
    username: formData.value.username,
    avatar_url: formData.value.avatar,
    phone: formData.value.phone,
    email: formData.value.email,
    age: formData.value.age,
    gender: formData.value.gender
  };
  // 这里可以添加实际的提交逻辑，如发送请求到后端
  axios.post('http://localhost:5000/infoChange', authStore.user).then(res => {
    console.log(res.data)
    message.success("修改成功")
  })
};

const handleSubmitFailed = (errorInfo) => {
  console.log('提交失败：', errorInfo);
  message.error('表单校验失败，请检查输入！');
};



//头像上传
const uploadUrl = 'http://localhost:5000/upload'
// 头像上传前的校验
function beforeAvatarUpload(file) {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    message.error('只能上传图片文件！');
  }
  const isLt2M = file.size / 1024 / 1024 < 2; // 限制文件大小为 2MB
  if (!isLt2M) {
    message.error('图片大小不能超过 2MB！');
  }
  return isImage && isLt2M;
}

// 处理头像上传
function handleAvatarChange(info) {
  console.log(info);
  if (info.file.status === 'done') {
    // 上传成功，更新头像 URL
    formData.value.avatar = info.file.response.url; // 假设接口返回 { url: '...' }
    message.success('头像上传成功！');
  } else if (info.file.status === 'error') {
    message.error('头像上传失败！');
  }
}


</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
