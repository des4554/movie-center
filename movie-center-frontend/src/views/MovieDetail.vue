<template>
  <a-layout>
    <!-- 返回按钮 -->
    <a-page-header
      title="返回"
      @back="goBack"
      style="background-color: #fff; border-bottom: 1px solid #ddd"
    />
    <a-layout-content style="padding-left: 75px; padding-right: 75px; padding-top: 25px;">
      <a-row :gutter="16">
        <!-- 电影海报 -->
        <a-col :span="8" style="display: flex; align-items: center; justify-content: center">
          <img :src="`/poster/${movie.movie_id}.jpg`" alt="Movie Poster" class="detail-poster" />
        </a-col>
        <!-- 电影信息 -->
        <a-col :span="16">
          <a-descriptions title="电影信息" bordered style="font-size: 30px">
            <a-descriptions-item label="电影名" >{{ movie.name }}</a-descriptions-item>
            <a-descriptions-item label="类别" :span="2">{{ movie.genre }}</a-descriptions-item>
            <a-descriptions-item label="简介">{{ movie.intro }}</a-descriptions-item>
            <a-descriptions-item label="导演">{{ movie.directors }}</a-descriptions-item>
            <a-descriptions-item label="编剧" :span="2">{{ movie.writers }}</a-descriptions-item>
            <a-descriptions-item label="主演">{{ movie.stars }}</a-descriptions-item>
            <a-descriptions-item label="上映日期">{{ movie.release_time }}</a-descriptions-item>
          </a-descriptions>

          <a-divider style="border-top: 2px solid #1890ff;"></a-divider>

          <!-- 观众统计图表 -->
          <div class="chart-container">
            <h3 style="margin-bottom: 20px; text-align: center; color: #1890ff;">观众统计</h3>
            <a-row :gutter="16">
              <a-col :span="12">
                <div ref="genderChart" style="width: 100%; height: 300px;"></div>
              </a-col>
              <a-col :span="12">
                <div ref="ageChart" style="width: 100%; height: 300px;"></div>
              </a-col>
            </a-row>
          </div>

          <a-divider style="border-top: 2px solid #1890ff;"></a-divider>

          <span style="font-weight: bold; font-size: large">我的评分  </span>
          <a-rate v-model:value="editFormData.rating" allow-half style="font-size: 30px"/>

          <a-divider style="border-top: 2px solid #1890ff;"></a-divider>

          <span style="display: block; font-weight: bold; font-size: large; margin-bottom: 15px">我的评论</span>
          <!-- 文本框 -->
          <a-textarea
            v-model:value="editFormData.comment"
            placeholder="请输入内容"
            :auto-size="{ minRows: 3, maxRows: 6 }"
            style="margin-bottom: 16px;"
          />

          <!-- 按钮组 -->
          <div>
            <a-button type="primary" @click="handleSubmit" style="margin-right: 8px;">
              提交
            </a-button>
            <a-button @click="handleClear">
              清空
            </a-button>
          </div>
        </a-col>

      </a-row>

    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/authStore.ts';
import * as echarts from 'echarts';

const authStore = useAuthStore()
// 定义电影数据的类型
interface Movie {
  movie_id: number;
  name: string;
  url: string;
  time: string;
  genre: string;
  release_time: string;
  intro: string;
  directors: string;
  writers: string;
  stars: string;
}

interface AudienceStats {
  gender: {
    male: number;
    female: number;
  };
  age: {
    'Under 18': number;
    '18-24': number;
    '25-34': number;
    '35-44': number;
    '45-54': number;
    '55+': number;
  };
}

// 获取路由实例
const route = useRoute();
const router = useRouter();

// 电影详情数据
const movie = ref<Movie>({
  movie_id: '',
  name: '',
  url: '',
  time: '',
  genre: '',
  release_time: '',
  intro: '',
  directors: '',
  writers: '',
  stars: ''
});

// 观众统计数据
const audienceStats = ref<AudienceStats>({
  gender: {
    male: 0,
    female: 0
  },
  age: {
    'Under 18': 0,
    '18-24': 0,
    '25-34': 0,
    '35-44': 0,
    '45-54': 0,
    '55+': 0
  }
});

const userId = authStore?.user.userid
const movieId = route.params.id;

