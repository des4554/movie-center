<template>
  <div>
    <h2>电影评分列表</h2>
    <a-table :columns="columns" :data-source="movieRatings">
      <template #operation="{ record }">
        <a-button @click="editMovieRating(record)">修改评分</a-button>
        <a-popconfirm title="确定要删除这条评分吗？" @confirm="deleteMovieRating(record)">
          <a-button danger>删除</a-button>
        </a-popconfirm>
      </template>
    </a-table>
    <!-- 修改评分模态框 -->
    <a-modal :visible="isEditModalVisible" title="修改评分" @ok="handleEditOk"
             @cancel="handleEditCancel">

      <a-form :model="editFormData" >
        <a-form-item label="电影名称">
          <a-input v-model:value="editFormData.movie_name" disabled />
        </a-form-item>
        <a-form-item label="评分">
          <a-rate v-model:value="editFormData.rating" allow-half style="font-size: 30px"/>
        </a-form-item>
        <a-form-item label="评论">
          <a-input v-model:value="editFormData.comment" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore.ts'
import axios from 'axios'
import { message } from 'ant-design-vue'

const authStore = useAuthStore()

class MovieRating {
  'rating_id': number
  'movie_id': number
  'user_id': number
  'rating': number
  'comment': string
  'timestamp': string
  'movie_name': string
}

// 模拟电影评分数据
const movieRatings = ref<MovieRating[]>([])

//获取电影评分
onMounted(() => {
  fetchMovieRatings(authStore?.user.userid)
})

const fetchMovieRatings = (userid: number) => {
  axios.get(`http://localhost:5000/ratings/${userid}`).then(res => {
    // console.log(res.data)
    // 显示的是电影名字，而不是电影id
    movieRatings.value = res.data
    for (let i = 0; i < res.data.length; i++) {
      const movieId = res.data[i].movie_id
      axios.get(`http://localhost:5000/movies/${movieId}`).then(res => {
        // console.log(movieName)
        movieRatings.value[i].movie_name = res.data.name
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
]

// 修改评分模态框相关
const isEditModalVisible = ref(false)
const editFormData = ref({
  user_id: authStore?.user.id,
  movie_id: null,
  movie_name: '',
  rating: null,
  comment: ''
})

const editMovieRating = (record) => {
  isEditModalVisible.value = true
  editFormData.value.movie_id = record.movie_id
  editFormData.value.user_id = record.user_id

  editFormData.value.movie_name = record.movie_name
  editFormData.value.rating = record.rating
  editFormData.value.comment = record.comment
  editingRecord = record
}

const handleEditOk = () => {
  console.log("ok", editFormData.value)
  const userId = editFormData.value.user_id
  const movieId = editFormData.value.movie_id
  axios.post(`http://localhost:5000/ratings/${userId}/${movieId}`, {
    //todo 更新时间
    rating: editFormData.value.rating,
    comment: editFormData.value.comment,
  }).then(
    ()=>{
      message.success("修改成功")
      fetchMovieRatings(authStore?.user.userid)

      isEditModalVisible.value = false
    }
  )

}

const handleEditCancel = () => {
  isEditModalVisible.value = false
}

// 删除评分
const deleteMovieRating = (record) => {
  console.log(record)
  axios.delete(`http://localhost:5000/ratings/${record.user_id}/${record.movie_id}`).then(res=>{
    console.log(res.data)
    message.success("删除成功")
    fetchMovieRatings(authStore?.user.userid)

  })
}

</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
