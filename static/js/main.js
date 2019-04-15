//                                  navbar expend

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

//                          check registration number

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

//                                  login check  

$(document).ready(function(){
    $('#loginForm').on('submit', function(event){
        if($(this).attr("success")){
            return true
        }else{
            event.preventDefault()
            res = $.ajax({
                url: '/login',
                type: 'POST',
                data: {'email':$('#loginEmail').val(), 'passwd': $('#loginPasswd').val()}
            })
            res.done(function(resp){
                if(resp.error){
                    if(resp.error.errors[0].message === "EMAIL_NOT_FOUND"){
                        $('#invalidEmail').html('Email not found').css({'color': 'red'})
                        $('#invalidPasswd').css({'display': 'none'})
                    }else if(resp.error.errors[0].message === "INVALID_PASSWORD"){
                        $('#invalidEmail').css({'display': 'none'})
                        $('#invalidPasswd').html('Invalid Password').css({'color': 'red'})
                    }
                }else{
                    $('#invalidEmail').css({'display': 'none'})
                    $('#invalidPasswd').css({'display': 'none'})
                    $("#loginForm").attr("success",true);
                    $("#loginForm").submit()
                }
            })
        }
    })
})