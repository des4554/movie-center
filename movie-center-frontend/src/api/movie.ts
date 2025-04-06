import request from '@/utils/request'
export const getMovieInfo = (ids) => {
  return request({
    url: '/movieinfo/' + ids
  })
}
