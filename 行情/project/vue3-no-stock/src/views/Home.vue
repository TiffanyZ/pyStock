<template>
  <div class="home">
    <div>
      <a-button type="primary" @click="getAllDailyFunc">
        Primary
      </a-button>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted, getCurrentInstance } from "vue";
import { homeParam } from "../common/param";
import {
  getAllDaily
} from "../services/api";

export default {
  name: "Home",
  components: {
  },
  setup() {
    //显示当前路径(用ctx的话，打包后你就会发现用不了，挂载的属性都没了,建议不要使用)
    const { ctx } = getCurrentInstance();
    // ctx.$message.success("this is message");
    // console.log(ctx.$router.currentRoute.value.path);
    console.log(ctx);

    const base = reactive(homeParam);
    let state = reactive({
      id: "",
      title: "",
      name: "",
      column: "",
      time: null,
      desc: "",
      link: "",
      img: "",
      tag: ""
    });
    let data = reactive({
      homeList: [],
      columnData: [], // 栏目
      tagData: [], // 标签
      visible: false,
      visibleType: "", // 区分error
      visibleText: "",
      acitonUrl: "",
      editor: null,
      content: "", // 富文本内容
      previewVisible: false,
      previewImage: ""
    });

    onMounted(() => {
      // 获取all当日数据
      // getAllDailyFunc();
    });

    function getAllDailyFunc() {
      getAllDaily().then(res => {
        console.log(res);
      });
    }

    return {
      state,
      base,
      data,
      getAllDailyFunc
    };
  }
};
</script>
<style lang="less" rel="stylesheet/less">
@import "../assets/less/home.less";
</style>
