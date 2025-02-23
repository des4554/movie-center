<template>
  <div>
    <!--    <h2>请选择你喜欢的电影类型</h2>-->

    <a-checkbox-group v-model:value="checkedList" >
      <a-checkbox v-for="genre in movieGenres" :key="genre" :value="genre"
                  class="a-checkbox-wrapper">
        {{ genre }}
      </a-checkbox>
    </a-checkbox-group>
    <div style="margin-top: 20px;">
      <a-button type="primary" @click="handleSubmit">提交</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore.ts'
import { message } from 'ant-design-vue'
const authStore = useAuthStore();

const movieGenres = ['动作', '喜剧', '科幻', '恐怖', '爱情', '悬疑', '动画', '冒险']
const checkedList = ref<string[]>(authStore.user?.tags.split(','))


function handleSubmit() {
  console.log('你选择的电影类型是:', checkedList.value)
  //先更新前端user，再发送给后端
  authStore.user = {
    ...authStore.user, // 保留原有字段
    tags: checkedList.value.join()
  };
  // 这里可以添加实际的提交逻辑，如发送请求到后端
  axios.post('http://localhost:5000/infoChange', authStore.user).then(res => {
    console.log(res.data)
    message.success("修改成功")
  })
}


</script>

<style scoped>
/* 调整复选框标签的间距 */
.a-checkbox-wrapper {
  margin-right: 50px; /* 可以根据需要调整这个值来改变间距 */
  margin-bottom: 30px;
}
</style>
