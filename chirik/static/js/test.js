/**
 * Created by John Smith on 28.11.2017.
 */

$('#id_username').change(function () {
        var username = $(this).val();

        $.ajax({
            url: 'ajax/validate_username/',
            data: { 'username': username},
            dataType: 'json',
            success: function (data) {
                if (data.is_taken){
                    alert ("A user with this username already exists");
                }
            }
        });
    });