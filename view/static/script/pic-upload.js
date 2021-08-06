$(document).ready(function() {
    $("#pic-p").on("change", upload_pic);
    $("#subque").on("click", flash_question);
})

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

function upload_pic(){
    var p = document.getElementById("pic").files[0]
    var pic = getObjectURL(p);

    $.post('/i', {
        'pic': pic
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
            "                  <p style=\"padding: 10px 0\">"+res+"</p>\n" +
            "                </th>\n" +
            "              </tr>\n" +
            "            </table>"
    }).fail(function (){
        alert("server error")
    })
}

function upload_pic_plus() {
    let formData = new FormData($("#pic")[0])
        console.log('点击提交之后，打印FormData中的数据')
        console.log(formData.get('pic'))
        $.ajax({
            url: 'http://127.0.0.1:5000/i',
            type: 'POST',
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: function(returndata) {
                alert(returndata);
            },
            error: function(error) {
                alert(error);
            }
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
        alert("server error")
    })
}