/*login*/
let form = document.querySelector('#staff_login_form');
form.onsubmit = function(){
    console.log('staff login submit');
    let sn = validUsername();
    let pw = validPassword();
    return sn && pw;
};


let noticeUsername = document.querySelector('#notice_staffname');
function validUsername(){
	let input = form.username.value;
	 if(input === ""){
		noticeUsername.innerHTML="Enter staff name please.";
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