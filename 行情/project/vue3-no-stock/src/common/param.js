// const comStatic = "https://www.sttsg.com/H5/vue3-no-stock/app/static/";
const comStatic = "";
const postUrl = "https://www.sttsg.com/stock/";
// const postUrl = "http://localhost:9017/stock/";

export const param = {
  postUrl: postUrl
};

export const homeParam = {
  labelCol: { span: 6 },
  wrapperCol: { span: 12 },
  aciton: postUrl + "upload?id=",
  rules: {
    title: [
      {
        required: true,
        message: "Please input Activity title",
        trigger: "blur"
      },
      { min: 3, max: 15, message: "Length should be 3 to 15", trigger: "blur" }
    ],
    desc: [
      {
        required: true,
        message: "Please input Activity title",
        trigger: "blur"
      }
    ],
    column: [
      {
        required: true,
        message: "Please select activity column",
        trigger: "change"
      }
    ],
    time: [
      {
        required: true,
        message: "Please select activity column",
        trigger: "change"
      }
    ]
  }
};

export const allParam = {
  imgUrl: comStatic + "img/allImg/",
  defaultImg: comStatic + "img/allImg/" + "default-img.png",
  columns: [
    {
      title: "ts_code",
      dataIndex: "ts_code",
      align: "center"
    },
    {
      title: "trade_date",
      dataIndex: "trade_date",
      align: "center",
      ellipsis: true
    },
    {
      title: "open",
      dataIndex: "open",
      align: "center"
    },
    {
      title: "high",
      dataIndex: "high",
      align: "center"
    },
    {
      title: "low",
      dataIndex: "low",
      align: "center"
    },
    {
      title: "close",
      dataIndex: "close",
      align: "center"
    },
    {
      title: "pre_close",
      dataIndex: "pre_close",
      align: "center"
    },
    {
      title: "change",
      dataIndex: "change",
      align: "center"
    },
    {
      title: "pct_chg",
      dataIndex: "pct_chg",
      align: "center"
    },
    {
      title: "vol",
      dataIndex: "vol",
      align: "center"
    },
    {
      title: "amount",
      dataIndex: "amount",
      align: "center"
    },
    {
      title: "foreAdjustFactor",
      dataIndex: "foreAdjustFactor",
      align: "center"
    },
    {
      title: "backAdjustFactor",
      dataIndex: "backAdjustFactor",
      align: "center"
    },
    {
      title: "adjustFactor",
      dataIndex: "adjustFactor",
      align: "center"
    }
  ],
  labelCol: { span: 6 },
  wrapperCol: { span: 16 }
};

export const listParam = {
  imgUrl: comStatic + "img/listImg/",
  defaultImg: comStatic + "img/listImg/" + "default-img.png",
  columns: [
    {
      title: "id",
      dataIndex: "id",
      width: "10%",
      align: "center"
    },
    {
      title: "title",
      dataIndex: "title",
      align: "center",
      ellipsis: true
    },
    {
      title: "desc",
      dataIndex: "desc",
      align: "center",
      slots: { customRender: "desc" }
    },
    {
      title: "time",
      width: "15%",
      dataIndex: "time",
      align: "center"
    },
    {
      title: "img",
      width: "10%",
      dataIndex: "img",
      align: "center",
      slots: { customRender: "img" }
    },
    {
      title: "checkTime",
      width: "15%",
      dataIndex: "check_time",
      align: "center"
    },
    {
      title: "checkName",
      dataIndex: "check_name",
      align: "center"
    },
    {
      title: "operation",
      width: "15%",
      dataIndex: "operation",
      slots: { customRender: "operation" }
    }
  ]
};

export const editSetParam = {
  menus: [
    // 菜单配置
    "head", // 标题
    "bold", // 粗体
    "fontSize", // 字号
    "fontName", // 字体
    "italic", // 斜体
    "underline", // 下划线
    "strikeThrough", // 删除线
    "foreColor", // 文字颜色
    "backColor", // 背景颜色
    "link", // 插入链接
    "list", // 列表
    "justify", // 对齐方式
    "quote", // 引用
    "emoticon", // 表情
    "image", // 插入图片
    "table", // 表格
    "code", // 插入代码
    "undo", // 撤销
    "redo" // 重复
  ],
  emotions: [
    {
      title: "custom", // tab 的标题
      type: "image", // 'emoji' 或 'image' ，即 emoji 形式或者图片形式
    },
    {
      title: "emoji", // tab 的标题
      type: "emoji", // 'emoji' / 'image'
      // emoji 表情，content 是一个数组即可
      content: "😀 😃 😄 😁 😆 😅 😂 😊 😇 🙂 🙃 😉 😓 😪 😴 🙄 🤔 😬 🤐".split(
        /\s/
      )
    }
  ],
  zIndex: 2
};
