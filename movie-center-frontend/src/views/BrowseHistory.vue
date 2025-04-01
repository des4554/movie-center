<template>
  <h2 style="margin-bottom: 20px">电影浏览历史</h2>
  <a-table :columns="columns" :data-source="records">

  </a-table>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getBrowseHistory } from '@/api/history.ts'
import { useAuthStore } from '@/stores/authStore.ts'

const authStore = useAuthStore()

class Record {
  'browse_id': number
  'movie_id': number
  'user_id': number
  'time': string
}

const records = ref<Record[]>([])

const columns = [
  {
    title: '编号',
    dataIndex: 'browse_id',
    key: 'browse_id',
  },
  {
    title: '电影id',
    dataIndex: 'movie_id',
    key: 'movie_id',
  },
  {
    title: '时间',
    dataIndex: 'time',
    key: 'time',
  },
]
function fetchRecords() {
  getBrowseHistory(authStore.user?.userid).then((res) => {
    // console.log(res.data)
    records.value = res.data.data
  })
}

onMounted(()=>{
  fetchRecords()
})
</script>
