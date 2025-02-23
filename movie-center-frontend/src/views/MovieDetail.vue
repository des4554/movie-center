<template>
  <a-layout>
    <!-- 返回按钮 -->
    <a-page-header
      title="返回"
      @back="goBack"
      style="background-color: #fff; border-bottom: 1px solid #ddd"
    />
    <a-layout-content style="padding: 24px">
      <a-row :gutter="16">
        <!-- 电影海报 -->
        <a-col :span="8">
          <img :src="`/poster/${movie.movie_id}.jpg`" alt="Movie Poster" class="detail-poster" />
        </a-col>
        <!-- 电影信息 -->
        <a-col :span="16">
          <a :ref="movie.url">{{ movie.name }}</a>
          <p><strong>电影时长:</strong> {{ movie.time }}</p>
          <p><strong>类别:</strong> {{ movie.genre }}</p>
<!--          <p><strong>评分:</strong> {{ movie.rating }}</p>-->
          <p><strong>简介:</strong> {{ movie.intro }}</p>
          <p><strong>导演:</strong> {{ movie.directors }}</p>
          <p><strong>编剧:</strong> {{ movie.writers }}</p>
          <p><strong>主演:</strong> {{ movie.stars }}</p>
          <p><strong>上映日期:</strong> {{ movie.release_time }}</p>
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

// 定义电影数据的类型
interface Movie {
  movie_id: string;
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

// 获取电影详情
const fetchMovieDetail = async () => {
  const movieId = route.params.id as string;  //动态路由，小子
  // console.log(movieId)
  movie.value.movie_id = movieId
    // 假设有一个API接口获取电影详情
    axios.get(`http://localhost:5000/movies/${movieId}`).then(res=>{
      // console.log(res.data)
      movie.value = res.data
    }).catch(err=>{
      message.error("电影详情加载失败")
    })
};

// 返回上一页
const goBack = () => {
  router.go(-1);
};

// 组件挂载时获取电影详情
onMounted(() => {
  fetchMovieDetail();
});
</script>

<style scoped>
.detail-poster {
  width: 100%;
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
