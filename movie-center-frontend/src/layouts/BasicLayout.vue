<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }"
    >
      <!-- 用户头像和用户名 -->
      <div class="user-info">
        <a-avatar :size="64" :src="authStore.user?.avatar_url" />
        <span class="username"> {{ authStore.user?.username }} </span>
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline" @select="handleSelect">
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <component :is="item.icon" />
          <span class="nav-text">{{ item.text }}</span>
        </a-menu-item>
<!--        <a-divider ></a-divider>-->
<!--        <div v-if="authStore?.user.role=='admin'">-->
<!--          <a-menu-item v-for="item in adminMenus" :key="item.key" >-->
<!--            <component :is="item.icon" />-->
<!--            <span class="nav-text">{{ item.text }}</span>-->
<!--          </a-menu-item>-->
<!--        </div>-->
        <a-menu-item @click="logout">
          <LogoutOutlined></LogoutOutlined>
          <span class="nav-text">登出</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">

      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        <component :is="currentComponent" />
      </a-layout-content>
      <a-layout-footer class="footer">
        Ant Design ©2018 Created by Ant UED
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import {
  VideoCameraOutlined,
  StarOutlined,
  LockOutlined,
  TagOutlined,
  EditOutlined,
  LikeOutlined,
  LogoutOutlined,
  SettingOutlined, TeamOutlined, VideoCameraFilled, ClockCircleOutlined
} from '@ant-design/icons-vue'
import MovieView from '@/views/MovieView.vue'
import LikeTagsView from '@/views/LikeTagsView.vue'
import PWDChangeView from '@/views/PWDChangeView.vue'
import InfoChange from '@/views/InfoChange.vue'
import RatingView from '@/views/RatingView.vue'
import { useAuthStore } from '../stores/authStore.ts'
import RecommandListView from '@/views/RecommandListView.vue'
import router from '@/router'
import MovieManageView from '@/views/MovieManageView.vue'
import UserManageView from '@/views/UserManageView.vue'
import SettingView from '@/views/SettingView.vue'
import BrowseHistory from '@/views/BrowseHistory.vue'
import RecommendHistory from '@/views/RecommendHistory.vue'
const authStore = useAuthStore()
console.log(authStore?.user)
const selectedKeys = ref<string[]>(['1'])
const menuItems = [
  { key: '0', icon: StarOutlined, text: '推荐列表', component: RecommandListView },

  { key: '1', icon: VideoCameraOutlined , text: '电影浏览', component: MovieView },
  { key: '2', icon: TagOutlined , text: '喜好标签', component: LikeTagsView },
  { key: '3', icon: LockOutlined , text: '修改密码', component: PWDChangeView },
  { key: '4', icon: EditOutlined , text: '修改信息', component: InfoChange },
  { key: '5', icon: LikeOutlined , text: '我的评分', component: RatingView },
  { key: '6', icon: ClockCircleOutlined , text: '浏览历史', component: BrowseHistory },
  { key: '7', icon: ClockCircleOutlined , text: '推荐历史', component: RecommendHistory },

]
const adminMenus = ref([
  { key: '6', icon: VideoCameraFilled, text: '电影管理', component: MovieManageView },
  { key: '7', icon: TeamOutlined , text: '用户管理', component: UserManageView },
  { key: '8', icon: SettingOutlined , text: '推荐设置', component: SettingView },
])
// 定义当前要显示的组件
const currentComponent = ref(null)
// 处理菜单项点击事件
const handleSelect = (selected) => {
  const key = selected.key;

  // 尝试从 menuItems 找到选中的菜单项
  let selectedItem = menuItems.find(item => item.key === key);

  if (selectedItem) {
    // 如果找到了对应的菜单项，则设置 currentComponent
    if (selectedItem.component) {
      currentComponent.value = selectedItem.component;
    } else {
      console.error(`Selected menu item with key ${key} does not have a component.`);
    }
  } else {
    // 如果在 menuItems 中没有找到，尝试从 adminMenus 中查找
    selectedItem = adminMenus.value.find(item => item.key === key);

    if (selectedItem) {
      // 同样地，在设置 currentComponent 之前检查是否存在 component 属性
      if (selectedItem.component) {
        currentComponent.value = selectedItem.component;
      } else {
        console.error(`Selected admin menu item with key ${key} does not have a component.`);
      }
    } else {
      console.error(`Could not find a menu item or admin menu item with key ${key}.`);
    }
  }
};
// 初始化当前显示的组件
const initialItem = menuItems.find(item => item.key === selectedKeys.value[0])
if (initialItem) {
  currentComponent.value = initialItem.component
}

const logout = ()=>{
  authStore.logout()
  router.push('/login')
}
</script>
<style scoped>

.footer {
  text-align: center;
  background: #efefef;
  margin-top: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* 添加分割线 */
}

.username {
  margin-top: 12px;
  color: white;
  font-size: 16px;
  font-weight: bold;
}
</style>
