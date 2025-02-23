<template>
  <a-layout>
    <!-- 返回按钮 -->
    <a-page-header
      title="返回"
      @back="goBack"
      style="background-color: #fff; border-bottom: 1px solid #ddd"
    />
    <a-layout-content style="padding-left: 75px; padding-right: 75px; padding-top: 25px;">
      <a-row :gutter="16">
        <!-- 电影海报 -->
        <a-col :span="8" style="display: flex; align-items: center; justify-content: center">
          <img :src="`/poster/${movie.movie_id}.jpg`" alt="Movie Poster" class="detail-poster" />
        </a-col>
        <!-- 电影信息 -->
        <a-col :span="16">
          <a-descriptions title="电影信息" bordered style="font-size: 30px">
            <a-descriptions-item label="电影名" >{{ movie.name }}</a-descriptions-item>
            <a-descriptions-item label="类别" :span="2">{{ movie.genre }}</a-descriptions-item>
            <a-descriptions-item label="简介">{{ movie.intro }}</a-descriptions-item>
            <a-descriptions-item label="导演">{{ movie.directors }}</a-descriptions-item>
            <a-descriptions-item label="编剧" :span="2">{{ movie.writers }}</a-descriptions-item>
            <a-descriptions-item label="主演">{{ movie.stars }}</a-descriptions-item>
            <a-descriptions-item label="上映日期">{{ movie.release_time }}</a-descriptions-item>
          </a-descriptions>

          <a-divider style="border-top: 2px solid #1890ff;"></a-divider>

          <span style="font-weight: bold; font-size: large">我的评分  </span>
          <a-rate v-model:value="editFormData.rating" allow-half style="font-size: 30px"/>

          <a-divider style="border-top: 2px solid #1890ff;"></a-divider>

          <span style="display: block; font-weight: bold; font-size: large; margin-bottom: 15px">我的评论</span>
          <!-- 文本框 -->
          <a-textarea
            v-model:value="editFormData.comment"
            placeholder="请输入内容"
            :auto-size="{ minRows: 3, maxRows: 6 }"
            style="margin-bottom: 16px;"
          />

          <!-- 按钮组 -->
          <div>
            <a-button type="primary" @click="handleSubmit" style="margin-right: 8px;">
              提交
            </a-button>
            <a-button @click="handleClear">
              清空
            </a-button>
          </div>
        </a-col>

      </a-row>

    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore.ts'
const authStore = useAuthStore()
// 定义电影数据的类型
interface Movie {
  movie_id: number;
  name: string;
  url: string;
  time: string;
  genre: string;
  release_time: string;
  intro: string;
  directors: string;
  writers: string;
  stars: string;
}

// 获取路由实例
const route = useRoute();
const router = useRouter();

// 电影详情数据
const movie = ref<Movie>({
  movie_id: '',
  name: '',
  url: '',
  time: '',
  genre: '',
  release_time: '',
  intro: '',
  directors: '',
  writers: '',
  stars: ''
});

const userId = authStore?.user.userid
const movieId = route.params.id;

// 获取电影详情
const fetchMovieDetail = async () => {
  movie.value.movie_id = movieId
    // 假设有一个API接口获取电影详情
    axios.get(`http://localhost:5000/movies/${movieId}`).then(res=>{
      // console.log(res.data)
      movie.value = res.data
    }).catch(()=>{
      message.error("电影详情加载失败")
    })
};

//获取评论详情
const fetchRatingInfo = ()=>{
  axios.get(`http://localhost:5000/ratings/${userId}/${movieId}`).then(res => {
    editFormData.value = res.data
  }).catch(()=>{
    console.log("暂无评论")
  })
}
// 返回上一页
const goBack = () => {
  router.go(-1);
};

const editFormData = ref({
  movie_name: '',
  rating: 0,
  comment: ''
})

const handleSubmit = ()=>{
  axios.post(`http://localhost:5000/ratings/${userId}/${movieId}`, {
    //todo 更新时间
    rating: editFormData.value.rating,
    comment: editFormData.value.comment,
  }).then(
    ()=>{
      message.success("修改成功")
      fetchRatingInfo()
    }
  ).catch(()=>{
    console.log(userId, movieId)
  })
}

const handleClear = () =>{
  editFormData.value.rating = 0;
  editFormData.value.comment = '';
}
// 组件挂载时获取电影详情
onMounted(() => {
  fetchMovieDetail();
  fetchRatingInfo();
});
</script>

<style scoped>
.detail-poster {
  width: 75%;
  border-radius: 8px;
}

h1 {
  font-size: 24px;
  margin-bottom: 16px;
}

p {
  font-size: 16px;
  margin: 8px 0;
}


</style>
