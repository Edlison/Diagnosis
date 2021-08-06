$(document).ready(function() {
    $("#pic-p").on("change", getPath);
    $("#subque").on("click", flash_question);
})

var base46;

function getObjectURL(file) {
    var url = null;
    if (window.createObjcectURL!= undefined) {
        url = window.createOjcectURL(file);
    } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}

function getPath()
{
    var obj = document.getElementById("pic")
  if(obj)
    {

    if (window.navigator.userAgent.indexOf("MSIE")>=1)
      {
        obj.select();
      }

    else if(window.navigator.userAgent.indexOf("Firefox")>=1)
      {
      if(obj.files)
        {
            var reader  = new FileReader();
            var base = null
            reader.readAsDataURL(obj.files[0])
            reader.onload = function(){//完成后this.result为二进制流
                 console.log(this.result);
                 base46 = this.result
                // var startNum = base46.indexOf("base64,");
                // startNum = startNum * 1 + 7;
                // //去除前部格式信息（如果有需求）
                // base46 = base46.slice(startNum);
                upload_pic()
      　　　　}
        }
      }
    else if(window.navigator.userAgent.indexOf("Chrome")>=1)
      {
      if(obj.files)
        {
            var reader  = new FileReader();
            var base = null
            reader.readAsDataURL(obj.files[0])
            reader.onload = function(){//完成后this.result为二进制流
                 console.log(this.result);
                 base46 = this.result
                // var startNum = base46.indexOf("base64,");
                // startNum = startNum * 1 + 7;
                // //去除前部格式信息（如果有需求）
                // base46 = base46.slice(startNum);
                upload_pic()
      　　　　}
        }
      }
    }
}

function upload_pic(){
    var p = document.getElementById("pic").files[0]
    var input = document.getElementById("pic")
    var pic = getObjectURL(p);

    $.post('/i', {
        'pic': base46
    }).done(function (response) {
        var res = response['res']
        // $(".hero-content").append("<img src='"+res+"'>")
        var hero = document.getElementById("result")
        hero.style.animation="none"
        hero.style.webkitAnimation="none"
        hero.style.top="100px"
        hero.innerHTML="<table style=\"width: 600px\">\n" +
            "              <tr>\n" +
            "                <th style=\"width: 280px\"><img src=\""+pic+"\" style=\"width: 280px\"></th>\n" +
            "              </tr>\n" +
            "              <tr>\n" +
            "                <th><p style=\"margin-bottom: 0 !important;font-size: 25px;margin-top: 15px\">Your Result:</p></th>\n" +
            "              </tr>\n" +
            "              <tr>\n" +
            "                <th colspan=\"2\">\n" +
            "                  <p style=\"padding: 10px 0; width: 550px; overflow-wrap: break-word\">"+res+"</p>\n" +
            "                </th>\n" +
            "              </tr>\n" +
            "            </table>"
        $("#message-pre").append("<div class=\"d-flex flex-row bd-highlight\"><p class=\"answer\">"+res+"</p></div>")
    })
}

function flash_question(){
    var que_in = document.getElementById("question")

    $.post('/nlp', {
        'que': que_in.value
    }).done(function (response) {
        var ans = response['ans']
        var que = que_in.value
        que_in.value = ""
        // $("#message-pre").append("<div class=\"d-flex flex-row bd-highlight\"><p class=\"answer\">"+ans+"</p></div>\n" +
        //     "            <div class=\"d-flex flex-row-reverse bd-highlight\"><p class=\"question\">"+que+"</p></div>" +
        //     "           ")
        $("#message-pre").append("<div class=\"d-flex flex-row-reverse bd-highlight\"><p class=\"question\">"+que+"</p></div>\n" +
            "            <div class=\"d-flex flex-row bd-highlight\"><p class=\"answer\">"+ans+"</p></div>")
        var modal_dialog = document.getElementById("message")
        modal_dialog.scrollTop=modal_dialog.scrollHeight
    }).fail(function (){
        alert("nonononono")
    })
}