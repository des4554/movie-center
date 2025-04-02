<template>
  <a-layout class="admin-layout">
    <!-- 侧边栏 - 修改了背景色和样式 -->
    <a-layout-sider :width="220" class="admin-sider fixed-sider">
      <!-- 管理员信息卡片 - 新增样式 -->
      <div class="admin-info">
        <a-avatar class="admin-avatar" :size="64" :src="authStore.user?.avatar_url || 'https://joeschmoe.io/api/v1/random'" />
        <div class="admin-details">
          <h3 class="admin-name">{{ authStore.user?.username }}</h3>
          <span class="admin-role">系统管理员</span>
        </div>
      </div>

      <!-- 菜单 - 修改了样式 -->
      <a-menu
        mode="inline"
        v-model:selectedKeys="selectedKeys"
        class="admin-menu"
      >
        <a-menu-item key="user-management" class="menu-item">
          <template #icon>
            <user-outlined />
          </template>
          用户管理
        </a-menu-item>
        <a-menu-item key="movie-management" class="menu-item">
          <template #icon>
            <video-camera-outlined />
          </template>
          电影管理
        </a-menu-item>
        <a-menu-item key="recommendation-settings" class="menu-item">
          <template #icon>
            <setting-outlined />
          </template>
          推荐系统设置
        </a-menu-item>
        <!-- 退出登录 -->
        <a-menu-item key="logout" class="menu-item logout-item" @click="handleLogout">
          <template #icon>
            <logout-outlined />
          </template>
          退出登录
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <!-- 内容区域 -->
    <a-layout>
      <a-layout-content class="admin-content">
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
  LogoutOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/authStore.ts'
import router from '@/router'

const authStore = useAuthStore()
// 默认选中的菜单项
const selectedKeys = ref(['user-management'])

// 动态组件
const currentTabComponent = computed(() => {
  switch (selectedKeys.value[0]) {
    case 'user-management':
      return defineAsyncComponent(() => import('@/views/admin/UserMangeView.vue'))
    case 'movie-management':
      return defineAsyncComponent(() => import('@/views/admin/MovieManageView.vue'))
    case 'recommendation-settings':
      return defineAsyncComponent(() => import('@/views/admin/SettingsView.vue'))
    default:
      return null
  }
})

const handleLogout = ()=>{
  authStore.logout();
  router.push('/admin/login')
}
</script>

<style scoped>
/* 新增固定侧边栏样式 */
.fixed-sider {
  position: fixed !important;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
  left: 0;
  top: 0;
}

.has-fixed-sider {
  margin-left: 220px !important; /* 与侧边栏宽度一致 */
  width: calc(100% - 220px) !important;
  min-height: 100vh;
}

/* 整体布局样式 */
.admin-layout {
  min-height: 100vh;
}

/* 侧边栏样式 */
.admin-sider {
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  color: white;
}

/* 管理员信息卡片样式 */
.admin-info {
  padding: 30px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-avatar {
  background-color: #fff;
  margin-bottom: 15px;
  border: 3px solid rgba(255, 255, 255, 0.2);
}

.admin-details {
  color: white;
}

.admin-name {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: white;
}

.admin-role {
  display: inline-block;
  margin-top: 5px;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 12px;
}

/* 菜单样式 */
.admin-menu {
  background: transparent !important;
  border-right: none !important;
  padding: 10px 0;
}

.admin-menu :deep(.ant-menu-item) {
  margin: 5px 10px !important;
  border-radius: 6px !important;
  color: rgba(255, 255, 255, 0.8);
  height: 45px;
  line-height: 45px;
}

.admin-menu :deep(.ant-menu-item-selected) {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  font-weight: 500;
}

.admin-menu :deep(.ant-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1) !important;
  color: white !important;
}

.admin-menu :deep(.ant-menu-item .anticon) {
  font-size: 16px;
}

/* 退出登录特殊样式 */
.logout-item {
  margin-top: 20px !important;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 10px !important;
}

/* 内容区域样式 */
.admin-content {
  padding: 24px;
  margin-left: 220px !important;
  background: #f5f7fa;
  min-height: calc(100vh - 48px);
}
</style>
