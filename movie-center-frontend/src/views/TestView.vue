<template>
  <div>
<!--    表单校验-->

    <p>{{authStore.username}}</p>
    <!-- 数据列表 -->
    <ul>
      <li v-for="item in currentPageData" :key="item.id">
        {{ item.name }}
      </li>
    </ul>

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
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore.js'
import { ref, computed } from 'vue';

const authStore = useAuthStore()
// 模拟数据
const data = ref(
  Array.from({ length: 100 }, (_, index) => ({
    id: index + 1,
    name: `Item ${index + 1}`,
  }))
);

// 分页状态
const currentPage = ref(1); // 当前页码
const pageSize = ref(10); // 每页条数
const total = computed(() => data.value.length); // 总条数

// 计算当前页的数据
const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return data.value.slice(start, end);
});

// 页码改变时的回调
const handlePageChange = (page) => {
  currentPage.value = page;
  console.log('当前页码:', page);
};

// 每页条数改变时的回调
const handleSizeChange = (current, size) => {
  pageSize.value = size;
  console.log('每页条数:', size);
};
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 8px;
  border-bottom: 1px solid #eee;
}
</style>
