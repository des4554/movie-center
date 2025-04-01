<template>
  <a-card title="浏览历史" :bordered="false">
    <!-- 搜索和筛选区域 -->
    <div class="search-container">
      <a-input-search
        v-model:value="searchText"
        placeholder="搜索电影"
        style="width: 300px"
        @search="handleSearch"
      />
      <a-range-picker
        v-model:value="dateRange"
        :disabled-date="disabledDate"
        style="margin-left: 16px"
      />
    </div>

    <!-- 浏览历史列表 -->
    <a-table
      :columns="columns"
      :data-source="filteredHistory"
      :pagination="pagination"
      :loading="loading"
      row-key="browse_id"
      @change="handleTableChange"
    >
      <template #bodyCell="{ column, record }">
        <!-- 电影名称列 -->
        <template v-if="column.key === 'movie'">
          <router-link :to="`/movie/detail/${record.movie_id}`">
            {{ getMovieName(record.movie_id) }}
          </router-link>
        </template>

        <!-- 浏览时间列 -->
        <template v-if="column.key === 'time'">
          {{ formatDateTime(record.time) }}
        </template>

        <!-- 操作列 -->
        <template v-if="column.key === 'action'">
          <a-button type="link" danger @click="handleDelete(record.browse_id)">
            删除
          </a-button>
        </template>
      </template>
    </a-table>
  </a-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import dayjs from 'dayjs';
import { getBrowseHistory, deleteBrowseRecord } from '@/api/history';
import { useAuthStore } from '@/stores/authStore.ts'

// import { getMovieById } from '@/api/movie';
const authStore = useAuthStore()
// 表格列配置
const columns = [
  {
    title: '电影名称',
    key: 'movie',
    width: '40%',
  },
  {
    title: '浏览时间',
    key: 'time',
    sorter: true,
    width: '30%',
  },
  {
    title: '操作',
    key: 'action',
    width: '30%',
  },
];

// 数据状态
const loading = ref(false);
const browseHistory = ref([]);
const moviesCache = ref({});
const searchText = ref('');
const dateRange = ref([]);
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
});

// 获取浏览历史
const fetchHistory = (userid) => {
  getBrowseHistory(userid).then((res) => {
    console.log(res)
  })
};

// 获取电影信息并缓存
const fetchMovieInfo = async (movieId) => {
  if (!moviesCache.value[movieId]) {
    // const res = await getMovieById(movieId);
    // moviesCache.value[movieId] = res.data;
  }
};

// 获取电影名称
const getMovieName = (movieId) => {
  return moviesCache.value[movieId]?.title || '未知电影';
};

// 格式化时间显示
const formatDateTime = (time) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss');
};

// 禁用未来日期
const disabledDate = (current) => {
  return current && current > dayjs().endOf('day');
};

// 删除记录
const handleDelete = async (browseId) => {
  try {
    await deleteBrowseRecord(browseId);
    message.success('删除成功');
    fetchHistory();
  } catch (error) {
    message.error('删除失败');
  }
};

// 处理表格变化（分页、排序等）
const handleTableChange = (pag, filters, sorter) => {
  pagination.value.current = pag.current;
  pagination.value.pageSize = pag.pageSize;
  fetchHistory();
};

// 搜索处理
const handleSearch = () => {
  pagination.value.current = 1;
  fetchHistory();
};

// 计算过滤后的数据
const filteredHistory = computed(() => {
  let data = [...browseHistory.value];

  // 按时间降序排列
  data.sort((a, b) => dayjs(b.time).unix() - dayjs(a.time).unix());

  // 文本搜索
  if (searchText.value) {
    const search = searchText.value.toLowerCase();
    data = data.filter(item => {
      const movieName = getMovieName(item.movie_id).toLowerCase();
      return movieName.includes(search);
    });
  }

  // 日期范围筛选
  if (dateRange.value && dateRange.value.length === 2) {
    const [start, end] = dateRange.value;
    data = data.filter(item => {
      const time = dayjs(item.time);
      return time.isAfter(start) && time.isBefore(end);
    });
  }

  return data;
});

// 初始化加载
onMounted(() => {
  fetchHistory(authStore?.user.userid);
  console.log("id", authStore?.user.userid);
});
</script>

<style scoped>
.search-container {
  margin-bottom: 24px;
  display: flex;
}
</style>
