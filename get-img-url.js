var superagent = require('superagent');
var fs = require("fs");

var headers = {
    Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    Origin: 'http://admin.', //#请求地址只留下后缀了
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    DNT: 1,
    Referer: 'admin/audit', //#请求地址只留下后缀了
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4,sr;q=0.2',
};

var origin = 'http://admin.', //#请求地址只留下后缀了
    urls = {
        audit: origin + '/admin/audit',
        login: origin + '/admin/login'
    },
    cookie = {
            value: "uid=EF9CD4B584C2A2DC0937FE9A046D247A; user=admin; key=a6e16f3e10b1f3c0c000316fc88e81d5066bfe98",
            expires: null
        },
    max_id = [100];

function get_json () {
       superagent
           .post(urls.audit)
           .set(headers)
           .set('Cookie', cookie.value)
           .send({
              'page': "",
              'r_id': "",
              'date': "",
              'title': "",
              'content': "",
              'status':1,
              'uid': ""
           })
           .end(function (err,res) {
             function strToJson(str){
               return JSON.parse(str);
             }
                let jsons = strToJson(res.text)
                let arr_data = jsons.res;

                let all_imgs = pussToArr(arr_data)
                console.log(all_imgs);
                write(all_imgs);
             });
   };
function pussToArr(arr) {
    let all_img = [];
    for (value of arr) {
         if (value.urls != undefined) {
           for (val of value.urls) {
             all_img.push(val)
           }
         }
      }
    return all_img;
  };
   get_json();

function write(data) {
  fs.writeFile('1.txt', data, function (err) {
         if (err) {
             console.log(err);
         } else {
             console.log('ok.');
         }
     });
}
