
const progress = document.getElementById("progress");
const stepCircles = document.querySelectorAll(".circle");
const currentActive = document.getElementById('nodeActive').getAttribute('value');
console.log(currentActive);
update(currentActive);

function update(currentActive) {
  stepCircles.forEach((circle, i) => {
    if (i < currentActive) {
      circle.classList.add("active");
    } else {
      circle.classList.remove("active");
    }
  });

  const activeCircles = document.querySelectorAll(".active");
  progress.style.width =
    ((activeCircles.length - 1) / (stepCircles.length - 1)) * 100 + "%";

}

