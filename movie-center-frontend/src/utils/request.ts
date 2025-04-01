// src/utils/request.js
import axios from 'axios'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:5000', // 从环境变量读取
  timeout: 15000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    config.headers['Content-Type'] = 'application/json'
    return config
  },
  error => {
    // 对请求错误做些什么
    console.log('Request Error:', error)
    return Promise.reject(error)
  }
)

export default service
