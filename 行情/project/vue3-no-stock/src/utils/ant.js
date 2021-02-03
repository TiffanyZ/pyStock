import {
  Button,
  Form,
  Input,
  Select,
  DatePicker,
  Checkbox,
  Radio,
  Upload,
  Table,
  Popconfirm,
  Modal,
  Menu,
  Spin,
  Drawer,
  Affix
} from "ant-design-vue";
const ant = {
  install(Vue) {
    Vue.use(Button)
      .use(Form)
      .use(Input)
      .use(Select)
      .use(DatePicker)
      .use(Checkbox)
      .use(Radio)
      .use(Upload)
      .use(Table)
      .use(Popconfirm)
      .use(Modal)
      .use(Menu)
      .use(Spin)
      .use(Drawer)
      .use(Affix);
    // Vue.component(Button.name, Button)
    // .component(Form.name, Form)
    // .component(Form.Item.name, Form.Item)
  }
};
export default ant;
