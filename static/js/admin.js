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
                if(res.error.errors[0].message == "EMAIL_NOT_FOUND"){
                    $('#invalidEmail').html('Email not found').css({'color': 'red'})
                    $('#invalidPasswd').css({'display': 'none'})
                }
                else if(res.error.errors[0].message == "INVALID_PASSWORD"){
                    $('#invalidEmail').css({'display': 'none'})
                    $('#invalidPasswd').html('Invalid Password').css({'color': 'red'})
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