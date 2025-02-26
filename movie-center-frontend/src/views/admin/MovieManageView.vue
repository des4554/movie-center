<template>
  <div>
    <!-- 操作按钮 -->
    <a-button type="primary" @click="showModal('add')">新增电影</a-button>

    <!-- 电影列表 -->
    <a-table
      :columns="columns"
      :data-source="movieList"
      :pagination="pagination"
      :loading="loading"
      row-key="id"
      style="margin-top: 20px"
    >
      <!-- 操作列 -->
      <template #action="{ record }">
        <a-button type="link" @click="showModal('edit', record)">编辑</a-button>
        <a-button type="link" danger @click="handleDelete(record.id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑电影弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form ref="formRef" :model="formState" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
        <a-form-item label="电影名称" name="name" :rules="[{ required: true, message: '请输入电影名称' }]">
          <a-input v-model:value="formState.name" />
        </a-form-item>
        <a-form-item label="电影链接" name="url">
          <a-input v-model:value="formState.url" />
        </a-form-item>
        <a-form-item label="时长" name="time">
          <a-input v-model:value="formState.time" />
        </a-form-item>
        <a-form-item label="类型" name="genre">
          <a-input v-model:value="formState.genre" />
        </a-form-item>
        <a-form-item label="上映时间" name="release_time">
          <a-input v-model:value="formState.release_time" />
        </a-form-item>
        <a-form-item label="简介" name="intro">
          <a-textarea v-model:value="formState.intro" />
        </a-form-item>
        <a-form-item label="导演" name="directors">
          <a-input v-model:value="formState.directors" />
        </a-form-item>
        <a-form-item label="编剧" name="writers">
          <a-input v-model:value="formState.writers" />
        </a-form-item>
        <a-form-item label="主演" name="stars">
          <a-textarea v-model:value="formState.stars" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios'

// 电影列表数据
const movieList = ref([]);
const loading = ref(false);
const formRef = ref(null);
// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  onChange: (page) => {
    pagination.current = page;
    fetchMovieList();
  },
});

// 表格列配置
const columns = [
  { title: '电影名称', dataIndex: 'name', key: 'name' },
  { title: '时长', dataIndex: 'time', key: 'time' },
  { title: '类型', dataIndex: 'genre', key: 'genre' },
  { title: '上映时间', dataIndex: 'release_time', key: 'release_time' },
  { title: '简介', dataIndex: 'intro', key: 'intro' },
  { title: '导演', dataIndex: 'directors', key: 'directors' },
  { title: '编剧', dataIndex: 'writers', key: 'writers' },
  { title: '主演', dataIndex: 'stars', key: 'stars' },
  { title: '操作', key: 'action', slots: { customRender: 'action' } },
];

// 弹窗相关状态
const modalVisible = ref(false);
const modalTitle = ref('新增电影');
const formState = reactive({
  id: null,
  name: '',
  url: '',
  time: '',
  genre: '',
  release_time: '',
  intro: '',
  directors: '',
  writers: '',
  stars: '',
});
const currentAction = ref('add'); // 当前操作：add 或 edit

// 获取电影列表
const fetchMovieList = async () => {
  loading.value = true;
  axios.get('http://localhost:5000/allmovies').then(res=>{
    movieList.value = res.data
    loading.value = false;
  }).catch(err=>{
    message.error("获取电影列表失败")
  })
};

// 显示弹窗
const showModal = (action, record) => {
  currentAction.value = action;
  modalTitle.value = action === 'add' ? '新增电影' : '编辑电影';
  if (action === 'edit') {
    Object.assign(formState, record); // 填充表单数据
  } else {
    Object.assign(formState, {
      id: null,
      name: '',
      url: '',
      time: '',
      genre: '',
      release_time: '',
      intro: '',
      directors: '',
      writers: '',
      stars: '',
    }); // 重置表单
  }
  modalVisible.value = true;
};

// 提交表单
const handleModalOk = async () => {
  try {
    await formRef.value.validate();
    const url = currentAction.value === 'add' ? 'http://localhost:5000/movies' : `http://localhost:5000/movies/${formState.id}`;
    const method = currentAction.value === 'add' ? 'POST' : 'PUT';
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formState),
    });
    if (response.ok) {
      message.success(currentAction.value === 'add' ? '新增成功' : '更新成功');
      fetchMovieList(); // 刷新列表
      modalVisible.value = false;
    }
  } catch (error) {
    message.error('操作失败');
  }
};

// 删除电影
const handleDelete = async (movieId) => {
  try {
    const response = await fetch(`http://localhost:5000/movies/${movieId}`, { method: 'DELETE' });
    if (response.ok) {
      message.success('删除成功');
      fetchMovieList(); // 刷新列表
    }
  } catch (error) {
    message.error('删除失败');
  }
};

// 初始化加载电影列表
onMounted(() => {
  fetchMovieList();
});
</script>

<style scoped>
/* 样式可以根据需要调整 */
</style>
