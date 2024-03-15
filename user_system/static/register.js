
function submit() {
	// if (check_username() && check_password() && check_email()) {
		var email = $("#id_email").val();
		// if (email == "")
		// {
		// 	alert("email must not be empty");
		// 	return;
		// }

		var username = $("#id_username").val();
		// if (username == "")
		// {
		// 	alert("username must not be empty");
		// 	return;
		// }
		var password = $("#id_password").val();
		// if (password == "")
		// {
		// 	alert("password must not be empty");
		// 	return;
		// }
		// if (password != $("#confirm_password").val())
		// {
		// 	alert("password not the same");
		// 	return;
		// }
		/** @type {HTMLParagraphElement} */
		$("#result").text(email + " | " + username + " | " + password);

		// $("#submit").
		// jq
		// $.post("url", data,
		// 	function (data, textStatus, jqXHR) {
				
		// 	},
		// 	"dataType"
		// );
		
		//alert("parent_email:" + parent_email);
		// 1,获取csrfmiddlewaretoken的input标签value属性对应的值
		// { #var token = $('[name="csrfmiddlewaretoken"]').val();# }
		// 2,直接就能得到 csrfmiddlewaretoken 的input标签value属性的值
		// var csrf_token = '{{ csrf_token }}';
		// alert("submit");
		/*$.post("/study_system/register/",
			{
				'role': role,
				'username': username,
				'password': password,
				'email': email,
				'parent_email': parent_email,
				// 将token值放到请求数据部分,token的键必须是 csrfmiddlewaretoken
				'csrfmiddlewaretoken': csrf_token,
			}, function (data) {
				if ("success" == data.result) {
					alert("注册成功");
					// 注册成功，去登录页面
					window.location.href = "/study_system/login/";
				} else {
					alert("注册失败:" + data.errorMsg);
				}
			});*/
	// }
}
$(document).ready(function () {
	$("#submit").click(submit);
});

