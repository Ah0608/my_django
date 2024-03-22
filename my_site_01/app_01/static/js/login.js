$('.captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
    });
});
$(document).ready(function () {
    $('.form-login').on('submit', function (event) {
        console.log(111)
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/login/',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.flag) {
                    console.log(response.message)
                    location.href = 'http://127.0.0.1:8000/index/'
                } else {
                    console.log(response.message)
                    $('.tips').text(response.message);
                    setTimeout(function () {
                        location.reload();
                    }, 3000);
                }
            }
        })
    })
});
