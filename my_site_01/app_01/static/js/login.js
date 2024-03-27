$('.captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
    });
});


// axios.post('/api/login/', { username, password })
//     .then(response => {
//         const { access, refresh, message } = response.data;
//         // 存储令牌到本地存储或Cookie中
//         localStorage.setItem('access_token', access);
//         localStorage.setItem('refresh_token', refresh);
//         alert(message); // 可以显示登录成功的提示信息
//         // 导航至登录成功后的页面
//         window.location.href = '/protected_page';
//     })
//     .catch(error => {
//         console.error(error);
//         alert('登录失败，请检查用户名和密码');
//     });
