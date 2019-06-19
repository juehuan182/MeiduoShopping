var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        is_show_waiting: true,

        error_password: false,
        error_phone: false,
        error_email_code: false,
        error_email_message: '',
        error_email_code_message: '',

        email_code_tip: '获取邮箱验证码',
        sending_flag: false, // 正在发送邮件标志

        password: '',
        email: '',
        email_code: '',
        bind_token: ''
    },
    mounted: function () {  // 在模板渲染成html后调用，通常是初始化页面完成后，再对html的dom节点进行一些需要的操作。
        // 从路径中获取qq重定向返回的code
        var code = this.get_query_string('code'); // 要获取到的Authorization Code值
        var state = this.get_query_string('state');
        console.log(code, state);
        axios.get(this.host + '/oauth/qq/user/?code=' + code + '&state=' + state, {
            responseType: 'json',
        }).then(response => {
            if (response.data.user_id) {
                // 用户已绑定
                sessionStorage.clear();
                localStorage.clear();
                localStorage.user_id = response.data.user_id;  // 保存在浏览器本地存储中
                localStorage.username = response.data.username;
                localStorage.token = response.data.token;
                location.href = state;  // 跳转到state
            } else {
                // 用户未绑定
                alert(response.data.bind_token);
                this.bind_token = response.data.bind_token;
                this.is_show_waiting = false;
            }
        }).catch(error => {
            console.log(error.response);
            alert('服务器异常');
        })
    },
    methods: {
        // 获取url路径参数    
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        // 生成uuid
        generate_uuid: function () {
            var d = new Date().getTime();
            if (window.performance && typeof window.performance.now === "function") {
                d += performance.now(); //use high-precision timer if available
            }
            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = (d + Math.random() * 16) % 16 | 0;
                d = Math.floor(d / 16);
                return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
            return uuid;
        },
        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_email: function () {
            var re = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
            if (re.test(this.email)) {
                this.error_email = false;
            } else {
                this.error_email_message = '您输入的邮箱格式不正确';
                this.error_email = true;
            }
        },
        check_email_code: function () {
            if (!this.email_code) {
                this.error_email_code_message = '请填写邮箱验证码';
                this.error_email_code = true;
            } else {
                this.error_email_code = false;
            }
        },
        // 发送邮箱验证码
        send_email_code: function () {
            if (this.sending_flag == true) {
                return;
            }
            this.sending_flag = true;

            // 校验参数，保证输入框有数据填写
            this.check_email();

            if (this.error_email == true) {
                this.sending_flag = false;
                return;
            }

            // 向后端接口发送请求，让后端发送短信验证码
            axios.get(this.host + '/verifications/email_codes/' + this.email + '/', {
               params:{
                    send_type: 'bindAccount'
               }
            }, {
                responseType: 'json'
            })
                .then(response => {
                    // 表示后端发送短信成功
                    // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                    var num = 60;
                    // 设置一个计时器
                    var t = setInterval(() => {
                            if (num == 1
                            ) {
                                // 如果计时器到最后, 清除计时器对象
                                clearInterval(t);
                                // 将点击获取验证码的按钮展示的文本回复成原始文本
                                this.email_code_tip = '获取短信验证码';
                                // 将点击按钮的onclick事件函数恢复回去
                                this.sending_flag = false;
                            } else {
                                num -= 1;
                                // 展示倒计时信息
                                this.email_code_tip = num + '秒';
                            }
                        },
                        1000, 60
                    )
                })
                .catch(error => {
                    console.log(error.response.data);
                    this.sending_flag = false;
                })
        },
        // 保存
        on_submit: function () {
            this.check_pwd();
            this.check_email();
            this.check_email_code();

            if (this.error_password == false &&
                this.error_email == false &&
                this.error_email_code == false) {
                axios.post(this.host + '/oauth/qq/user/', {
                    password: this.password,
                    email: this.email,
                    email_code: this.email_code,
                    bind_token: this.bind_token,
                    login_type: '1'
                }, {
                    responseType: 'json',
                })
                    .then(response => {
                        // 记录用户登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage.token = response.data.token;
                        localStorage.user_id = response.data.id;
                        localStorage.username = response.data.username;
                        location.href = this.get_query_string('state');
                    })
                    .catch(error => {
                        if (error.response.status == 400
                        ) {
                            this.error_email_code_message = error.response.data.message;
                            this.error_email_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        }
    }
});