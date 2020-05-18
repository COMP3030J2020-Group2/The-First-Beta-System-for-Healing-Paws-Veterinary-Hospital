var submit = document.getElementById('searchlink');
var input = document.getElementById('search');
submit.onclick= function search() {
  var str = input.value;
  submit.href='staff_search/'+str;
};