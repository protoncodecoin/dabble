//main page content tabs
// main page content tabs
const videoTab = document.querySelector(".videos-tab");
const storyTab = document.querySelector(".stories-tab");
const postTab = document.querySelector(".post-tab");
const seriesTab = document.querySelector(".series-tab");

const videoSection = document.querySelector(".videos-section");
const storySection = document.querySelector(".stories-section");
const postSection = document.querySelector(".post-section");
const seriesSection = document.querySelector(".series-section");

function selectPageTab(tab, tabContent) {
  tab.addEventListener("click", () => {
    videoTab.classList.remove("current");
    videoSection.classList.add("hidden");
    storyTab.classList.remove("current");
    storySection.classList.add("hidden");
    postTab.classList.remove("current");
    postSection.classList.add("hidden");
    seriesTab.classList.remove("current");
    seriesSection.classList.add("hidden");
    tab.classList.add("current");
    tabContent.classList.remove("hidden");
  });
}

selectPageTab(videoTab, videoSection);
selectPageTab(storyTab, storySection);
selectPageTab(postTab, postSection);
selectPageTab(seriesTab, seriesSection);

// Modal

// MODAL VARIABLES
// ///////////////
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");
const btnCloseModal = document.querySelector(".close-modal");
const btnOpenModal = document.querySelector(".show-modal");

// MODAL FUNCTIONS
// ///////////////
const openModal = function () {
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const closeModal = function () {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
};

btnOpenModal.addEventListener("click", openModal);

btnCloseModal.addEventListener("click", closeModal);

overlay.addEventListener("click", closeModal);

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// <!-- Modal tabs -->
// Variables
const createTab = document.getElementById("create-tab");
const uploadTab = document.getElementById("upload-tab");

function selectTab(tab) {
  tab.addEventListener("click", () => {
    createTab.classList.remove("selected");
    uploadTab.classList.remove("selected");
    tab.classList.add("selected");
  });
}

selectTab(createTab);
selectTab(uploadTab);

// Form Tabs Variables
const postVideoTab = document.querySelector(".post-nav-video");
const postStoryTab = document.querySelector(".post-nav-story");
const postImageTab = document.querySelector(".post-nav-image");

function selectNavTab(tab) {
  tab.addEventListener("click", () => {
    postVideoTab.classList.remove("current");
    postStoryTab.classList.remove("current");
    postImageTab.classList.remove("current");
    tab.classList.add("current");
  });
}

selectNavTab(postVideoTab);
selectNavTab(postStoryTab);
selectNavTab(postImageTab);

// Form Content Variables
const createVideo = document.querySelector(".create-video");
const createStory = document.querySelector(".create-story");
const createImage = document.querySelector(".create-image");

const uploadVideo = document.querySelector(".upload-video");
const uploadStory = document.querySelector(".upload-story");

// ////////////////////////////////////////////
// const displayContent = (mainTab, postTab, formContent) => {

//   const arr = document.querySelectorAll('.create');
//   const arr2 = document.querySelectorAll('.upload');

//   mainTab.addEventListener('click', () => {})
//   if (mainTab.classList.contains('selected')) {
//     postTab.addEventListener('click', () => {

//       for (let i = 0; i < arr.length; i++) {
//         arr[i].classList.add('hidden')
//       }

//       for (let i = 0; i < arr2.length; i++) {
//         arr2[i].classList.add('hidden')
//       }

//       formContent.classList.remove('hidden')
//     })
//   }
// }

const displayContent = (mainTab, postTab, formContent) => {
  const arr = document.querySelectorAll(".create");
  const arr2 = document.querySelectorAll(".upload");

  mainTab.addEventListener("click", () => {
    if (mainTab.classList.contains("selected")) {
      postTab.addEventListener("click", () => {
        for (let i = 0; i < arr.length; i++) {
          arr[i].classList.add("hidden");
        }

        for (let i = 0; i < arr2.length; i++) {
          arr2[i].classList.add("hidden");
        }

        formContent.classList.remove("hidden");
      });
    }
  });
};

displayContent(createTab, postVideoTab, createVideo);
displayContent(createTab, postStoryTab, createStory);
displayContent(createTab, postImageTab, createImage);
displayContent(uploadTab, postVideoTab, uploadVideo);
displayContent(uploadTab, postStoryTab, uploadStory);
