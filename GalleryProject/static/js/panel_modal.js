

function handleModal(modalSet, buttonSet, numberClose){
  // Get the modal
  var detailsWindow = document.getElementById(modalSet);

  // Get the button that opens the modal
  var detailsBtn = document.getElementById(buttonSet);

  // Get the <span> element that closes the modal
  var span = document.getElementById(numberClose);

  // When the user clicks the button, open the modal 
  detailsBtn.onclick = function() {
    detailsWindow.style.display = "block";
    window.scrollTo(10, 10);
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    detailsWindow.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == detailsWindow) {
      detailsWindow.style.display = "none";
    }
  }
}

