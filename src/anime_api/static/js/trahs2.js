

function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const secondsAgo = Math.floor((now - date) / 1000);

    const minutesAgo = Math.floor(secondsAgo / 60);
    const hoursAgo = Math.floor(minutesAgo / 60);
    const daysAgo = Math.floor(hoursAgo / 24);

    if (daysAgo > 0) {
        return daysAgo === 1 ? "1 day ago" : `${daysAgo} days ago`;
    } else if (hoursAgo > 0) {
        return hoursAgo === 1 ? "1 hour ago" : `${hoursAgo} hours ago`;
    } else if (minutesAgo > 0) {
        return minutesAgo === 1 ? "1 minute ago" : `${minutesAgo} minutes ago`;
    } else {
        return secondsAgo === 1 ? "1 second ago" : `${secondsAgo} seconds ago`;
    }
}


const baseDetailURL = "http://localhost:8000/content";
    /**
     * 
     * @param {String} baseURL base url to be used
     * @param {Number} id id of the selected post element 
     * @param {String} typoOfPost typeof of selected post
     *  
     */
    const getDetailedPost = async (baseUrl, id, typoOfPost) => {
        const url = `${baseUrl}/${typoOfPost}/${id}`;

        try {
            const response = await fetch(url);

            if (!response.ok){
                console.log(response.status, response.statusText);
                throw Error("Something happened")
            }

            const resJon = await response.json();
            return resJon;
            
        } catch (error) {
            console.log(error)
        }


    }


      /**
   * 
   * @param {Number} creator_id id of the creator to be followed
   * @pararm {String} action to be performed [POST, PUT]
   */
const followAndUnfollow = async function(creator_id, action="POST"){
  const url = `http://localhost:8000/actions/follow/${creator_id}/`;

  try {
      const response = await fetch(url, {
    headers: {
      "X-CSRFToken": csrf_token,
      "Content-Type": "application/json"
    },
    credentails: "same-origin",
    method: action
  })

  if (!response.ok) {
    throw new Error("Could post data to follow endpoint")
  }

  const resJon = await response.json();
  return resJon;
  
  } catch (error) {
    console.log(error);
  }

}


  /**
   * 
   * @param {Number} creator_id id of the creator to check status 
   */
const checkFollowStatus = async function(creator_id){
  const url = `http://localhost:8000/actions/check_follow_status/${creator_id}/`;

  try {
      const response = await fetch(url, {
    headers: {
      "X-CSRFToken": csrf_token,
      ContentType: "application/json",
      
    },
    credentials: "same-origin",
    method: "POST"
  })

  if (!response.ok) {
    console.log(response)
    console.log(response.status, response.statusText)
    throw new Error("Could post data to follow endpoint")
  }

  const resJon = await response.json();
  return resJon;

  } catch (error) {
    console.log(error);
  }


}



   /**
   * 
   * @param {String} content_type content_type of the post
   * @param {Number} content_id id of the post
   */
  const getLikeFavStatus = async (content_type, content_id) => {
    const url = `localhost:8000/content/action/like/${content_type}/${content_id}/`;

    try {
      
      const response = await fetch(url, {
        headers: {
          'X-CSRFToken': csrf_token,
        },
      })

      if (!response.ok) {
        console.log(response, response.status, response.statusText);
        throw new Error("Couldn't post data to the api")
      }

      const resJon = await response.json();
      console.log(resJon)
    } catch (error) {
      console.log(error)
    }

  }





/**
 * 
 * @param {String} content_type type of post object 
 * @param {Number} object_id id of post object
 */
const getComments = async (content_type, object_id) => {
  const url = `http://localhost:8000/comment/all/?content_type=${content_type}&object_id=${object_id}`;

  try {
    
    const response = await fetch(url, {
      header:{
        "X-CSRFToken": csrf_token,
      }
    },)

    if (!response.ok) {
      console.log(response.status, response.statusText, response)
      throw Error("An error occurred in comment async await")
    }

    const resJson = await response.json();
    
    // render comments
    renderComments(resJson);
    
    return resJson;

  } catch (error) {
    console.log(error)
  }
}

/**
 * 
 * @param {Array} data data to be rendered on the dom
 */
function renderComments(data){
  const renderedCommentsHTML = data.length === 0 ? "<h2>Be the first to comment</h2>" : data.map((el) => {

  return    `    <div class="image-text">
            <a href="profilepage.html">
              <img src="${el.owner.creator_logo}" alt="${el.owner.company_name || el.user}" />
            </a>

            <div class="name-time">
              <a href="profilepage.html">
                <h3>${el.owner.company_name || el.user}</h3>
              </a>
              <p>${el.text}</p>
            </div>
          </div>
    `
  }).join();

  commentContainerEl.innerHTML = "";
  commentContainerEl.insertAdjacentHTML("beforeend", renderedCommentsHTML);
}



