<template>
  <div>
<!--    <h2>请选择你喜欢的电影类型</h2>-->

    <a-checkbox-group v-model="checkedList" @change="handleCheckboxChange" >
      <a-checkbox v-for="genre in movieGenres" :key="genre" :value="genre" class="a-checkbox-wrapper">
        {{ genre }}
      </a-checkbox>
    </a-checkbox-group>
    <div style="margin-top: 20px;">
      <a-button type="primary" @click="handleSubmit">提交</a-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Checkbox, Button } from 'ant-design-vue';

export default {
  components: {
    'a-checkbox': Checkbox,
    'a-checkbox-group': Checkbox.Group,
    'a-button': Button
  },
  data() {
    return {
      movieGenres: ['动作', '喜剧', '科幻', '恐怖', '爱情', '悬疑', '动画', '冒险'],
      checkedList: []
    };
  },
  methods: {
    handleCheckboxChange(checkedValues) {
      this.checkedList = checkedValues;
    },
    handleSubmit() {
      console.log('你选择的电影类型是:', this.checkedList);
      // 这里可以添加实际的提交逻辑，例如发送数据到服务器
    }
  }
};
</script>

<style scoped>
/* 调整复选框标签的间距 */
.a-checkbox-wrapper {
  margin-right: 50px; /* 可以根据需要调整这个值来改变间距 */
  margin-bottom: 30px;
}
</style>
