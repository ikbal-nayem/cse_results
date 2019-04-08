$(document).ready(function(){
    $('#createTables').on('click', function(){
        $(this).addClass('disabled')
        res = $.ajax({
            url: '/admin/create-tables',
            type: 'POST',
        });
        res.done(function(data){
            $('.hidden-msg').css({'visibility': 'visible', 'display':'inline'});
        });
    });
});

$(document).ready(function(){
    $('#loginForm').on('submit', function(event){
        if($(this).attr("success")){
            return true
        }
        res = $.ajax({
            url: '/login',
            type: 'POST',
            data: {'email':$('#loginEmail').val(), 'passwd': $('#loginPasswd').val()}
        })
        res.done(function(res){
            if(res.error){
                if(res.error.message == "EMAIL_NOT_FOUND"){
                    $('#invalidEmail').html('Invalid email').css({'color': 'red'})
                    $('#invalidPasswd').css({'display': 'none'})
                }
                else{
                    $('#invalidPasswd').html('Invalid Password').css({'color': 'red'})
                    $('#invalidEmail').css({'display': 'none'})
                }
            }
            else{
                $('#invalidEmail').css({'display': 'none'})
                $('#invalidPasswd').css({'display': 'none'})
                $("#loginForm").attr("success",true);
                $("#loginForm").submit()
            }
        })
        event.preventDefault()
    })
})