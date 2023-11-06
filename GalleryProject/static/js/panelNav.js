var buttons = document.getElementsByClassName('addLoader');

const mainWindow = document.getElementById('main');
const loaderWindow = document.getElementById('windowLoader');

for (var i = 0; i < buttons.length; i++) {
  buttons[i].onclick = clickedHide;
}

function clickedHide() {
  loaderWindow.style.display = 'block';
  mainWindow.style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function(event) {
  const toggleIcons = document.querySelectorAll('.header_toggle');
  const nav = document.getElementById('nav-bar');
  const bodypd = document.getElementById('body-pd');
  const headerpd = document.getElementById('header');

  toggleIcons[0].addEventListener('click', () => {
      nav.classList.toggle('show');
      bodypd.classList.toggle('body-pd');
      headerpd.classList.toggle('body-pd');
  });

  const linkColor = document.querySelectorAll('.nav_link');

  function colorLink() {
      linkColor.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
  }

  linkColor.forEach(l => l.addEventListener('click', colorLink));
});