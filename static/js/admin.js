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