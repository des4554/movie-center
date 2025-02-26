<template>
  <div>
    <!-- 操作按钮 -->
    <a-button type="primary" @click="showModal('add')">新增用户</a-button>

    <!-- 用户列表 -->
    <a-table
      :columns="columns"
      :data-source="userList"
      :pagination="pagination"
      :loading="loading"
      row-key="user_id"
      style="margin-top: 20px"
    >
      <!-- 操作列 -->
      <template #action="{ record }">
        <a-button type="link" @click="showModal('edit', record)">编辑</a-button>
        <a-button type="link" danger @click="handleDelete(record.user_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑用户弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
    >
      <a-form ref="formRef" :model="formState" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-item label="用户名" name="username" :rules="[{ required: true, message: '请输入用户名' }]">
          <a-input v-model:value="formState.username" />
        </a-form-item>
        <a-form-item label="密码" name="password" :rules="[{ required: true, message: '请输入密码' }]">
          <a-input-password v-model:value="formState.password" />
        </a-form-item>
        <a-form-item label="邮箱" name="email" :rules="[{required: true, message: '请填入邮箱'}]">
          <a-input v-model:value="formState.email" />
        </a-form-item>
        <a-form-item label="角色" name="role" v-if="currentAction=='edit'">
          <a-input v-model:value="formState.role" disabled/>
        </a-form-item>
        <a-form-item label="角色" name="role" v-else :rules="[{ required: true, message: '请选择角色' }]">
          <a-select v-model:value="formState.role">
            <a-select-option value="user">user</a-select-option>
            <a-select-option value="admin">admin</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="手机号" name="phone">
          <a-input v-model:value="formState.phone" />
        </a-form-item>
        <a-form-item label="年龄" name="age">
          <a-input-number v-model:value="formState.age" />
        </a-form-item>
        <a-form-item label="性别" name="gender">
          <a-select v-model:value="formState.gender">
            <a-select-option value="男">男</a-select-option>
            <a-select-option value="女">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="喜好标签" name="tags">
          <a-input v-model:value="formState.tags" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios'

// 用户列表数据
const userList = ref([]);
const loading = ref(false);

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  onChange: (page) => {
    pagination.current = page;
    fetchUserList();
  },
});

// 表格列配置
const columns = [
  { title: '用户ID', dataIndex: 'user_id', key: 'user_id' },
  { title: '用户名', dataIndex: 'username', key: 'username' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '角色', dataIndex: 'role', key: 'role' },
  { title: '手机号', dataIndex: 'phone', key: 'phone' },
  { title: '年龄', dataIndex: 'age', key: 'age' },
  { title: '性别', dataIndex: 'gender', key: 'gender' },
  { title: '操作', key: 'action', slots: { customRender: 'action' } },
];

// 弹窗相关状态
const modalVisible = ref(false);
const modalTitle = ref('新增用户');
const formState = reactive({
  user_id: null,
  username: '',
  password: '',
  email: '',
  role: '',
  avatarUrl: '',
  phone: '',
  age: null,
  gender: '',
  tags: '',
});
const currentAction = ref('add'); // 当前操作：add 或 edit

// 获取用户列表
const fetchUserList = async () => {
  loading.value = true;
  try {
    // 模拟 API 调用
    axios.get('http://localhost:5000/users').then(res=>{
      userList.value = res.data
      pagination.total = res.data.length
    })
  } catch (error) {
    message.error('获取用户列表失败');
  } finally {
    loading.value = false;
  }
};

// 显示弹窗
const showModal = (action, record) => {
  currentAction.value = action;
  modalTitle.value = action === 'add' ? '新增用户' : '编辑用户';
  if (action === 'edit') {
    Object.assign(formState, record); // 填充表单数据
  } else {
    Object.assign(formState, {
      user_id: null,
      username: '',
      password: '',
      email: '',
      role: '',
      avatarUrl: '',
      phone: '',
      age: null,
      gender: '',
      tags: '',
    }); // 重置表单
  }
  modalVisible.value = true;
};
const formRef = ref(null);
// 提交表单
const handleModalOk = async () => {
  try {
    await formRef.value.validate();
    const url = currentAction.value === 'add' ? 'http://localhost:5000/user' : `http://localhost:5000/infoChange`;
    const method = 'POST';
    // 构造请求体，将 user_id 改为 userid
    const requestBody = {
      ...formState,
      userid: formState.user_id, // 将 user_id 改为 userid
    };
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody),
    });
    if (response.ok) {
      message.success(currentAction.value === 'add' ? '新增成功' : '更新成功');
      fetchUserList(); // 刷新列表
      modalVisible.value = false;
    } else if (currentAction.value === 'add') {
      message.error('用户名重复，添加失败')
    }
  } catch (error) {
    message.error('操作失败');
  }
};

// 删除用户
const handleDelete = async (userId) => {
  try {
    const response = await fetch(`http://localhost:5000/user/${userId}`, { method: 'DELETE' });
    if (response.ok) {
      message.success('删除成功');
      fetchUserList(); // 刷新列表
    }
  } catch (error) {
    message.error('删除失败');
  }
};

// 初始化加载用户列表
onMounted(() => {
  fetchUserList();
});
</script>

<style scoped>
/* 样式可以根据需要调整 */
</style>
