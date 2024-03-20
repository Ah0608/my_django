// 禁止获取验证码按钮
document.getElementById("sendButton").disabled = true;

document.getElementById("email").addEventListener("input", function () {
    // 获取邮箱输入框的值
    var emailInput = document.getElementById("email").value;
    console.log(emailInput)

    if (emailInput.trim() !== "") {
        document.getElementById("sendButton").disabled = false;
    }
});

// 检查用户名是否可用
$(document).ready(function () {
    $('#username').on('input', function () {
        var username = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/checkusername/',
            data: {
                'username': username
            },
            dataType:"json",
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
        var password = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/verifypassword/',
            data: {
                'password': password
            },
            dataType:"json",
            success: function (response) {
                console.log(response)
                if (response.flag) {
                    $('#password_feedback').text(response.message);
                } else {
                    $('#password_feedback').text(response.message);
                }
            }
        });
    });
});

function sendEmail() {
    var emailInput = document.getElementById('email');
    var email = emailInput.value;
    console.log(email)
    $.ajax({
        url: '/sendmeail/',
        type: 'POST',
        data: {
            'email': email
        },
    });
    // 倒计时60秒
    var seconds = 60;
    var countdownElement = document.getElementById('countdown');
    var countdownInterval = setInterval(function () {
        seconds--;
        countdownElement.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(countdownInterval);
            countdownElement.textContent = '';
            sendButton.disabled = false; // 启用发送按钮
        }
    }, 1000);
}