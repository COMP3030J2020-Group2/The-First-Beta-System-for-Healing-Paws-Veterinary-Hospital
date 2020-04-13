var search  = document.querySelector('#search');
function searching(){
    var input = search.value;
    if(input != null){
        $.post('/staff_search',{
            'query': input
        });
    }
}
var submit = document.querySelector('#searchsubmit');
submit.onClick(searching());