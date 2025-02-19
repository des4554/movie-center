<template>
  <div>
    <h2>电影评分列表</h2>
    <a-table :columns="columns" :data-source="movieRatings">
      <template #title>
        <a-button @click="addMovieRating">添加评分</a-button>
      </template>
      <template #operation="{ record }">
        <a-button @click="editMovieRating(record)">修改评分</a-button>
        <a-button danger @click="deleteMovieRating(record)">删除</a-button>
      </template>
    </a-table>
    <!-- 修改评分模态框 -->
    <a-modal :visible="isEditModalVisible" title="修改评分" @ok="handleEditOk" @cancel="handleEditCancel">
      <template #content>
        <a-form :model="editFormData" @finish="handleEditFormSubmit">
          <a-form-item label="电影名称">
            <a-input v-model:value="editFormData.movie" disabled />
          </a-form-item>
          <a-form-item label="评分" :rules="[{ required: true, message: '请输入评分' }, { type: 'number', min: 0, max: 10, message: '评分范围为 0 - 10' }]">
            <a-input-number v-model:value="editFormData.rating" :min="0" :max="10" />
          </a-form-item>
        </a-form>
      </template>
    </a-modal>
    <!-- 添加评分模态框 -->
    <a-modal :visible="isAddModalVisible" title="添加评分" @ok="handleAddOk" @cancel="handleAddCancel">
      <template #content>
        <a-form :model="addFormData" @finish="handleAddFormSubmit">
          <a-form-item label="电影名称" :rules="[{ required: true, message: '请输入电影名称' }]">
            <a-input v-model:value="addFormData.movie" />
          </a-form-item>
          <a-form-item label="评分" :rules="[{ required: true, message: '请输入评分' }, { type: 'number', min: 0, max: 10, message: '评分范围为 0 - 10' }]">
            <a-input-number v-model:value="addFormData.rating" :min="0" :max="10" />
          </a-form-item>
        </a-form>
      </template>
    </a-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Table, Button, Modal, Form, Input, InputNumber } from 'ant-design-vue';

// 模拟电影评分数据
const movieRatings = ref([
  {
    key: '1',
    id: 1,
    movie: '复仇者联盟4',
    rating: 8.5,
    ratingTime: '2025-01-01 10:00:00'
  },
  {
    key: '2',
    id: 2,
    movie: '流浪地球2',
    rating: 9.0,
    ratingTime: '2025-01-10 14:30:00'
  }
]);

// 表格列定义
const columns = [
  {
    title: '编号',
    dataIndex: 'id',
    key: 'id'
  },
  {
    title: '电影',
    dataIndex: 'movie',
    key: 'movie'
  },
  {
    title: '评分',
    dataIndex: 'rating',
    key: 'rating'
  },
  {
    title: '评分时间',
    dataIndex: 'ratingTime',
    key: 'ratingTime'
  },
  {
    title: '操作',
    key: 'operation',
    slots: { customRender: 'operation' }
  }
];

// 修改评分模态框相关
const isEditModalVisible = ref(false);
const editFormData = ref({
  movie: '',
  rating: null
});
let editingRecord = null;

const editMovieRating = (record) => {
  isEditModalVisible.value = true;
  editFormData.value.movie = record.movie;
  editFormData.value.rating = record.rating;
  editingRecord = record;
};

const handleEditOk = () => {
  // 触发表单提交
  document.querySelector('#editForm').requestSubmit();
};

const handleEditCancel = () => {
  isEditModalVisible.value = false;
};

const handleEditFormSubmit = (values) => {
  const index = movieRatings.value.findIndex(item => item.key === editingRecord.key);
  if (index !== -1) {
    movieRatings.value[index].rating = values.rating;
    movieRatings.value[index].ratingTime = new Date().toLocaleString();
  }
  isEditModalVisible.value = false;
};

// 删除评分
const deleteMovieRating = (record) => {
  movieRatings.value = movieRatings.value.filter(item => item.key !== record.key);
};

// 添加评分模态框相关
const isAddModalVisible = ref(false);
const addFormData = ref({
  movie: '',
  rating: null
});

const addMovieRating = () => {
  isAddModalVisible.value = true;
};

const handleAddOk = () => {
  // 触发表单提交
  document.querySelector('#addForm').requestSubmit();
};

const handleAddCancel = () => {
  isAddModalVisible.value = false;
};

const handleAddFormSubmit = (values) => {
  const newId = movieRatings.value.length > 0 ? movieRatings.value[movieRatings.value.length - 1].id + 1 : 1;
  const newRecord = {
    key: String(newId),
    id: newId,
    movie: values.movie,
    rating: values.rating,
    ratingTime: new Date().toLocaleString()
  };
  movieRatings.value.push(newRecord);
  isAddModalVisible.value = false;
};
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
