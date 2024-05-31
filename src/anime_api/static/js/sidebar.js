// variables
const sideBar = document.querySelector("#side-bar");
const sideToggle = document.querySelector("#side-bar-toggle");
const mainPage = document.querySelector("#main-view");
const sideIcons = document.querySelectorAll(".s-ico");

const sideText = document.querySelectorAll(".s-text");

const toggleButton = document.querySelector("#side-toggle-img");
// console.log(src)

function slideSideBar() {
  mainPage.style.marginLeft = "170px";
  sideBar.style.width = "170px";
  // sideBar.style.paddingLeft = '10px'
  sideBar.style.alignItems = "start";
  toggleButton.src = "static/icons/backarrow 2icons.svg";

  for (let t = 0; t < sideText.length; t++) {
    sideText[t].classList.remove("hide");
    // console.log('removed')
  }

  for (let i = 0; i < sideIcons.length; i++) {
    sideIcons[i].classList.add("ico-expanded");
  }
}

function unSlideSideBar() {
  mainPage.style.marginLeft = "65px";
  sideBar.style.width = "65px";
  // sideBar.style.paddingLeft = '20px'
  sideBar.style.alignItems = "center";
  toggleButton.src = "static/icons/arrow 2icons.svg";

  for (let t = 0; t < sideText.length; t++) {
    sideText[t].classList.add("hide");
  }

  for (let i = 0; i < sideIcons.length; i++) {
    sideIcons[i].classList.remove("ico-expanded");
  }
}

let a = 1;
sideToggle.addEventListener("click", () => {
  if (a === 1) {
    slideSideBar();
    a = 0;
  } else {
    unSlideSideBar();
    a = 1;
  }
});
