
function dueBal() {
    var elem = document.getElementById("due");
    
    var ratio = parseInt(elem.getAttribute("value"));
    
    var width = ratio;
	console.log(width)
    elem.style.width = width + "%";
}

window.onload = dueBal;