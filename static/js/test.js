/**
 * Created by John Smith on 28.11.2017.
 */
alert ('test1');

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
   $('[data-action="follow"]').click(to_follow)
})
