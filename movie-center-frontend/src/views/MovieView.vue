<template>
  <!-- 搜索栏 -->
  <a-layout-header class="header">
    <!-- 搜索栏 -->
    <div class="search-container">
      <!-- 电影名搜索输入框 -->
      <div class="search-item">
        <span class="search-label">名称</span>
        <a-input
          v-model:value="searchName"
          class="search-input"
        />
      </div>

      <!-- 种类选择下拉框 -->
      <div class="search-item">
        <span class="search-label">类型</span>
        <a-select
          v-model:value="searchGenre"
          placeholder="请选择种类"
          class="search-input"
        >
          <a-select-option v-for="genre in genres" :key="genre" :value="genre">
            {{ genre }}
          </a-select-option>
        </a-select>
      </div>

      <!-- 评分搜索输入框 -->
      <div class="search-item">
        <span class="search-label">评分</span>
        <a-input-number
          v-model:value="searchRating"
          :min="0"
          :max="5"
          :step="0.1"
          placeholder="0-5分"
          class="search-input"
        />
      </div>

      <!-- 按钮组 -->
      <div class="button-group">
        <a-button @click="handleReset">重置</a-button>
        <a-button @click="handleSearch" type="primary">搜索</a-button>
      </div>
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
import { message } from 'ant-design-vue'
import { useAuthStore } from '@/stores/authStore.ts'
import { addBrowseHistory } from '@/api/history.ts'
const authStore = useAuthStore()
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
const searchRating = ref(3)
function handleSearch() {
  const params = {
    name: searchName.value,
    genre: searchGenre.value,
    rating: searchRating.value
  };
  // 使用axios发送GET请求
  axios.get('http://127.0.0.1:5000/movies/search', { params })
    .then(response => {
      movies.value = response.data;
      message.success("一共搜索到"+ response.data.length+"部电影");
    })
    .catch(error => {
      console.error("搜索失败:", error);
    });
}

function handleReset() {
  searchName.value = '';
    searchGenre.value = '';
    searchRating.value = 3;
}

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
function goToDetail(movieId) {
  //添加一条电影浏览记录
  const obj = {
    user_id : authStore.user.userid,
    movie_id: movieId,
    time: add8HoursToISOTime(),
  }
  addBrowseHistory(obj).then(res=>{
    console.log(res)
  })
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
  width: 16%;
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
/* 基础样式 */
.search-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  padding: 16px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.search-item {
  display: flex;
  align-items: center;
  min-width: 200px;
  flex: 1;
}

.search-label {
  margin-right: 8px;
  white-space: nowrap;
  color: #333;
  font-weight: 500;
}

.search-input {
  flex: 1;
  min-width: 120px;
}

.button-group {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .search-item {
    min-width: 100%;
  }

  .button-group {
    margin-left: 0;
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 480px) {
  .search-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .search-label {
    margin-right: 0;
  }

  .search-input {
    width: 100%;
  }

  .button-group {
    justify-content: space-between;
  }
}
</style>
