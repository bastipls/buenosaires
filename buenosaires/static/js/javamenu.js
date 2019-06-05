var btnmenu = document.getElementById("btn-menu");
var navega = document.getElementById("navegador");

btnmenu.addEventListener('click', function(){
    navega.classList.toggle('move');
})