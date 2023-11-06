const boxObj = document.getElementById('boxObject');
const imageObj = document.querySelectorAll('.image-objects');

const boxHeight = boxObj.clientHeight;
const boxWidth = boxObj.clientWidth;


function imageMove1() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)- mather[2]) / (imgCount* 10))*-1;
    let imageX =  ((mather[2] - boxWidth) + mather[0]);
    image.style.transform = `translate(${imageX}px, ${imageY}px)`; 
    imgCount++;
    console.log(imageY, imageX, rowCount)
    for (let i = 0; i < imageObj.length; i++) {
      imageObj[i].classList.remove("display-off");
    };
  }
}


function imageMove2() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  ((mather[1] * boxHeight)/mather[2]) * (30)-1;
    let imageX =  ((mather[2] - boxWidth) + mather[0]);
    image.style.transform = `translate(${imageX}px, ${imageY}px)`; 
    imgCount++;
    console.log(imageY, imageX, rowCount)
  }
}


function imageMove3() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  ((mather[1] * 2.5) + mather[0])-(rowCount* 120);
    let imageX =  (mather[2] * 1.2) - mather[0]-600;
    image.style.transform = `translate(${imageX}px, ${imageY}px)`; 
    imgCount++;
    console.log(imageY, imageX, rowCount)
  }
}

async function executeImageMoves() {
  const imageObj = document.getElementsByClassName('your-image-class'); // Replace with your actual image elements
  const imageMoves = [imageMove1, imageMove2, imageMove3]; // Array of your imageMove functions

  for (let i = 0; i < imageMoves.length; i++) {
    const imageMoveFunction = imageMoves[i];

    await new Promise((resolve) => {
      setTimeout(() => {
        imageMoveFunction(imageObj);
        resolve();
      }, i * 800); // Adjust the delay (1000ms = 1 second) to control the timing between function executions
    });
  }
}

// Call the executeImageMoves function when the page is loaded
window.addEventListener('load', () => {
  executeImageMoves();
});

function numbStuff(imgCount, rowCount) {
	let rowN = rowCount * 300;
  let y1 = (imgCount*boxHeight)/10;
  let x1 = (imgCount*boxWidth)/12;
  return [x1, y1, rowN]; 
}