// fileName = function(){
//     var n = document.getElementById('inputFile').files[0].name
//     document.getElementById('viewFileName').innerHTML = n
// }
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