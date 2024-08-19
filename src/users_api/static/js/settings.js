// get the current user
const currentUser = authUser;

const topProfileSettings = document.querySelector("#top-profile");
const bio = document.querySelector("#bio-info")
const emailEl = document.querySelector("#email")
const quoteEl = document.querySelector("#quote")
const bgImgEl = document.querySelector("#bg-img")
const interestEl = document.querySelector("#interests")


let creatorURL;

/**
 * @param {Number} id if of the user
 * @returns Profile data of the authenticated user
 */
const getProfileInfo = async (id) => {
    const profileUrl = `http://localhost:8000/userprofiles/${id}/`;

try {
      const response = await fetch(profileUrl, {
    headers: {
      "X-CSRFToken": csrf_token,
      "Content-Type": "application/json"
    },
    credentails: "same-origin",
  })

  if (!response.ok) {
    throw new Error("Could post data to profile endpoint")
  }

  const resJon = await response.json();
  renderProfileInfo(resJon);

  return resJon;
  
  } catch (error) {
    console.log(error);
  }
}


const renderProfileInfo = (data) => {

    
    if (Object.keys(data).length > 0){
        
        const {id, url, creator, company_name, programme, biography,  background_image, creator_logo, owner, company_website, email, favorite_quote, interests} = data;

        creatorURL = creator;

        // username
        topProfileSettings.querySelector(".profile-info").querySelector(".text").querySelector("h4").textContent = owner;
        
        // programme
        topProfileSettings.querySelector(".profile-info").querySelector(".text").querySelector("p").textContent = programme;
        
        // bio information
        bio.value = biography    
        
        // email
        emailEl.value = email;
        emailEl.disabled = true;

        // favorite quote
        quoteEl.value = favorite_quote;

        // profile image
        topProfileSettings.querySelector("img").setAttribute("src", creator_logo);

        // background image
        bgImgEl.querySelector("img").setAttribute("src", background_image)

        // studio name
        document.querySelector("#studio-name").value = company_name

        // website name
        document.querySelector("#website").value = company_website

        // interests
        interestEl.querySelectorAll(".interest-item").forEach((el) => {
            let interestDataset = el.dataset.interest;

            if (interests.includes(interestDataset)){
                // set element value to active
                el.querySelector("input").checked = true;
            }else {
                // console.log(interestDataset, interests)
            }
        })
    
    } else {
        console.log("length is zero")
    }
}

getProfileInfo(authUser);


/**
 * @param {String} url Url to the endpoint
 * @returns Profile data of the authenticated user
 */
const getUserInfo = async (url) => {


try {
      const response = await fetch(url, {
    headers: {
      "X-CSRFToken": csrf_token,
      "Content-Type": "application/json"
    },
    credentails: "same-origin",
  })

  if (!response.ok) {
    throw new Error("Could post data to getuserInfo endpoint")
  }

  const resJon = await response.json();

  const {email} = resJon;
  
  return email;
  
  } catch (error) {
    console.log(error);
  }
}


document.querySelector(".update").addEventListener("click", async function (e){
    // get field values
    // get profile image
   const profileImg =  document.querySelector("#imageInput").value;
   const bgImg = document.querySelector("#imageInput2").value;

    // bio
    const bioInput = document.querySelector("#bio-info").value;

    // quote field
    const quoteInput = document.querySelector("#quote").value;

    // programme
    const programmeInput = document.querySelector("#programme").value;

    // website
    const websiteInput = document.querySelector("#website").value;

    // studio-name
    const studioInput = document.querySelector("#studio-name").value;

    // interest fields
    const allInterest = interestEl.querySelectorAll(".interest-item")
    const userSelectedInputs = []

    for (let interest of allInterest){
        if (interest.querySelector("input").checked){
            userSelectedInputs.push(interest.dataset.interest)
        }
    }

    // new a form and append elements
    const updateForm = new FormData();

    // append the authenticated user to the form
    updateForm.append("creator", `http://localhost:8000/users/${defaultUser}/`);


    if (profileImg !== ""){
        updateForm.append("creator_logo", profileImg);
    }
    if (bgImg !== ""){
        updateForm.append("background", bgImg)
    }if (bioInput !== ""){
        updateForm.append("bio", bioInput)
    }if (quoteInput !== ""){
        updateForm.append("favorite_quote", quoteInput)
    if (programmeInput !== ""){
        updateForm.append("programme", programmeInput);
    }if (websiteInput !== ""){
        updateForm.append("company_website", websiteInput)
    }if (studioInput !== ""){
        updateForm.append("company_name", studioInput);
    }
    }if (userSelectedInputs.length !== 0){
        userSelectedInputs.map((el) => updateForm.append("interests", el));
    }
    
    // send data to api
    const apiURL = `http://localhost:8000/userprofiles/${currentUser}/`;
    try {

        const response = await fetch(apiURL, {
            method: "PATCH",
            headers: {
                "X-CSRFToken": csrf_token,
            },
            credentials: "same-origin",
            body: updateForm
        });

        if (!response.ok) {
            console.log(response, response.status, response.statusText)
            throw new Error("Failed to post data from settings.py", response)
        }

        // success
        const resData = await response.json()

        // display an alert showing the success message

    } catch (error) {
        console.log(error)
    }
})
