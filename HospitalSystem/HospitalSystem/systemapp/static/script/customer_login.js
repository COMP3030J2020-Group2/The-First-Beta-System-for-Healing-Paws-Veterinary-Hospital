/*login*/
let form = document.querySelector('#customer_login_form');
console.log('hahah');
form.onsubmit = function(){
    console.log('customer login submit');
    let un = validUsername();
    let pw = validPassword();
    return un && pw;
};


let noticeUsername = document.querySelector('#notice_username');
function validUsername(){
	let input = form.username.value;
	 if(input === ""){
		noticeUsername.innerHTML="Enter your username please.";
		noticeUsername.style.color = 'blue';
		return false;
	}else{
	 	noticeUsername.innerHTML="";
	 	return true;
	}
}

let noticePassword = document.querySelector('#notice_password');
function validPassword(){
	let input = form.password.value;
	 if(input === ""){
		noticePassword.innerHTML="Enter your password please.";
		noticePassword.style.color = 'blue';
		return false;
	}else{
	 	noticePassword.innerHTML="";
	 	return true;
	}
}