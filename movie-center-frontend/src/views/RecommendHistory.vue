<template>
  <h2 style="margin-bottom: 20px">电影推荐历史</h2>
  <a-table
    :columns="columns"
    :data-source="combinedData"
    :loading="loading"
    @change="handleTableChange"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'rating'">
        <a-rate :value="record.rating" disabled allow-half />
      </template>
      <template v-else-if="column.key === 'time'">
        {{ formatTime(record.time) }}
      </template>
    </template>
  </a-table>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getRecommendHistory } from '@/api/history.ts'
import { getMovieInfo } from '@/api/movie.ts'
import { useAuthStore } from '@/stores/authStore.ts'
import type { TableProps } from 'ant-design-vue'

const authStore = useAuthStore()
const loading = ref(false)
const sortDirection = ref<'ascend' | 'descend' | undefined>(undefined)

interface RecommendRecord {
  recommend_id: number
  movie_id: number
  user_id: number
  time: string
}

interface MovieDetails {
  movie_id: number
  title: string
  rating: number
  categories: string[]
}

const recommendRecords = ref<RecommendRecord[]>([])
const movieDetails = ref<Record<number, MovieDetails>>({})
const combinedData = ref<any[]>([])

// 格式化时间显示
const formatTime = (timeString: string) => {
  return new Date(timeString).toLocaleString()
}

const columns = [
  {
    title: '电影名称',
    dataIndex: 'title',
    key: 'title'
  },
  {
    title: '评分',
    dataIndex: 'rating',
    key: 'rating'
  },
  {
    title: '类别',
    dataIndex: 'genres',
    key: 'genres'
  },
  {
    title: '推荐时间',
    dataIndex: 'time',
    key: 'time',
    sorter: true,
    sortDirections: ['ascend', 'descend'],
    defaultSortOrder: 'descend' as const
  }
]

// 处理表格排序变化
const handleTableChange: TableProps['onChange'] = (pagination, filters, sorter) => {
  if (Array.isArray(sorter)) {
    // 多列排序情况（本例不需要）
    return
  }

  sortDirection.value = sorter.order

  if (sorter.order) {
    // 有排序时，重新排序数据
    combinedData.value.sort((a, b) => {
      const timeA = new Date(a.time).getTime()
      const timeB = new Date(b.time).getTime()

      return sorter.order === 'ascend' ? timeA - timeB : timeB - timeA
    })
  } else {
    // 没有排序时，恢复原始顺序（按recommend_id排序）
    combinedData.value.sort((a, b) => a.recommend_id - b.recommend_id)
  }
}

async function fetchMovieDetails(movieId: number): Promise<MovieDetails> {
  try {
    const response = await getMovieInfo(movieId)
    return response.data
  } catch (error) {
    console.error('获取电影详情失败:', error)
    return {
      movie_id: movieId,
      title: '未知电影',
      rating: 0,
      categories: ['未知']
    }
  }
}

async function fetchRecords() {
  loading.value = true
  try {
    // 1. 获取浏览记录
    const historyRes = await getRecommendHistory(authStore.user?.userid)
    recommendRecords.value = historyRes.data.data

    // 2. 获取所有电影详情
    const movieIds = [...new Set(recommendRecords.value.map(r => r.movie_id))]
    const detailsPromises = movieIds.map(id => fetchMovieDetails(id))
    const details = await Promise.all(detailsPromises)

    // 3. 将电影详情存入map方便查找
    details.forEach(movie => {
      movieDetails.value[movie.movie_id] = movie
    })

    // 4. 合并数据并按时间降序排列（最新浏览在前）
    combinedData.value = recommendRecords.value.map(record => ({
      ...record,
      ...movieDetails.value[record.movie_id]
    })).sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime())

  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecords()
})
</script>
