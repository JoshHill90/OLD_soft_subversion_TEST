const boxObj = document.getElementById('boxObject');
const imageObj = document.querySelectorAll('.image-objects');
let onSwitch = 'off'
const boxHeight = boxObj.clientHeight;
const boxWidth = boxObj.clientWidth;
const imageArrayX = new Array ;
const imageArrayY = new Array ;
const w = window.innerWidth;
const pastScreenX = imageObj.length / 2;


function imageMove1() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)- mather[2]) / (imgCount* 15))*-1;
    let imageX =  ((mather[2] - boxWidth) + mather[0]);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(65deg) skew(20deg, 10deg)`; 
    imgCount++;
    
    for (let i = 0; i < imageObj.length; i++) {
      imageObj[i].classList.remove("display-off");
    };
  }
  return;
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
    let imageY =  (((mather[1] * boxHeight)/mather[2]) * (30)-1) * 2;
    let imageX =  ((mather[2] + boxWidth) + mather[0] * 4);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(45deg) scale(122%) skew(4deg, 32deg)`; 
    imgCount++;
    
  }
  return;
};

function imageMove3_1() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)- mather[2]) / (imgCount* 15))*-1;
    let imageX =  ((mather[2] - boxWidth) * (mather[0])/40);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(32deg) scale(130%) skew(6deg, 36deg)`; 
    imgCount++;
    
  }
  return;
};

function imageMove3_2() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
      imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)/mather[2]) * (30)-1) * 2;
    let imageX =  ((mather[2] + boxWidth) + mather[0] * -4);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(38deg) scale(135%) skew(10deg, 40deg)`;  
    imgCount++;
    
  }
  return;
};

function imageMove3_3() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)- mather[2]) / (imgCount* 10))*-1;
    let imageX =  ((mather[2] - boxWidth) * (mather[0])/40);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(-26deg) scale(-45%) skew(-4deg, -32deg)`; 
    imgCount++;
    
  }
  return;
}

function imageMove4() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  (((mather[1] * boxHeight)/mather[2]) * (30)-1);
    let imageX =  ((mather[2] - boxWidth) + (mather[0]) + 300);
    image.style.transition = 'transform 2s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(23deg) scale(120%) skew(4deg, 32deg)`; 
    imgCount++;
    
  }
  return;
}


function imageMove5() {
  let imgCount = 1;
  let rowCount = 1;
  for (let image of imageObj) { 
    if (imgCount == 5) {
			imgCount = 1;
      rowCount++;
    };
    let mather = numbStuff(imgCount, rowCount);
    let imageY =  ((mather[1] * 2.5) + mather[0])-(rowCount* 120);
    let imageX =  ((mather[2] * 1.2) - mather[0]-600) + w;
    image.style.transition = 'transform 1.5s';
    image.style.transform = `translate(${imageX}px, ${imageY}px) rotate(-4deg) scale(90%) skew(0deg, 0deg)`; 
    imgCount++;
   
  }
  return;
}

function lastMoveFunc() {
  let imageCounter0 = 0;
  for (let image of imageObj) {
    const initialImagePosistionX = image.getBoundingClientRect().left;
    const initialImagePosistionY = image.getBoundingClientRect().top;
    imageArrayX.push(initialImagePosistionX);
    imageArrayY.push(initialImagePosistionY);
    console.log(initialImagePosistionX)
    console.log('step 0')
    image.style.transition = 'transform 190s';
    image.style.transform = `translate(${imageArrayX[imageCounter0] - (w * pastScreenX)}px, ${imageArrayY[imageCounter0] + 200}px) rotate(-14deg)`;

    imageCounter0 +=1;
  }

 

  window.setInterval(() => {
    imageMove4();
    console.log(
      imageObj[imageObj.length - 1].getBoundingClientRect().left,
      imageArrayX[imageObj.length - 1] + ((w * .8 ) - 200) 
    )
  },1000);

  function imageMove4() {
    let imageCounter = 0;

    for (let image of imageObj) {
      let currentImagePositionX = image.getBoundingClientRect().left;
      const newPosistionX = imageArrayX[imageCounter] - (w * pastScreenX) ;
      const newPosistionY = imageArrayY[imageCounter] + 2500;

      
      if (currentImagePositionX > -300) {
        
        if (image.style.transform != `translate(${newPosistionX}px, ${newPosistionY}px) rotate(-14deg)` &&
        (imageObj[imageObj.length - 1].getBoundingClientRect().left) < -(w / 2) || (imageObj[imageObj.length - 1].getBoundingClientRect().left) > (imageArrayX[imageObj.length - 1] + ((w * .8 ) - 200)) ) {
          console.log(imageCounter, 'step 1')
          image.style.transition = 'transform 190s';
          image.style.transform = `translate(${newPosistionX}px, ${newPosistionY}px) rotate(-14deg)`;
        } else {
          //console.log(imageCounter, 'in action')
          //pass
        }
        
      } else {
        console.log(imageCounter, 'step 2')
        imageRotater(image, imageArrayX[imageCounter], imageArrayY[imageCounter])
      }
      imageCounter += 1;
    };
  };
  return;
};


async function executeImageMoves() {
  const imageMoves = [imageMove4, imageMove5, lastMoveFunc];
  imageMove1();
  for (let i = 0; i < imageMoves.length; i++) {
    const imageMoveFunction = imageMoves[i];
    console.log(imageMoveFunction)
    
    await new Promise((resolve) => {
      setTimeout(() => {
        imageMoveFunction();
        resolve();
      }, 1800); 
    });

  }
  return;
}


window.addEventListener('load', () => {
  executeImageMoves();
});

function numbStuff(imgCount, rowCount) {
	let rowN = rowCount * 300;
  let y1 = (imgCount*boxHeight)/10;
  let x1 = (imgCount*boxWidth)/12;
  return [x1, y1, rowN]; 
}

function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

function rotate1(image, imageX, imageY) {
  image.style.transition = 'transform .2s';
  image.style.transform = `translate(${imageX - (w * pastScreenX)}px, ${imageY -2000}px) rotate(-14deg)`;
  return;
}

function rotate2(image, imageX, imageY) {
  image.style.transition = 'transform .2s';
  image.style.transform = `translate(${imageX + w * 4 }px, ${imageY -2000}px) scale(1%) rotate(-14deg)`;
  return;
}

function rotate3(image, imageX, imageY) {
  image.style.transition = 'transform .2s';
  
  image.style.transform = `translate(${imageX + (w * .8 ) }px, ${imageY + 250}px) rotate(-14deg)`;
  return;
}


async function imageRotater(image, imageX, imageY) {
  const rotateSets = [ rotate1, rotate2, rotate3];
  for (let i = 0; i < rotateSets.length; i++) {
    const rotateFunction = rotateSets[i];

    
    await new Promise((resolve) => {
      setTimeout(() => {
        rotateFunction(image, imageX, imageY);
        resolve();
      }, 200); 
    });

  }
  return;
}