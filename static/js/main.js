//                                  navbar expend

$(document).ready(function(){
    $('.loading').fadeOut(500)
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
            $.ajax({
                url: '/',
                type: 'POST',
                data: {'regiInput': reg, 'select': $('#select').val()},
                success: function(value){
                    $('.container').html(value)
                }
            })
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

//                                          CGPA calculator

$(document).ready(function(){
    $("#subject-number").change(function(){
        var gArr = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        $('#subject-inputs').empty()
        $('#hiddenHelp').addClass('show')
        for(i=0; i<$(this).val(); i++){
            var data = "<div style=\"margin-bottom: 10px\">\
                            <div class=\"row\">\
                                <div class=\"col\" style=\"text-align:right\"><span>"+ gArr[i] +" :</span></div>\
                                <div class=\"col\"><input type=\"text\" class=\"form-control form-control-sm\" name=\""+gArr[i]+"\"></div>\
                                <div class=\"col\"><input type=\"text\" class=\"form-control form-control-sm\" name=\""+gArr[i]+"-c\"></div>\
                            </div>\
                        </div>"
            $('#subject-inputs').append(data)
        }
    })
})