/**
 * 
 * @param {Object} data data to be rendered on the dom
 */
function renderSingleComment(data){

const renderedCommentHtml =
    `    <div class="image-text">
            <a href="profilepage.html">
              <img src="${data.owner.creator_logo}" alt="${data.owner.company_name || data.user}" />
            </a>

            <div class="name-time">
              <a href="profilepage.html">
                <h3>${data.owner.company_name || data.user}</h3>
              </a>
              <p>${data.text}</p>
            </div>
          </div>
    `

  commentContainerEl.insertAdjacentHTML("beforeend",renderedCommentHtml);
  commentContainerEl.scrollHeight;

}


/**
 * 
 * @param {String} content_type type of post object 
 * @param {Number} object_id id of post object
 * @param {String} msg comment of user
*/
const postUserComment = async (content_type, object_id, msg) => {

  const url = `http://localhost:8000/comment/create/`;
  

  const filter_content =  {
    textcontent: "text",
    designconten: "design",
    videocontent: "video",
    anime: "anime",
    writtenstory: "writtenstory"
  }

  const userProf = "{{request.user.creator_profile.id}}"

//  {% comment %} const userComment =  {
//   "user": userProf,
//     "text": msg,
//     "parent": null,
//     "object_id": +object_id,
//     "content_type_str": filter_content[content_type]
// } {% endcomment %}

  let newCommentForm = new FormData();
  newCommentForm.append("text", msg);
  newCommentForm.append("object_id", object_id)
  newCommentForm.append("content_type_str", filter_content[content_type])
  newCommentForm.append("user", userProf)
  

  try {
    
    const response = await fetch(url,
    
      {
        headers: {
          "X-CSRFToken": csrf_token
        },
    method: "POST",
    body: newCommentForm
    },
  )

    if (!response.ok) {
      console.log(response.status, response.statusText, response)
      throw Error("An error occurred in comment async await")
    }

    const resJson = await response.json();
    console.log(resJson)

    // re-render comments
    renderSingleComment(resJson);
    
    // {% comment %} return resJson; {% endcomment %}
    

  } catch (error) {
    console.log(error)
  }
}
    
  //  <!-- Modal -->
      // MODAL VARIABLES
          const modal = document.querySelector(".modal");
          const overlay = document.querySelector(".overlay");
          const btnOpenModal = document.querySelectorAll(".show-modal");
          const modalImage = document.querySelector('.modal-image');
          const modalVideo = document.querySelector('.modal-video');

          // user's post details
          const profileLink = document.querySelector("#prof-lnk");  // update link to person profile and img
          const detailPostInfo = document.querySelector(".name-time");  // to update link to profile and name of post owner and date posted
          const followBtn = document.querySelector(".follow");
          const captionEl = document.querySelector(".caption")


          // <!-- NEW MODAL -->
      const profilePostContainerEl = document.querySelector("#post-container");

      profilePostContainerEl.addEventListener("click", async function (e){
      const selectedComponentEl = e.target.parentElement;

      const selectedPostId = e.target.parentElement.dataset.id;
      const selectedPostType = e.target.parentElement.dataset.posttype;

      

      if (selectedComponentEl.classList.contains("show-modal")){
        modal.classList.remove("hidden");
        overlay.classList.remove("hidden");

        const contentType = e.target.parentElement.dataset.posttype == "anime" || e.target.parentElement.dataset.posttype == "videocontent" ? "video" : "img";

        // <!-- get comments related to the post -->
      const relatedComments = await getComments(selectedPostType, selectedPostId);

    //   <!-- user add comment -->
        submitCommentBtn.addEventListener("click", async function(e){

          e.preventDefault();
            // get user input
            const comment = userComment.value;
            

            // validate data and send it to the backend
            if (comment) {
               const result = await postUserComment(selectedPostType, selectedPostId, comment);
               userComment.value = ""
            }
        })

      // <!-- keyboard binding-->
       submitCommentBtn.addEventListener("keypress", function(e){
        if (e.key == "Enter"){
          // cancel the default action if needed
          e.preventDefault();
          // trigger click event on button
          submitCommentBtn.click();
        }
       })

       userComment.focus();


        
        // <!-- Fill Modal with necessary data from the selected component -->
        if (contentType == "img"){
           const selectedSrc = selectedComponentEl.querySelector("img").getAttribute("src");

        // <!-- Call API to get detail information about selected element-->
        //  <!-- use the id and typeof dataset value to compose the url for the detail page-->
        //  <!-- make request to the url to get the data -->
          const detailData = await getDetailedPost(baseDetailURL, selectedPostId, selectedPostType);

          if (detailData) {

            const data = detailData;

            modal.querySelector(".post-view").querySelector("img").classList.remove("hidden")
            modal.querySelector(".post-view").querySelector("img").setAttribute("src", selectedSrc);

             profileLink.setAttribute("href", "/")

            // set profile image
            profileLink.querySelector("img").setAttribute("src", data.owner.creator_logo);

            // post detail
            // name of the post owner
            detailPostInfo.querySelector("h3").textContent =  data.owner.company_name;

            // set the date
            detailPostInfo.querySelector("p").textContent = timeAgo(data.release_date);

            // set the caption
            captionEl.textContent = data.description;

            // follow and unfollow
            // check the if authenticated user is following the creator and change the button text to show the status

            const followStatus = await checkFollowStatus(data.creator || data.owner.id );

            if (followStatus.message){
              followBtn.textContent = "Unfollow";
              followBtn.dataset.status = "unfollow";
            }else {
              followBtn.textContent = "Follow";
              followBtn.dataset.status = "follow"
            }

            // add eventlistener to the follow btn
            followBtn.addEventListener("click", async function(){

              const followStatus = followBtn.dataset.status == "follow" ? "POST" : "PUT";
              
              const result = await followAndUnfollow(data.creator || data.owner.id);

              if (result.message){
                followBtn.textContent = "Unfollow";
              }else if (!result.message){
                followBtn.textContent = "Follow";
              }
            })

          }


         } else if (contentType == "video" || contentType == "anime"){

          // <!-- Call API to get detail information about selected element-->
        //  <!-- use the id and typeof dataset value to compose the url for the detail page-->
        //  <!-- make request to the url to get the data -->
          const detailData = await getDetailedPost(baseDetailURL, selectedPostId, selectedPostType);

          if (detailData){

            const data = detailData;

          // const selectedSrc = selectedComponentEl // no src set on parentEl
            modal.querySelector('.post-view').querySelector('video').classList.remove('hidden')
            modal.querySelector('.post-view').querySelector('video').setAttribute("poster", data.thumbnail)
            modal.querySelector('.post-view').querySelector('video').setAttribute("src", data.video_file)

            // Update user information
            profileLink.setAttribute("href", "/")

            // set profile image
            profileLink.querySelector("img").setAttribute("src", data.owner.creator_logo);

            // post detail
            // name of the post owner
            detailPostInfo.querySelector("h3").textContent =  data.owner.company_name;

            // set the date
            detailPostInfo.querySelector("p").textContent = timeAgo(data.release_date);

            // set the caption
            captionEl.textContent = data.description;

            // follow and unfollow
            // check the if authenticated user is following the creator and change the button text to show the status

            const followStatus = await checkFollowStatus(data.creator || data.owner.id );

            if (followStatus.message){
              followBtn.textContent = "Unfollow";
              followBtn.dataset.status = "unfollow";
            }else {
              followBtn.textContent = "Follow";
              followBtn.dataset.status = "follow"
            }


            // <!-- add eventlistener to follow button -->
            followBtn.addEventListener("click", async function(){

              const followStatus = followBtn.dataset.status == "follow" ? "POST" : "PUT";
              
              const result = await followAndUnfollow(data.creator || data.owner.id);

              if (result.message){
                followBtn.textContent = "Unfollow";
              }else if (!result.message){
                followBtn.textContent = "Follow";
              } else {
                console.log(result)
                return ;
              }
            })
          }

         } else {
          // content type is not known
          console.log("none was selected")
          console.log(contentType,  "this is the content type");
         }


      } else {
        console.log("No")
        console.log(selectedComponentEl)
      }

      userComment.focus();

  })

/**
 * 
 * @param {String} url url of the resource
 * @returns 
 */
  const getRecentlyLikedUser = async (url) => {
    
    try {
      const response = await fetch(url,  {
        headers: {
          "X-CSRFToken": csrf_token
        },
        credentials: "same-origin"
      })

      if (!response.ok) {
        console.log(response);
        throw new Error("Couldn't get the name of the latest liked user")
      }

      const resJon = await response.json();
      const {owner} = resJon;

      return owner;
    } catch (error) {
      console.log(error)
    }
  }

const likeUpdate = async () => {
  //
}