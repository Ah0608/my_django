// 禁止获取验证码按钮
$("#sendButton").prop("disabled", true);

// 检查邮箱格式
$(document).ready(function () {
    $('#email').on('input', function () {
        const email = $(this).val();
        console.log(email)
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (emailPattern.test(email)) {
            $("#sendButton").prop("disabled", false);
            $("#email_error").text('')
        } else {
            $("#sendButton").prop("disabled", true);
            $("#email_error").text('请输入正确的邮箱')
        }
    })
});

// 检查用户名是否可用
$(document).ready(function () {
    $('#username').on('blur', function () {
        const username = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/checkusername/',
            data: {
                'username': username
            },
            dataType: "json",
            success: function (response) {
                if (response.flag) {
                    $('#username_feedback').text(response.message);
                } else {
                    $('#username_feedback').text(response.message);
                }
            }
        });
    });
});

// 检查密码是否合法
$(document).ready(function () {
    $('#password').on('input', function () {
        const password = $(this).val();
        const regexDigit = /\d/;
        const regexLetter = /[a-zA-Z]/;
        if (regexDigit.test(password) && regexLetter.test(password)) {
            if (password.length >= 8 && password.length <= 16) {
                $('#password_feedback').text('密码合法');
            } else {
                $('#password_feedback').text('密码长度应在8到16之间');
            }
        } else {
            $('#password_feedback').text('密码须同时包含至少一个字母和一个数字');
        }
    });
});

// 检查两次输入的密码是否相同
$(document).ready(function () {
    $('#confirm_pwd').on('input', function () {
        const password = $('#password').val();
        const confirm_pwd = $(this).val();
        if (password !== confirm_pwd) {
            $('#password_error').text('两次输入的密码不一样');
        } else {
            $('#password_error').text('');
        }
    });
});

// 发送邮箱验证码
function sendEmail() {
    const email = $('#email').val();
    console.log(email);
    $.ajax({
        url: '/sendmeail/',
        type: 'POST',
        data: {
            'email': email
        },
        success: function (response) {
            if (response.flag) {
                $('#email_error').text(response.message);
                // 倒计时60秒
                var seconds = 60;
                const countdownElement = $('#countdown');
                const countdownInterval = setInterval(function () {
                    seconds--;
                    countdownElement.text(seconds);
                    if (seconds <= 0) {
                        clearInterval(countdownInterval);
                        countdownElement.text('');
                        $('#sendButton').prop('disabled', false); // 启用发送按钮
                    }
                }, 1000);
            } else {
                $('#email_error').text(response.message);
            }
        }
    });
}
