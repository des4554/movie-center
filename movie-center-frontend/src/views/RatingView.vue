<template>
  <div>
    <h2>电影评分列表</h2>
    <a-table :columns="columns" :data-source="movieRatings">
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
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore.ts'
import axios from 'axios'
const authStore = useAuthStore()

class MovieRating {
  "rating_id": number;
  "movie_id": number;
  "user_id": number;
  "rating": number;
  "comment": string;
  "timestamp": string;
  "movie_name": string;
}

// 模拟电影评分数据
const movieRatings = ref<MovieRating[]>([]);

//获取电影评分
onMounted(()=>{
  fetchMovieRatings(authStore?.user.userid)
})

const fetchMovieRatings = (userid: number) => {
  axios.get(`http://localhost:5000/ratings/${userid}`).then(res =>  {
    // console.log(res.data)
    // 显示的是电影名字，而不是电影id
    movieRatings.value = res.data
    for (let i = 0; i < res.data.length; i++) {
      const movieId = res.data[i].movie_id
      axios.get(`http://localhost:5000/movies/${movieId}`).then(res =>  {
        const movieName = res.data.name
        // console.log(movieName)
        movieRatings.value[i].movie_name = movieName
      })
    }

  })
}
// 表格列定义
const columns = [
  {
    title: '编号',
    dataIndex: 'rating_id',
    key: 'id'
  },
  {
    title: '电影',
    dataIndex: 'movie_name',
    key: 'movie'
  },
  {
    title: '我的评分',
    dataIndex: 'rating',
    key: 'rating'
  },
  {
    title: '我的评论',
    dataIndex: 'comment',
    key: 'comment'
  },
  {
    title: '评分时间',
    dataIndex: 'timestamp',
    key: 'timestamp'
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

const addFormData = ref({
  movie: '',
  rating: null
});


const handleAddOk = () => {
  // 触发表单提交
  document.querySelector('#addForm').requestSubmit();
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
};
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
