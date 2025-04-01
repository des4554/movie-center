import request from '@/utils/request' // 假设你使用 axios 封装
export const getMovieInfo = (ids) => {
  return request({
    url: '/movieinfo/' + ids
  })
}
