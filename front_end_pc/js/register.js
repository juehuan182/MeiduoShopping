var vm = new Vue({
    el: '#app',
    data: {
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_email: false,
        error_allow: false,
        error_email_code: false,

        username: '',
        password: '',
        password2: '',
        email: '',
        email_code: '',
        allow: true,

        send_flag: false,
        email_code_tip: '获取邮箱验证码',
        email_code_error_tip: '邮箱验证码错误',
        host: host,
    },
    mounted: function () { //mounted:在模板渲染成html后调用，通常是初始化页面完成后，再对html的dom节点进行一些需要的操作。
        //this.generate_image_code();
    },
    methods: {
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name = true;
            } else {
                this.error_name = false;
            }

            // 检查重名，向后台发起请求
            if (this.error_name == false) {
                axios.get(this.host + '/users/usernames/' + this.username + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_cpwd: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },
        check_email: function () {
            var re = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
                    
            if (re.test(this.email)) {
                this.error_email = false;
            } else {
                this.error_email = true;
            }

            if (this.error_email == false) {
                axios.get(this.host + '/users/emails/' + this.email + '/count/', {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_email_message = '邮箱已存在';
                        } else {
                            this.error_email = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
        check_email_code: function () {
            if (!this.email_code) {
                this.error_email_code = true;
            } else {
                this.error_email_code = false;
            }
        },
        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        // 注册
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_email();
            this.check_email_code();
            this.check_allow();

            if (this.error_name == false &&
                this.error_password == false &&
                this.error_check_password == false &&
                this.error_email == false &&
                this.error_email_code == false &&
                this.error_allow == false) {
                axios.post(this.host + '/users/', {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    email: this.email,
                    email_code: this.email_code,
                    allow: this.allow.toString()
                }, {
                    responseType: 'json'
                })
                    .then(response => {
                        // 记录用户的登录状态
                        sessionStorage.clear();
                        localStorage.clear();
                        localStorage.token = response.data.token;
                        localStorage.username = response.data.username;
                        localStorage.user_id = response.data.id;
                        location.href = '/index.html';
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_email_code_message = error.response.data.non_field_errors[0];
                            } else {
                                this.error_email_code_message = '数据有误';
                            }
                            this.error_email_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
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
        //发送邮件验证码
        send_email_code: function () {
            if (this.send_flag == true) {
                return;
            }
            this.send_flag = true;

            this.check_email();

            if (this.error_email) {
                this.send_flag = false;
                return;
            }
           
            axios.get('http://127.0.0.1:8000/verifications/email_codes/' + this.email + '/',{
                params: {
                    send_type: 'register'
                }
            })
                .then(response => {
                    var num = 60;
                    var t = setInterval(function () {
                        if (num == 1) {
                            clearInterval(t);
                            vm.email_code_tip = '获取短信验证码';
                            vm.send_flag = false;
                        } else {
                            num -= 1;
                            vm.email_code_tip = '再过 ' + num + ' 秒后发送';
                        }
                    }, 1000);
                })
                .catch(error => {
                    this.send_flag = false;
					console.log(error.response.data);
                });
        }
    }
});
