<template>
  <div class="list"></div>
</template>
<script>
import { reactive, onMounted } from "vue";
import { listParam, allParam } from "../common/param";
// import { getHomeList, getColumnList, backColumnList, getOper } from "../services/api";
// import { MailOutlined } from '@ant-design/icons-vue';
export default {
  name: "List",
  components: {
    // MailOutlined
  },
  setup() {
    const base = reactive(listParam);
    const allbase = reactive(allParam);
    let data = reactive({
      homeList: [],
      columnData: [],
      current: [0],
      spinning: true,
      paginationSet: {
        pageSize: 5,
        total: 0,
        current: 1
      },
      currentColumn: "",
      drawerVisible: false,
      drawerContent: "",
      drawerTitle: "",
      previewVisible: false,
      previewImage: "",
      czyVisible: false,
      operForm: {
        code: ""
      },
      operName: ""
    });

    onMounted(() => {
      // getColumnFunc();
    });

    // function getColumnFunc() {
    //   getColumnList({}).then(res => {
    //     data.columnData = res.data || [];
    //     if (res.data && res.data.length > 0) {
    //       data.currentColumn = res.data[0].id;
    //       getListFunc();
    //     }
    //   });
    // }

    return {
      base,
      allbase,
      data
    };
  }
};
</script>
<style lang="less" rel="stylesheet/less">
@import "../assets/less/list.less";
</style>
