<template>
  <a-layout>
    <!-- 侧边栏 -->
    <a-layout-sider :width="200" style="background: #fff">
      <a-menu
        mode="inline"
        v-model:selectedKeys="selectedKeys"
        style="height: 100%"
      >
        <a-menu-item key="user-management">
          <template #icon>
            <user-outlined />
          </template>
          用户管理
        </a-menu-item>
        <a-menu-item key="movie-management">
          <template #icon>
            <video-camera-outlined />
          </template>
          电影管理
        </a-menu-item>
        <a-menu-item key="recommendation-settings">
          <template #icon>
            <setting-outlined />
          </template>
          推荐系统设置
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <!-- 内容区域 -->
    <a-layout>
      <a-layout-content style="padding: 24px; background: #fff">
        <component :is="currentTabComponent" />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from 'vue'
import {
  UserOutlined,
  VideoCameraOutlined,
  SettingOutlined,
} from '@ant-design/icons-vue';

// 默认选中的菜单项
const selectedKeys = ref(['user-management']);

// 动态组件
const currentTabComponent = computed(() => {
  switch (selectedKeys.value[0]) {
    case 'user-management':
      return defineAsyncComponent(() => import('@/views/admin/UserMangeView.vue'));
    case 'movie-management':
      return defineAsyncComponent(() => import('@/views/admin/MovieManageView.vue'));
    case 'recommendation-settings':
      return defineAsyncComponent(() => import('@/views/admin/SettingsView.vue'));
    default:
      return null;
  }
});
</script>

<style scoped>
/* 布局样式 */
.ant-layout {
  min-height: 100vh;
}

.ant-layout-sider {
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.ant-layout-content {
  margin: 24px 16px;
  padding: 24px;
  background: #fff;
  min-height: 280px;
}
</style>
