const scrollHit1 = document.getElementById('scrollHit1');
//const scrollHit2 = document.getElementById('scrollHit2');
document.addEventListener("scroll", function () {
	if (window.scrollY > scrollHit1.getBoundingClientRect().top) {
	  document.body.classList.add("scroll-up1");
	} else {
	  document.body.classList.remove("scroll-up1");
	}
});

//document.addEventListener("scroll", function () {
//	if (window.scrollY > scrollHit2.getBoundingClientRect().bottom) {
//	  document.body.classList.add("scroll-up2");
//	} else {
//	  document.body.classList.remove("scroll-up2");
//	}
//});