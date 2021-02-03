import XLSX from "xlsx";
import param from "../common/param";
// excel地址
export function loadRemoteFile(type, page, callback) {
  let url = "";
  if (type === "column" || type === "tag") {
    url = param.columnUrl;
  } else if (type === "homeList") {
    url = param.homeListUrl;
  }
  readWorkbookFromRemoteFile(url, function(workbook) {
    let sheetNames = workbook.SheetNames; // 工作表名称集合
    let worksheet = workbook.Sheets[sheetNames[page]]; // 这里我们只读取第一张sheet
    let json = XLSX.utils.sheet_to_json(worksheet);
    if (callback) callback(json);
  });
}

function readWorkbookFromRemoteFile(url, callback) {
  // url必须同域，否则报错
  var xhr = new XMLHttpRequest();
  xhr.open("get", url, true);
  xhr.responseType = "arraybuffer";
  xhr.onload = function() {
    if (xhr.status == 200) {
      let data = new Uint8Array(xhr.response);
      let workbook = XLSX.read(data, { type: "array" });
      if (callback) callback(workbook);
    }
  };
  xhr.send();
}

export function formatDate(date, fmt) {
  date = date == undefined ? new Date() : date;
  date =
    typeof date == "number" || typeof date == "string" ? new Date(date) : date;
  fmt = fmt || "yyyy-MM-dd HH:mm:ss";
  var o = {
    "M+": date.getMonth() + 1, //月份
    "d+": date.getDate(), //日
    "h+": date.getHours() % 12 === 0 ? 12 : date.getHours() % 12, //小时
    "H+": date.getHours(), //小时
    "m+": date.getMinutes(), //分
    "s+": date.getSeconds(), //秒
    "q+": Math.floor((date.getMonth() + 3) / 3), //季度
    S: date.getMilliseconds() //毫秒
  };
  var week = {
    "0": "\u65e5",
    "1": "\u4e00",
    "2": "\u4e8c",
    "3": "\u4e09",
    "4": "\u56db",
    "5": "\u4e94",
    "6": "\u516d"
  };

  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(
      RegExp.$1,
      (date.getFullYear() + "").substr(4 - RegExp.$1.length)
    );
  }

  if (/(E+)/.test(fmt)) {
    fmt = fmt.replace(
      RegExp.$1,
      (RegExp.$1.length > 1
        ? RegExp.$1.length > 2
          ? "\u661f\u671f"
          : "\u5468"
        : "") + week[date.getDay() + ""]
    );
  }

  for (var k in o) {
    if (new RegExp("(" + k + ")").test(fmt)) {
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length === 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length)
      );
    }
  }

  return fmt;
}
