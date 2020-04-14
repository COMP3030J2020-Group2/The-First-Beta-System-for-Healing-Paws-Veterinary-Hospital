var ongoing = document.getElementById('ongoing');
ongoing.onclick=function () {
    var td_id = document.getElementById('apm_id');
    var id = td_id.textContent;
    location.href = '/appointment_ongoing/'+id;
};
var finish = document.getElementById('finish');
finish.onclick=function () {
    var td_id = document.getElementById('apm_id');
    var id = td_id.textContent;
    location.href = '/appointment_finish/'+id;
};