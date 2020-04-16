var submit = document.getElementById('searchsubmit');
var input = document.getElementById('search');
submit.onclick= function temp() {
  var str = input.value;
  location.href='staff_search/'+str;
};