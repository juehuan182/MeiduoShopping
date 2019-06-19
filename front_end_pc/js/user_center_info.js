var vm = new Vue({
    el: '#app',
    data: {
        host,
        user_id: sessionStorage.user_id || localStorage.user_id, // 获取本地存储的
        token: sessionStorage.token || localStorage.token,
        username: '',
        mobile: '',
        email: '',
        email_active: false,
        set_email: false,
        send_email_btn_disabled: false,
        send_email_tip: '重新发送验证邮件',
        email_error: false,
        histories: []
    },
    mounted: function () {
        // 判断用户的登录状态
        if (this.user_id && this.token) {
            axios.get(this.host + '/users/user/detail/', {
                // 向后端传递JWT token的方法
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
                .then(response => {
                    console.log(response);
                    // 加载用户数据
                    this.user_id = response.data.id;
                    this.username = response.data.username;
                    this.email = response.data.email;
                    // 补充请求浏览历史
                    axios.get(this.host + '/browse_histories/', {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                        .then(response => {
                            this.histories = response.data;
                            for (var i = 0; i < this.histories.length; i++) {
                                this.histories[i].url = '/goods/' + this.histories[i].id + '.html';
                            }
                        })
                })
                .catch(error => {
                    alert(error.response);
                    if (error.response.status == 401 || error.response.status == 403) {
                        location.href = '/login.html?next=/user_center_info.html';
                    }
                });
        } else {  // 如果没有登录，则跳转到登录界面
            location.href = '/login.html?next=/user_center_info.html';
        }
    },
    methods: {
        // 退出
        logout: function () {
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        // 保存email
        save_email: function () {
            // 保存email
            var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if (re.test(this.email)) {
                this.email_error = false;
            } else {
                this.email_error = true;
                return;
            }
            axios.put(this.host + '/emails/',
                {email: this.email},
                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.set_email = false;
                    this.send_email_btn_disabled = true;
                    this.send_email_tip = '已发送验证邮件'
                })
                .catch(error => {
                    alert(error.data);
                });
        }
    }
});