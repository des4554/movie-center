<template>
  <!-- 搜索栏 -->
  <a-layout-header class="header">
    <!-- 搜索栏 -->
    <div class="search-container">
      <!-- 电影名搜索输入框 -->
      <a-input-search
        v-model:value="searchName"
        placeholder="请输入电影名"
        style="width: 200px; margin-right: 10px"
        @search="handleSearch"
      />
      <!-- 种类选择下拉框 -->
      <a-select
        v-model:value="searchGenre"
        placeholder="请选择种类"
        style="width: 200px; margin-right: 10px"
        @change="handleSearch"
      >
        <!-- 动态生成种类选项 -->
        <a-select-option v-for="genre in genres" :key="genre" :value="genre">
          {{ genre }}
        </a-select-option>
      </a-select>
      <!-- 评分搜索输入框 -->
      <a-input-number
        v-model:value="searchRating"
        placeholder="请输入评分"
        style="width: 200px; margin-right: 10px"
        @change="handleSearch"
      />
      <!-- 搜索按钮 -->
      <a-button @click="handleSearch">搜索</a-button>
    </div>
  </a-layout-header>
  <div class="movie-list">
    <!-- 循环遍历电影列表 -->
    <div class="movie-item" v-for="movie in currentPageData" :key="movie.movie_id" @click="goToDetail(movie.movie_id)">
      <!-- 显示电影海报 -->
<!--      <img src="D:\Project\movie-center-frontend\src\assets\poster\a.jpg" alt="Movie Poster" class="movie-poster">-->
      <img :src="`/poster/${movie.movie_id}.jpg`" alt="Movie Poster" class="movie-poster">
      <div class="movie-info">
        <!-- 显示电影名称 -->
        <h2 class="movie-title">{{ movie.title }}</h2>
        <!-- 显示电影类别 -->
        <p class="movie-genre">Genre: {{ movie.genres }}</p>
        <!-- 显示电影评分 -->
        <p class="movie-rating">Rating: {{ movie.rating }}</p>
      </div>
    </div>
  </div>
  <div class="pagination"  style="place-items: center; margin-top: 20px">
    <!-- 分页组件 -->
    <a-pagination
      v-model:current="currentPage"
      :total="total"
      :pageSize="pageSize"
      :showSizeChanger="true"
      @change="handlePageChange"
      @showSizeChange="handleSizeChange"
    />
  </div>
  <a-back-top :visibilityHeght="100" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
//test
// 定义电影数据
const movies = ref([]);
const genres = ['Adventure', 'Animation', 'Action', 'Children','Crime', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Sci-Fi', 'Thriller', 'Romance']
function fetchMovies() {
  axios.get('http://localhost:5000/movies')
  .then(res =>  {
    movies.value = res.data;
  })
}
// 分页状态
const currentPage = ref(1); // 当前页码
const pageSize = ref(25); // 每页条数
const total = computed(() => movies.value.length); // 总条数

// 计算当前页的数据
const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return movies.value.slice(start, end);
});

// 页码改变时的回调
const handlePageChange = (page) => {
  currentPage.value = page;
};

// 每页条数改变时的回调
const handleSizeChange = (current, size) => {
  pageSize.value = size;
};
fetchMovies();

const searchName = ref('')
const searchGenre = ref('')
const searchRating = ref(0)
function handleSearch() {
  const params = {
    name: searchName.value,
    genre: searchGenre.value,
    rating: searchRating.value
  };
  console.log('hello')
  // 使用axios发送GET请求
  axios.get('http://127.0.0.1:5000/movies/search', { params })
    .then(response => {
      console.log(response.data);  // 处理返回的电影数据
      // 这里你可以将返回的数据赋值给某个变量，用于显示
      movies.value = response.data;
    })
    .catch(error => {
      console.error("搜索失败:", error);
    });
}

function goToDetail(movieId) {
  console.log(movieId)
  // 跳转到详情页，传递电影ID作为参数
  router.push('/movie/' + movieId);
}
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.movie-item {
  width: 250px;
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

.header {
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
}
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
</style>
