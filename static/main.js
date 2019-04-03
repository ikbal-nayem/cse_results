fileName = function(){
    var n = document.getElementById('inputFile').files[0].name
    document.getElementById('viewFileName').innerHTML = n
}