// 图表引用
const genderChart = ref<HTMLElement>();
const ageChart = ref<HTMLElement>();

// 获取电影详情
const fetchMovieDetail = async () => {
  movie.value.movie_id = movieId
  // 假设有一个API接口获取电影详情
  axios.get(`http://localhost:5000/movies/${movieId}`).then(res=>{
    // console.log(res.data)
    movie.value = res.data
    // 将性别和年龄评分数据添加到audienceStats
    audienceStats.value = {
      gender: {
        male: res.data.male_rating || 0,
        female: res.data.female_rating || 0
      },
      age: {
        'Under 18': parseInt(res.data.age_rating?.split(',')[0]) || 0,
        '18-24': parseInt(res.data.age_rating?.split(',')[1]) || 0,
        '25-34': parseInt(res.data.age_rating?.split(',')[2]) || 0,
        '35-44': parseInt(res.data.age_rating?.split(',')[3]) || 0,
        '45-54': parseInt(res.data.age_rating?.split(',')[4]) || 0,
        '55+': parseInt(res.data.age_rating?.split(',')[5]) || 0
      }
    };
    initCharts();
  }).catch(()=>{
    message.error("电影详情加载失败")
  })
};

//获取评论详情
const fetchRatingInfo = ()=>{
  axios.get(`http://localhost:5000/ratings/${userId}/${movieId}`).then(res => {
    editFormData.value = res.data
  }).catch(()=>{
    console.log("暂无评论")
  })
}
// 初始化图表
const initCharts = () => {
  if (genderChart.value && ageChart.value) {
    // 性别分布饼图
    const genderChartInstance = echarts.init(genderChart.value);
    const genderOption = {
      title: {
        text: '性别分布',
        left: 'center',
        textStyle: {
          color: '#1890ff'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        data: ['男性', '女性']
      },
      series: [
        {
          name: '性别分布',
          type: 'pie',
          radius: ['50%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: [
            { value: audienceStats.value.gender.male, name: '男性', itemStyle: { color: '#1890ff' } },
            { value: audienceStats.value.gender.female, name: '女性', itemStyle: { color: '#ff85c0' } }
          ]
        }
      ]
    };
    genderChartInstance.setOption(genderOption);

    // 年龄分布柱状图
    const ageChartInstance = echarts.init(ageChart.value);
    const ageOption = {
      title: {
        text: '年龄分布',
        left: 'center',
        textStyle: {
          color: '#1890ff'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: Object.keys(audienceStats.value.age),
        axisLine: {
          lineStyle: {
            color: '#1890ff'
          }
        },
        axisLabel: {
          interval: 0,
          rotate: 30
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: '#1890ff'
          }
        }
      },
      series: [
        {
          name: '人数',
          type: 'bar',
          data: Object.values(audienceStats.value.age),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#0077e6' }
            ]),
            borderRadius: [4, 4, 0, 0]
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#2378f7' },
                { offset: 0.7, color: '#2378f7' },
                { offset: 1, color: '#83bff6' }
              ])
            }
          }
        }
      ]
    };
    ageChartInstance.setOption(ageOption);

    // 响应式调整
    window.addEventListener('resize', () => {
      genderChartInstance.resize();
      ageChartInstance.resize();
    });
  }
};

// 返回上一页
const goBack = () => {
  router.go(-1);
};

const editFormData = ref({
  movie_name: '',
  rating: 0,
  comment: ''
})

const handleSubmit = ()=>{
  axios.post(`http://localhost:5000/ratings/${userId}/${movieId}`, {
    //todo 更新时间
    rating: editFormData.value.rating,
    comment: editFormData.value.comment,
  }).then(
    ()=>{
      message.success("修改成功")
      fetchRatingInfo()
    }
  ).catch(()=>{
    console.log(userId, movieId)
  })
}

const handleClear = () =>{
  editFormData.value.rating = 0;
  editFormData.value.comment = '';
}

// 组件挂载时获取电影详情
onMounted(() => {
  fetchMovieDetail();
  fetchRatingInfo();
});
</script>

<style scoped>
.detail-poster {
  width: 75%;
  border-radius: 8px;
}

h1 {
  font-size: 24px;
  margin-bottom: 16px;
}

p {
  font-size: 16px;
  margin: 8px 0;
}

.chart-container {
  margin: 20px 0;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
