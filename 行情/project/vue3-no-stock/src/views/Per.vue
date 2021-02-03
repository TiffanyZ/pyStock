<template>
  <div class="per">
    <div>个股搜索</div>
    <a-form
      ref="perForm"
      :model="data"
      :label-col="base.labelCol"
      :wrapper-col="base.wrapperCol"
    >
      <a-form-item label="code" required name="title">
        <a-input v-model:value="data.title" placeholder="600519.SH" />
      </a-form-item>
      <a-form-item label="begin time" required name="begin">
        <a-date-picker
          v-model:value="data.begin"
          format="YYYYMMDD"
          type="date"
          placeholder="Pick a date"
          style="width: 100%;"
          @change="beginChange"
        />
      </a-form-item>
      <a-form-item label="end time" required name="end">
        <a-date-picker
          v-model:value="data.end"
          format="YYYYMMDD"
          type="date"
          placeholder="Pick a date"
          style="width: 100%;"
          @change="endChange"
        />
      </a-form-item>
      <a-form-item class="form-center" :wrapper-col="{ span: 18 }">
        <a-button type="primary" @click="onSubmitFunc">Search</a-button>
        <a-button style="margin-left: 10px;" @click="resetFormFunc"
          >Reset</a-button
        >
      </a-form-item>
    </a-form>
    <div>个股行情</div>
    <!-- 未复权 -->
    <a-spin :spinning="data.spinning">
      <a-table
        bordered
        :data-source="data.showList"
        :columns="base.columns"
        :pagination="data.paginationSet"
        @change="tableChange"
      >
      </a-table>
    </a-spin>
    <a-modal v-model:visible="data.visible" title="提示" @ok="handleOk">
      <p>{{ data.visibleText }}</p>
    </a-modal>
  </div>
</template>
<script>
import { reactive, onMounted, getCurrentInstance } from "vue";
import { allParam } from "../common/param";
// import { formatDate } from "../common/index";
import { getPerInfo, getPerFactor, getPerPageInfo } from "../services/api";

export default {
  name: "All",
  components: {},
  setup() {
    //显示当前路径
    const { ctx } = getCurrentInstance();
    console.log(ctx);
    // console.log(ctx.$router.currentRoute.value.path);
    const base = reactive(allParam);
    let data = reactive({
      spinning: false,
      paginationSet: { pageSize: 5, total: 0, current: 1 },
      title: "",
      begin: "",
      end: "",
      factorTitle: "",
      factorTime: "",
      factorEndTime: "",
      showList: [],
      visible: false,
      visibleType: "", // 区分error
      visibleText: ""
    });

    onMounted(() => {
      init();
    });

    function init() {
    }

    // 时间框选择（个股搜索）
    function beginChange(time, str) {
      data.begin = null;
      data.begin = str;
    }

    function endChange(time, str) {
      data.end = null;
      data.end = str;
    }

    // 个股搜索(未复权)
    function onSubmitFunc() {
      if (!data.title) {
        comErr("请输入查询内容");
        return;
      }
      if (!data.begin) {
        comErr("请选择开始日期");
        return;
      }
      if (!data.end) {
        comErr("请选择结束日期");
        return;
      }
      data.spinning = true;
      getPerInfo({
        code: data.title,
        begin: data.begin,
        end: data.end,
        page_size: data.paginationSet.pageSize
      }).then(res => {
        dealRes(res);
      });
    }

    // 分页，个股搜索(未复权)
    function tableChange(i) {
      data.paginationSet.current = i.current;
      getPageInfo();
    }
    function getPageInfo() {
      data.spinning = true;
      getPerPageInfo({
        code: data.title,
        page_no: data.paginationSet.current,
        page_size: data.paginationSet.pageSize
      }).then(res => {
        dealRes(res);
      });
    }

    function dealRes(res) {
      const resData = res.data || [];
      const len = resData.length;
      if (len > 0) {
        const startTime = resData[len - 1].trade_date;
        const endTime = resData[0].trade_date;
        factorSubmitFunc(startTime, endTime, resData);
      } else {
        data.showList = resData;
      }
      data.paginationSet.total = res.total || 0;
      data.spinning = false;
    }

    // 复权因子搜索
    function factorSubmitFunc(start, end, arr) {
      getPerFactor({
        code: data.title,
        begin: start,
        end: end
      }).then(res => {
        const resData = res.data || [];
        const len = resData.length;
        if (len > 0) {
          for (var i = 0; i < arr.length; i++) {
            const date = arr[i].trade_date.slice(0, 4) + "-" + arr[i].trade_date.slice(4, 6) + "-" + arr[i].trade_date.slice(6, 8);
            for (var j = 0; j < len; j++) {
              if (date === resData[j].dividOperateDate) {
                arr[i].foreAdjustFactor = resData[j].foreAdjustFactor;
                arr[i].backAdjustFactor = resData[j].backAdjustFactor;
                arr[i].adjustFactor = resData[j].adjustFactor;
              }
            }
          }
        }
        data.showList = arr;
      });
    }

    // 提交报错
    function comErr(i) {
      data.visibleType = "error";
      data.visibleText = i;
      data.visible = true;
    }

    // 重置搜索项
    function resetFormFunc() {
      data.title = "";
      data.begin = "";
      data.end = "";
      data.showList = [];
    }

    // 关闭弹框
    function handleOk() {
      data.visible = false;
    }

    return {
      base,
      data,
      beginChange,
      endChange,
      onSubmitFunc,
      tableChange,
      resetFormFunc,
      handleOk
    };
  }
};
</script>
<style lang="less" rel="stylesheet/less">
@import "../assets/less/per.less";
</style>
