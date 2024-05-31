// // MODAL VARIABLES
//     // ///////////////
//     const modal = document.querySelector(".modal");
//     const overlay = document.querySelector(".overlay");
//     const btnCloseModal = document.querySelector(".close-modal");
//     const btnsOpenModal = document.querySelector(".show-modal");
    
//     const openModal = function () {
//           modal.classList.remove("hidden");
//           overlay.classList.remove("hidden");
//         };
    
    
//     // VALIDATION VARIABLES
//     // ////////////////////
//     const submitButton = document.querySelector(".submit");
//     const info = document.querySelectorAll(".info");
    
//     // VALIDATION FUNCTIONS
//     // ///////////////////////////////////////
//     const revertColors = (input) => {
//       input.classList.remove("placeholder-color-red");
//     };
    
//     submitButton.onclick = function () {
//       let allValid = true
    
//       info.forEach((m) => {
//         if (m.value.trim() === "") {
//           m.classList.add("placeholder-color-red");
//           allValid = false;
//         }
        
//         m.onkeydown = () => revertColors(m);
//       });
      
//       if (allValid) {
//         openModal()
//       }
//     };
    
//     // MODAL FUNCTIONS
//     // ///////////////
//     const closeModal = function () {
//       modal.classList.add("hidden");
//       overlay.classList.add("hidden");
//     };
    
//     btnCloseModal.addEventListener("click", closeModal);
//     overlay.addEventListener("click", closeModal);
    
//     document.addEventListener("keydown", function (e) {
//       // console.log(e.key);
    
//       if (e.key === "Escape" && !modal.classList.contains("hidden")) {
//         closeModal();
//       }
//     });