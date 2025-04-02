<template>
  <a-card :bordered="true">
    <template #title>
      <h2>基于用户的协同过滤算法和差分隐私算法</h2>
    </template>
    <a-spin :spinning="loading">
    <div class="movie-list">
      <!-- 循环遍历电影列表 -->
      <div class="movie-item" v-for="movie in movies" :key="movie.movie_id" @click="goToDetail(movie.movie_id)">
        <!-- 显示电影海报 -->
        <!--      <img src="D:\Project\movie-center-frontend\src\assets\poster\a.jpg" alt="Movie Poster" class="movie-poster">-->
        <img :src="`/poster/${movie.movie_id}.jpg`" alt="Movie Poster" class="movie-poster">
        <div class="movie-info">
          <!-- 显示电影名称 -->
          <h2 class="movie-title">{{ movie.title }}</h2>
          <!-- 显示电影类别 -->
          <p class="movie-genre">种类: {{ movie.genres }}</p>
          <!-- 显示电影评分 -->
          <p class="movie-rating">评分: {{ movie.rating }}</p>
          <p class="recommend-score">推荐分数: {{ movie.recommend_score }}</p>
        </div>
      </div>
    </div>
    </a-spin>
    <div style="text-align: center; margin-top: 16px;">
      <a-button type="primary" @click="fetchMovies" :loading="loading">{{ first ? "生成推荐内容" : "换一批" }}</a-button>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore.ts'
import { addBrowseHistory } from '@/api/history.ts'
import { useRouter } from 'vue-router'
const router = useRouter()



class Movie {
  'movie_id': number;
  'title': string;
  'poster_url': string;
  'description': string;
  'genres': string;
  'rating': number;
  "recommend_score": number;
}
const authStore = useAuthStore()
const movies = ref(authStore.recommendMovies)
const loading = ref(false);
const first = ref(true);

onMounted(()=>{
  if (movies.value.length > 0) {
    first.value = false
  } else {
    first.value = true
    //fetchMovies()
  }
})
const fetchMovies = () => {
  loading.value = true;
  // 模拟从API获取数据
  axios.get(`http://localhost:5000/recommend/${authStore?.user.userid}`)
    .then(res=>{
      // console.log(res.data)
      const ids = res.data.map(item => item[0]); // 提取 ID
      const idsString = ids.join(',');
      const scores = res.data.map(item => item[1].toFixed(2)); // 提取评分
      axios.get(`http://localhost:5000/movies`, {params:{
        ids: idsString
        }}).then(res => {
          console.log(res.data)
          movies.value = res.data
          authStore.recommendMovies = res.data
          for (let i = 0; i < movies.value.length; i++) {
            movies.value[i].recommend_score = scores[i]
            authStore.recommendMovies[i].recommend_score = scores[i]
          }
          first.value = false
          console.log(movies.value)
          loading.value = false;
      })
    })
};

function add8HoursToISOTime() {
  const date = new Date();
  // 解析出原始的小时部分
  let hours = date.getUTCHours() + 8; // 增加8小时
  if (hours >= 24) { // 如果小时数超过24小时，则需要调整日期
    hours -= 24;
    date.setDate(date.getDate() + 1); // 增加一天
  }
  // 使用setUTCHours确保我们只修改小时部分，并保持其他部分不变
  date.setUTCHours(hours, date.getUTCMinutes(), date.getUTCSeconds(), date.getUTCMilliseconds());
  // 返回更新后的ISO格式字符串
  return date.toISOString();
}
const goToDetail = (movieId) => {
  router.push('/movie/' + movieId);

  // 添加一条电影浏览记录
  const obj = {
    user_id : authStore.user.userid,
    movie_id: movieId,
    time: add8HoursToISOTime(),
  }
  addBrowseHistory(obj).then(res=>{
    console.log(res)
  })
}

</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-item {
  width: 18%;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  transform-style: preserve-3d; /* 启用 3D 变形 */
  perspective: 1000px; /* 设置透视视角 */
}

.movie-item:hover {
  transform: scale(1.05); /* 3D 变形效果 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* 增加阴影 */
}

.movie-poster {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.movie-info {
  padding: 15px;
}

.movie-title {
  margin: 0;
  font-size: 1.2em;
}

.movie-genre,
.movie-rating {
  margin: 5px 0;
  font-size: 0.9em;
  color: #666;
}

</style>
