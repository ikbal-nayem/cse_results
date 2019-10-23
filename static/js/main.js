//                                              navbar

$(document).ready(function(){
    $('.loading').fadeOut(500)

    //                                       navbar extend

    $('#navBar').on('click', function(){
        $(this).attr('aria-expanded') ? $(this).attr('aria-expanded', 'false') : $(this).attr('aria-expanded', 'true')
        $(this).toggleClass('collapsed')
        $('#navbarColor02').toggleClass('show')
    })

    //                                     navbar list active

    $('nav ul li').click(function(){
        $('nav ul li').removeClass('active')
        $(this).addClass('active')
    })
    if(window.location.pathname.split('/')[1] === ''){
        $('nav ul #result').addClass('active')
    }
    else{
        $('nav ul li').removeClass('active')
        $('nav ul #'+ window.location.pathname.split('/')[1]).addClass('active')
    }
})

//                          check registration number and result

$(document).ready(function(){
    var error = function(id, msg){
        $(id).addClass('is-invalid')
        $(id).next().html(msg).addClass('error-alert')     
    }
    var success = function(id, msg=''){
        $(id).removeClass('is-invalid')
        $(id).next().html(msg).removeClass('error-alert')
    }

    $('#resultInfo').on('submit', function(event){
        if($(this).attr("success")){
            return true
        }
        event.preventDefault()
        var reg = $('#reg_no').val()
        if(!$.isNumeric(reg)){
            $('#reg_no').addClass('is-invalid')
            $('.alart').html("Invalid registration number.").addClass("error-alert")
        }else{
            $('.alart').html('Finding result...').removeClass("error-alert")
            $('#reg_no').removeClass('is-invalid')
            $('#resultInfo').attr("success", true)
            $(this).submit()
        }
    })

    $('#btnGroupDrop').on('click', function(){
        $('#'+$(this).attr('data-target')).slideToggle()
    })

    $('#getEmail').on('submit', function(event){
        reg = $('#reg_no').val()
        email = $('#putEmail').val()
        event.preventDefault()
        $.ajax({
            url: '/subscribe',
            type: 'POST',
            data: {'reg_no': reg, 'email': email},
            success: function(value){
                if(value.submitted){
                    $('#subscribtion').slideUp('slow').html(value.htmlValue).slideDown('slow')
                }else{
                    error('#putEmail', 'Email is used before.')
                }
            }
        })
    })
})

//                                  login check  

$(document).ready(function(){
    $('#loginForm').on('submit', function(event){
        $('#login-btn').addClass('disabled').html('<span id="checking"></span> Checking...')
        $('#checking').addClass('spinner-border spinner-border-sm')
        $('#invalidEmail').removeClass('show')
        $('#invalidPasswd').removeClass('show')
        $('#loginEmail').removeClass('is-invalid')
        $('#loginPasswd').removeClass('is-invalid')
        if($(this).attr("success")){
            return true
        }else{
            event.preventDefault()
            $.ajax({
                url: '/login',
                type: 'POST',
                data: {'email':$('#loginEmail').val(), 'passwd': $('#loginPasswd').val()},
                success: function(resp){
                    $('#login-btn').removeClass('disabled').html('<span id="checking"></span> Login')
                    $('#checking').removeClass('spinner-border spinner-border-sm')
                    if(resp === "EMAIL_NOT_FOUND"){
                        $('#loginEmail').addClass('is-invalid')
                        $('#invalidEmail').html('Email not found').addClass('show')
                    }else if(resp === "INVALID_PASSWORD"){
                        $('#loginPasswd').addClass('is-invalid')
                        $('#invalidPasswd').html('Invalid Password').addClass('show')
                    }else if(resp === false){
                        alert("somethimg was wrong!")
                    }
                    else{
                        $('#loginForm').attr("success", true)
                        $("#loginForm").submit()
                    }
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


//                                      search student

$(document).ready(function(){
    var error = function(id, msg, disabled=true){
        $(id).html(msg).addClass('error-alert')
        $(id).prev().addClass('is-invalid')
        $('#autocomplete').attr('disabled', disabled)     
    }
    var success = function(id, msg=''){
        $(id).html(msg).removeClass(error-alert)
        $(id).prev().removeClass('is-invalid')
        $('#autocomplete').removeAttr('disabled')
    }
    var stdList = []
    var get_list = function(data){ stdList = data }
    $('#batch').keyup(function(){
        if($.isNumeric($('#batch').val())){
            success('#batchErr')
        }else{
            error('#batchErr', 'Batch number should be numaric form.')
        }
    })
    $('#autocomplete').on('focus',function(){
        $.ajax({
            url: '/result/find',
            type: 'POST',
            data: {'batch' : $('#batch').val()},
            success: function(list){
                if(list==[]){
                    error('#batchErr', 'No student found of this batch.')
                }else{
                    success("#batchErr")
                    $("#autocomplete").autocomplete({
                        source: list,
                        autoFocus: true,
                        classes: {
                            'ui-autocomplete': 'autocomplete',
                        }
                    })
                get_list(list)
                }
            }
        })
    })
    $('#autocomplete').on('change', function(){
        if(stdList.indexOf($('#autocomplete').val()) == -1){
            error('#nameErr', 'Select name from suggestion list', false)
        }else{
            success('#nameErr')
            $.ajax({
                url: '/result/find',
                type: 'POST',
                data: {
                    'batch': $('#batch').val(),
                    'name': $('#autocomplete').val()
                },
                success: function(reg){
                    $('#reg').val(reg.reg_no)
                }
            })
        }
    })
});