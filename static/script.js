(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#form_submit').click(
        function () {
            data = {
                login: $('#id_login').val(),
                password: $('#id_password').val()
            };
            if (data.login != '' && data.password != '') {
                $.post('/user/', data).done(function (s) {
                    $('#error').text('');
                    $('#user').text('Hello ' + s.login);
                    $('#myModal').modal('hide');
                    $('button').hide();
                }).fail(function (e) {
                    $('#error').text(e.responseText)
                })
            }
            else {
                $('#error').text('all fields is required');
            }
        }
    )
})();
