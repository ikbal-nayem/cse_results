//                                              navbar

$(document).ready(function(){
    $('.loading').fadeOut("slow")
    //                                       navbar extend

    $('#navBar').on('click', function(){
        $(this).attr('aria-expanded') ? $(this).attr('aria-expanded', 'false') : $(this).attr('aria-expanded', 'true')
        $(this).toggleClass('collapsed')
        $('#navbarColor02').toggleClass('show')
    })
    //                                    navbar list active

    $('nav ul li').click(function(){
        $('nav ul li').removeClass('active')
        $(this).addClass('active')
    })
    if(window.location.pathname.split('/').pop()){
        $('nav ul #'+ window.location.pathname.split('/').pop()).addClass('active')
    }
})

//                                    login  dropdown

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

//                                   Alert Box close

$(document).ready(function(){
    $('button.close').on('click', function(){
        $(this).parent().remove()
    })
})

//                                    update from NU

$(document).ready(()=>{
    $('#updateResults').on('submit', function(event){
        $('#update-btn').addClass('disabled').html('<span id="updating"></span> Updating...')
        $('#updating').addClass('spinner-border spinner-border-sm')
        $('#alert').addClass('hidden-msg')
        if($(this).attr('success')){
            return true
        }else{
            event.preventDefault()
            $.ajax({
                url: '/admin/update-db',
                type: 'POST',
                data: {
                    'batch': $('#batch').val(),
                    'semester': $('#semester').val(),
                    'xm-code': $('#xm-code').val(),
                    'xm-year': $('#xm-year').val(),
                },
                success: resp =>{
                    if (resp === 'updated'){
                        $('#tableCreated').text('Result successfully updated!').parent().removeClass('hidden-msg alert-warning').addClass('alert-success')
                    }else if (resp === 'registration_error'){
                        $('#tableCreated').text('No registration number found for this batch!').parent().removeClass('hidden-msg alert-success').addClass('alert-warning')
                    }else if(resp === 'xm_code_error'){
                        $('#tableCreated').text('Exam code or year error!').parent().removeClass('hidden-msg alert-success').addClass('alert-warning')
                    }else{
                        $('#tableCreated').text('Updating failed!').parent().removeClass('hidden-msg alert-success').addClass('alert-warning')
                    }
                    $('#update-btn').removeClass('disabled').html('Update now')
                }
            })
        }
    })
})

//                                      create table

$(document).ready(function(){
    $('#createTables').on('click', function(){
        $(this).addClass('disabled')
        res = $.ajax({
            url: '/admin/create-tables',
            type: 'POST',
        });
        res.done(function(){
            $('.hidden-msg').css({'visibility': 'visible', 'display':'inline'})
            // if(data.exception === true){
            //     $('.hidden-msg').css({'visibility': 'visible', 'display':'inline'})
            // }else if(data.exception === '1050'){
            //     $('#tableCreated').html('Tables are already created!');
            // }else{
            //     $('#tableCreated').html('Something was wrong creating tables!<br>check your database connection.');
            // }
        });
    });
});

//                                      year check

$(document).ready(function(){
    $('#uploadReslt').on('submit', function(event){
        if($(this).attr("success")){
            return true
        }
        event.preventDefault()
        var year = $('#year').val()
        if(!$.isNumeric(year)){
            $('#yearAlert').html("Year must be in numeric format.").addClass("error-alert")
        }else{
            $('#yearAlert').removeClass("error-alert")
            $('#uploadReslt').attr("success", true)
            $('#uploadReslt').submit()
        }
    })
})

//                                      show file name

fileName = function(){
    var n = document.getElementById('inputFile').files[0].name
    document.getElementById('viewFileName').innerHTML = n
}

//                                      .txt file upload

$(document).ready(function(){
    //                                      progressbar

    progressBar = function(){               //show
        $('#progressBar').removeClass('hidden-msg').addClass('show')
        $('#btnHelp').css({'display':'none'})
        $('#btn').addClass("disabled")
        $('#msg').removeClass('show')
}
    progressBar_hide = function(){          //hide
        $('#progressBar').removeClass('show').addClass('hidden-msg')
        $('#btn').removeClass("disabled")
    }

    $('#uploadReslt').submit(function(event){
        event.preventDefault()
        event.stopImmediatePropagation()
        progressBar()
        if($(this).attr('submitted')){
            $.ajax({
                url: '/admin/upload',
                type: 'POST',
                data: new FormData(this),
                contentType: false,
                cache: false,
                processData: false,
                success: function(msg){
                    if(msg.success){
                        $('#msg').html('File '+ document.getElementById('inputFile').files[0].name +' has been uploaded successfully!').addClass('show')
                        progressBar_hide()
                    }
                },
                complete: function(){
                    $('#uploadReslt').attr('submitted', false)
                }
            })
        }
        return false      
    })
})

//                              New admin

$(document).ready(()=>{
    var error = function(id){
        $(id).addClass('is-invalid')
        $(id).next().addClass('error-alert')
    }
    var success = function(id){
        $(id).removeClass('is-invalid')
        $(id).next().removeClass('error-alert')
        $(id).addClass('is-valid')
    }
    $('#newAdmin input').on('click', function(){
        $('#newAdmin small').addClass('hidden-msg').slideUp()
        $(this).next().removeClass('hidden-msg').slideDown()
    })
    $('#inputPassword1').keyup(function(){
        if($(this).val().length < 8){
            error($(this))
        } else {
            success($(this))
        }
    })
    $('#inputPassword2').keyup(function(){
        var pass1 = $('#inputPassword1').val()
        if($(this).val() === pass1){
            success($(this))
        }else{
            error($(this))
        }
    })
    $('#newAdmin').submit(function(event){
        event.preventDefault()
        if($('#inputPassword2').val()===$('#inputPassword1').val()){
            $('#inputPassword2').removeClass('is-valid')
            $('#createAdmin').addClass('disabled').html('<span id="creating"></span> Creating...')
            $('#creating').addClass('spinner-border spinner-border-sm')
            $.ajax({
                url: '/new-admin/',
                type: 'POST',
                data: {
                    'email': $('#inputEmail').val(),
                    'password': $('#inputPassword2').val()
                },
                success: function(data){
                    $('#createAdmin').removeClass('disabled').html('Create')
                    if(data.success){
                        $('#alert').html('Successfully created a new admin!').removeClass('alert-danger').addClass('alert-success').slideDown('slow')
                    } else {
                        $('#alert').html('Falied to create admin! Try again later.').removeClass('alert-success').addClass('alert-danger').slideDown('slow')
                    }
                }
            })
        }
    })
})