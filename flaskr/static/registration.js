// $(function(){
  // var hash = window.location.hash;
  // hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  // $('.nav-tabs a').click(function (e) {
    // $(this).tab('show');
    // var scrollmem = $('body').scrollTop() || $('html').scrollTop();
    // window.location.hash = this.hash;
    // $('html,body').scrollTop(scrollmem);
  // });
// });
$(document).ready(function() { 
	
	$('input:password + .glyphicon').on('click', function() {
  		$(this).toggleClass('glyphicon-eye-close').toggleClass('glyphicon-eye-open'); // toggle our classes for the eye icon
  		var password = $(this).prev($('input:password'));
  		togglePassword(password); // activate the hideShowPassword plugin
	});
	$('#forgot-pass').on('click', function() {
		$('#secret_word_div').show();
		$('#input_password').hide();
	});
	$('#signUpbutton').on('click', function() { 
		registration();
	});
	$('#signInbutton').on('click', function() {
		login();
	});
})
	function togglePassword(pass) {
		
			var type = pass.attr("type"); 
			if (type === 'password')
		{
			pass.attr("type","text");			
		}
		else
		{
  			pass.attr("type", "password");
		} 

	}
function registration()
	{
		$.ajax({
		type: "POST", 
		url: "/registration",
		data: {login: $('#inputLogin2').val(), pass: $('#inputPassword2').val(), secretWord: $('#secretWord').val()},
		success: function(data){
			alert('Регистрация выполнена успешно!');
			location.reload();

		}
		//error: function(response) { // Данные не отправлены
            // document.getElementById(result_form).innerHTML = "Ошибка. Данные не отправленны.";
			// alert('Ошибка при регистрации!');
        //}
	});
	}
function login()
	{
		$.ajax({
		type: "POST", 
		url: "/loginRequest",
		
		data: {login: $('#inputLogin').val(), pass: $('#inputPassword').val(), secretWord: $('#secretWord').val()},
		success: function(data){
			alert('Вход выполнен');
			window.location.href = "/";
		}
		//error: function(response) { // Данные не отправлены
            // document.getElementById(result_form).innerHTML = "Ошибка. Данные не отправленны.";
			// alert('Ошибка при регистрации!');
        //}
	});
	}
