<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">All</router-link> |
      <router-link to="/per">Per</router-link> |
      <router-link to="/list">List</router-link>
    </div>
    <router-view />
    <!-- 固钉 -->
    <div>
      <a-affix :offset-bottom="data.bottom">
        <div class="main-bot">Affix bottom</div>
      </a-affix>
    </div>
  </div>
</template>
<script>
import { reactive } from "vue";
export default {
  name: "App",
  setup() {
    let data = reactive({
      bottom: 0
    });
    return {data};
  }
}

</script>
<style lang="less">
@import "./assets/less/variable.less";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  .main-bot {
    padding: 8px;
    font-size: 12px;
    color: #6d6565;
    background-color: #f1f3f5;
    box-sizing: border-box;
  }
}

#nav {
  padding: 30px;

  a {
    padding: 0 10px;
    font-weight: bold;
    color: #2c3e50;
    box-sizing: border-box;

    &.router-link-exact-active {
      color: #1890ff;
      // color: @baseColorTitle;
    }
  }
}
</style>
