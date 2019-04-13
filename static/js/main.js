fileName = function(){
    var n = document.getElementById('inputFile').files[0].name
    document.getElementById('viewFileName').innerHTML = n
}
progressBar = function(){
    document.getElementById('progressBar').style.visibility = 'visible'
    document.getElementById('btnHelp').style.visibility = 'hidden'
    document.getElementById('btn').classList.add("disabled")
}

function drop() {
    document.getElementById("myDropdown").classList.toggle("show");
}
  
window.onclick = function(e) {
    if (!e.target.matches('.dropdown-toggle')) {
    var myDropdown = document.getElementById("myDropdown");
        if (myDropdown.classList.contains('show')) {
        myDropdown.classList.remove('show');
        }
    }
}

$(document).ready(function(){
    $('#navBar').on('click', function(){
        if($(this).attr('aria-expanded')==='true'){
            $(this).attr('aria-expanded', 'false')
        }else{
            $(this).attr('aria-expanded', 'true')
        }
        $(this).toggleClass('collapsed')
        $('#navbarColor02').toggleClass('show')
    })
})

$(document).ready(function(){
    $('#resultInfo').on('submit', function(event){
        if($(this).attr("success")){
            return true
        }
        event.preventDefault()
        var reg = $('#reg_no').val()
        if(!$.isNumeric(reg)){
            $('.alart').html("Invalid registration number.").addClass("error-alert")
        }else{
            $('.alart').removeClass("error-alert")
            $('#resultInfo').attr("success", true)
            $('#resultInfo').submit()
        }
    })
})