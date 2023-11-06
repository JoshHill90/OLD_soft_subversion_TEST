document.addEventListener("scroll", function () {
	if (window.scrollY > 0) {
	  document.body.classList.add("scroll-up");
	} else {
	  document.body.classList.remove("scroll-up");
	}
  });