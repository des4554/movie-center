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
          <h1>{{ movie.title }}</h1>
          <p><strong>类别:</strong> {{ movie.genres }}</p>
          <p><strong>评分:</strong> {{ movie.rating }}</p>
          <p><strong>简介:</strong> {{ movie.description }}</p>
          <p><strong>上映日期:</strong> {{ movie.release_date }}</p>
        </a-col>
      </a-row>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';

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
  starts: string;
}

// 获取路由实例
const route = useRoute();
const router = useRouter();

// 电影详情数据
const movie = ref<Movie>({
  movie_id: '',
  name: '',
  genres: '',
  rating: '',
  description: '',
  release_date: '',
});

// 获取电影详情
const fetchMovieDetail = async () => {
  const movieId = route.params.id as string;  //动态路由，小子
  // console.log(movieId)
  movie.value.movie_id = movieId
  try {
    // 假设有一个API接口获取电影详情
    const response = await fetch(`/api/movies/${movieId}`);
    if (!response.ok) throw new Error('Failed to fetch movie details');
    const data = await response.json();
    movie.value = data;
  } catch (error) {
    message.error('加载电影详情失败');
    console.error(error);
  }
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
