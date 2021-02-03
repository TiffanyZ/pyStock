<template>
  <div class="table-edit">
    <div class="editable-cell">
      111
        <!-- <div v-if="data.editable" class="editable-cell-input-wrapper">
          <a-input v-model:value="texts" @pressEnter="check" />
          <check-outlined class="editable-cell-icon-check" @click="check" />
        </div> -->
        <!-- <div v-else class="editable-cell-text-wrapper">
          {{texts || ' '}}
          <edit-outlined class="editable-cell-icon" @click="edit" />
        </div> -->
    </div>
  </div>
</template>

<script>
// import { CheckOutlined, EditOutlined } from '@ant-design/icons-vue';
export default {
  name: "TableEdit",
  props: {
    text: String,
    record: Object,
    onChange: Function
  },
  components: {
    // CheckOutlined,
    // EditOutlined
  },
  setup() {
    let data = {
      value: "",
      editable: false
    };

    function handleChange(e) {
      const value = e.target.value;
      data.value = value;
    }

    function check() {
      data.editable = false;
      this.$emit('change', data.value);
    }

    function edit() {
      data.editable = true;
    }

    return {
      data,
      handleChange,
      check,
      edit
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
