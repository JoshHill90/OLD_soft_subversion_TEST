const faders = document.querySelectorAll('.fade-in');
const loaderBlocks = document.querySelectorAll('.windowLoader');
const floaters = document.querySelectorAll('.float-in');
const floaters2 = document.querySelectorAll('.float-in-sec');

const sliders = document.querySelectorAll('#slide-in');

document.addEventListener("mousemove", parallax);
document.addEventListener("scroll", parallax);



const appearOptions = {
  threshold: 0,
  rootMargin: "-100px 0px 0px 0px"

};

const appearOnScroll = new IntersectionObserver(
  function (entries, appearOnScroll) {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) {
        entry.target.classList.remove("appear");
      } else {
        entry.target.classList.add("appear");
        appearOnScroll.unobserve(entry.target);
      }
    });
    
    // Add 'scrolling' class to body while the animations are in progress
    document.body.classList.add("scrolling");
    setTimeout(function () {
      // Remove 'scrolling' class after a short delay (adjust the delay as needed)
      document.body.classList.remove("scrolling");

    }, 1500); // Adjust the delay (in milliseconds) as needed
  },
  appearOptions
);

floaters.forEach(floater => {
  appearOnScroll.observe(floater);
});

floaters2.forEach(floater2 => {
appearOnScroll.observe(floater2);
});


sliders.forEach(slider => {
  appearOnScroll.observe(slider);
});

faders.forEach(fader => {
  appearOnScroll.observe(fader);
});

loaderBlocks.forEach(loaderBlock => {
appearOnScroll.observe(loaderBlock);
});

function parallax(e){

  var fadersN = document.querySelectorAll('.fade-in');
  var loaderBlocksN = document.querySelectorAll('.windowLoader');
  var floatersN = document.querySelectorAll('.float-in');
  var floaters2N = document.querySelectorAll('.float-in-sec');
  var slidersN = document.querySelectorAll('#slide-in');


  floatersN.forEach(floater => {
      appearOnScroll.observe(floater);
  });

  floaters2N.forEach(floater2 => {
    appearOnScroll.observe(floater2);
  });


  slidersN.forEach(slider => {
      appearOnScroll.observe(slider);

      if (slider.classList == 'slide-left'){
        console.log('slider here')
      }
  });

  fadersN.forEach(fader => {
      appearOnScroll.observe(fader);
  });

  loaderBlocksN.forEach(loaderBlock => {
    appearOnScroll.observe(loaderBlock);
  });

    if (!document.body.classList.contains("scrolling"))
    {document.querySelectorAll(".object").forEach(function(move){
            var moving_value = move.getAttribute("data-value");
            var x = (e.clientX * moving_value) /250;
            var y = (e.clientY * moving_value) / 250;
            move.style.transform = "translateX(" + x +"px) translateY(" + y +"px)";
            move.style.transition = "transform 50ms ease-in";
        });
    }

};
