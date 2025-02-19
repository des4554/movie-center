<template>
  <a-card :bordered="true">
    <template #title>
      <h2>根据您的喜好推荐的10部电影</h2>
    </template>
    <a-list item-layout="horizontal" :data-source="movies" :loading="loading">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-list-item-meta :description="item.description">
            <template #title>
              <a :href="item.href">{{ item.title }}</a>
            </template>
            <template #avatar>
              <a-avatar :src="item.cover" />
            </template>
          </a-list-item-meta>
        </a-list-item>
      </template>
    </a-list>
    <div style="text-align: center; margin-top: 16px;">
      <a-button type="primary" @click="fetchNewMovies">换一批</a-button>
    </div>
  </a-card>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Button, Card, List, Avatar } from 'ant-design-vue';

export default {
  components: {
    AButton: Button,
    ACard: Card,
    AList: List,
    AListItem: List.Item,
    AListItemMeta: List.Item.Meta,
    AAvatar: Avatar,
  },
  setup() {
    const movies = ref([]);
    const loading = ref(false);

    const fetchMovies = async () => {
      loading.value = true;
      // 模拟从API获取数据
      const response = await fetch('https://api.example.com/movies');
      const data = await response.json();
      movies.value = data.slice(0, 10);
      loading.value = false;
    };

    const fetchNewMovies = () => {
      fetchMovies();
    };

    onMounted(() => {
      fetchMovies();
    });

    return {
      movies,
      loading,
      fetchNewMovies,
    };
  },
};
</script>

<style scoped>
.ant-card {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.ant-list-item {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.ant-list-item:last-child {
  border-bottom: none;
}

.ant-avatar {
  width: 64px;
  height: 64px;
}
</style>
