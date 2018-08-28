/**
 * Created by John Smith on 05.12.2017.
 */

function getCookie(name){
    var cookieValue = null;
    if (document.cookie && document.cookie !== ''){
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++){
            var cookie = jQuery.trim(cookies[i]);
            if (cookies.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue
}


// Настройка AJAX

$(function () {
    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });
});


function to_follow() {

    var current = $(this);
    var pk = current.data('id');
    var action = current.data('action');
    var username = current.data('username');

    $.ajax({
        url : username + '/' + action + '/',
        type : 'POST',
        data : { 'obj' : pk},

        success : function (json) {
            current.find("[data-count='following']").text(json.following_count);
            current.find("[data-count='followers']").text(json.followers_count);
        }
    });
    return false;
}

$(function () {
    $('[data-action="follow"]').click(to_follow())
})