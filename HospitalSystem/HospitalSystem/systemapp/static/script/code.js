/*signup*/
var regPassword = /^\S{8,}$/;
var spanPassword = document.querySelector('#validation_password');
if(spanPassword!=null){
	function checkPassword(){
	    var input = password.value;

	    if(input == ""){
	        spanPassword.innerHTML="This field is required";
	        spanPassword.style.color = 'red';
	        return false;
	    }else{
	        if(!regPassword.test(input)){
	            spanPassword.innerHTML = "At least 8 digits, space is not allowed";
	            spanPassword.style.color = 'red';
	            return false;
	        }else{
	            spanPassword.innerHTML="Correct Format";
	            spanPassword.style.color = 'green';
	            return true;
	        }  
	    }
	    
	}	
}


var password2 = document.querySelector('#password2');
var spanPassword2 = document.querySelector('#validation_password2');
function checkEqualPassword(){
    var input = password.value;
    var input2 = password2.value;

    if(input2 == ""){
        spanPassword2.innerHTML="This field is required";
        spanPassword2.style.color = 'red';
        return false;
    }else{
        if(input == input2){
            spanPassword2.innerHTML="Equal";
            spanPassword2.style.color = 'green';
            return true;
        }else{
            spanPassword2.innerHTML="Password does not match";
            spanPassword2.style.color = 'red';
            return false;

        }
    }
    
}

var form = document.querySelector('#signup_form');
if(form!=null){
	form.onsubmit = function(){
	    console.log('submit');
	    var username = checkUsernameFormat();
	    var password = checkPassword();
	    var email = checkEmailFormat();
	    var equal = checkEqualPassword();
	    if(username && password && email && equal){
	        return true;
	    }else{
	        return false;
	    }
    
	}
}

if(password2!=null){
	password2.onmouseover = function(){
    	password2.style.borderColor = 'blue';

	}
	password2.onmouseout = function(){
    	password2.style.borderColor = 'black';
    
	}
}

/* username and email format*/
var regEmail = /^[a-zA-Z][a-zA-Z0-9_@\-\!\?]*@[a-zA-Z0-9]+.[a-z]+/;
var spanEmail = document.querySelector('#validation_email');
function checkEmailFormat(){
    var input = email.value;

    if(input == ""){
        spanEmail.innerHTML="This field is required";
        spanEmail.style.color = 'red';
        return false;
    }else{
        if(!regEmail.test(input)){
            console.log('not match');
            spanEmail.innerHTML = "Please enter correct format : xxxxx@xxx.xx";
            spanEmail.style.color = 'red';
            return false;
        }else{
            console.log('match');
            spanEmail.innerHTML="Correct Format";
            spanEmail.style.color = 'green';
            return true;
        }  
    }
    
}

var regUsername = /^[a-zA-Z][\S]{4,}_*$/;
var spanUsername = document.querySelector('#validation_username');
if(spanUsername!=null){
	function checkUsernameFormat(){
    	var input = username.value;
   		 if(input == ""){
       	 	spanUsername.innerHTML="This field is required";
        	spanUsername.style.color = 'red';
        	return false;
    	}else{
       		if(!regUsername.test(input)){
            	spanUsername.innerHTML = "Begin with character! At least 5 digits, no Space";
            	spanUsername.style.color = 'red';
            	return false;
        	}else{
            	spanUsername.innerHTML="Correct Format";
             	spanUsername.style.color = 'green';
            	return true;
        	}
    	}
	}
}



/*check duplicate email ans username*/

$(document).ready(function(){
	$("#email").on("change", check_email);
	$("p.signup>input").on("change", check_username);
	console.log("function registered");
});

function check_username(){
	var correctFormat = checkUsernameFormat();
	if(correctFormat){
		console.log("check_username called");
		var chosen_user = $("p.signup>input");
		console.log("User chose: " + chosen_user.val());	
		$.post('/checkuser', {
			'username': chosen_user.val()
		}).done(function (response){
			var server_response = response['text']
			var server_code = response['returnvalue']
			if (server_code == 0){ 
				$("#password").focus();
				$("#validation_username").html('<span>' + "Correct Format and "+server_response + '</span>');
				$("#validation_username").css("color","green");
			}else{ 
				chosen_user.val("");
				chosen_user.focus();
				$("#validation_username").html('<span>' + "Correct Format but "+server_response + '</span>');
			}
		}).fail(function() {
			$("#validation_username").html('<span>Error contacting server</span>');
		});

	
		console.log("finished check_username");
	}
}

function check_email(){
	var correctFormat = checkEmailFormat();
	if(correctFormat){
		var chosen_email = $("#email");
		$.post('/checkemail', {
			'email': chosen_email.val() 
		}).done(function (response){
			var server_response = response['text']
			var server_code = response['returnvalue']
			if (server_code == 0){ 
				$("#password").focus();
				$("#validation_email").html('<span>' +"Correct Format and "+server_response + '</span>');
			}else{ 
				chosen_email.val("");
				chosen_email.focus();
				$("#validation_email").html('<span>' + "Correct Format but "+server_response + '</span>');
			}
		}).fail(function() {
			$("#validation_email").html('<span>Error contacting server</span>');
		});
	}
}

