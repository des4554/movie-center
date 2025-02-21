import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

// 自定义警告处理函数
const originalWarnHandler = console.warn; // 保存原始的 console.warn
console.warn = function (msg, ...args) {
  // 如果警告内容包含特定字符串，则忽略
  if (msg.includes('Vue received a Component that was made a reactive object')) {
    return; // 忽略这个警告
  }
  // 其他警告正常输出
  originalWarnHandler.apply(console, [msg, ...args]);
};
const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(Antd)
app.mount('#app')
