  const profilePostContainerEl = document.querySelector("#post-container");

  profilePostContainerEl.addEventListener("click", function(e){
    console.log(e.target.parentElement)
  })
    // <!-- Modal -->
      // MODAL VARIABLES
          const modal = document.querySelector(".modal");
          const overlay = document.querySelector(".overlay");
          const btnOpenModal = document.querySelectorAll(".show-modal");
          const modalImage = document.querySelector('.modal-image');
          const modalVideo = document.querySelector('.modal-video');

          // MODAL FUNCTIONS
          // ///////////////
          const openModal = function (i) {
            return function() {

              modal.classList.remove("hidden");
              overlay.classList.remove("hidden");

              const objectPath = btnOpenModal[i].children[0];
              const src = objectPath.getAttribute("src");

              if (objectPath.tagName === "IMG") {
                // Handle image
                modalImage.classList.remove("hidden");
                modalVideo.classList.add("hidden");
                modalImage.setAttribute("src", src);
              } else if (objectPath.tagName === "VIDEO") {
                // Handle video
                modalImage.classList.add("hidden");
                modalVideo.classList.remove("hidden");
                modalVideo.setAttribute("src", src);
                modalVideo.load(); // Ensure the video loads with the new source
              }
            }
          };

          const closeModal = function () {
            modal.classList.add("hidden");
            overlay.classList.add("hidden");

            // Reset the modal content
            modalImage.classList.add("hidden");
            modalVideo.classList.add("hidden");
            modalVideo.setAttribute("src", ""); // Clear the video src
          };

          // Adding event listeners to each button
          btnOpenModal.forEach((button, i) => button.addEventListener("click", openModal(i)));

          overlay.addEventListener("click", closeModal);

          document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && !modal.classList.contains("hidden")) {
              closeModal();
            }
          });


    // <!-- Modal buttons(like, save icons) -->
      // interaction buttons
      const likeButton = document.querySelector(".like");
      const saveButton = document.querySelector(".save");
      const faveButton = document.querySelector(".fave");

      likeButton.addEventListener("click", () => {
        let src =
          likeButton.getAttribute("src") === "/Icons/likeicon1.svg"
            ? "/Icons/likeicon2.svg"
            : "/Icons/likeicon1.svg";
        likeButton.setAttribute("src", src);
      });

      // DO NOT DELETE!!!!!!!
      // saveButton.addEventListener("click", () => {
      //   let src =
      //     saveButton.getAttribute("src") === "/Icons/saveicon1.svg"
      //       ? "/Icons/saveicon2.svg"
      //       : "/Icons/saveicon1.svg";
      //   saveButton.setAttribute("src", src);
      // });

      faveButton.addEventListener("click", () => {
        let src =
          faveButton.getAttribute("src") === "/Icons/saveicon1.svg"
            ? "/Icons/saveicon2.svg"
            : "/Icons/saveicon1.svg";
        faveButton.setAttribute("src", src);
      });


    ```

         <div class="page-content-card show-modal">
                <img src="/Portfolio/jennifer_s works/aresst.jpg" alt="" />
                <p>Arrest your cravings</p>
              </div>




            <div class="page-content-card show-modal" data-id="2" >
                <img src="/Portfolio/jennifer_s works/hungry.jpg" alt="" />
                <p>Hungry</p>
              </div>




    <div class="pop-modal modal hidden">
      <div class="post-view">
        <img class="modal-image hidden" src="" alt="Modal Image">
        <video class="modal-video hidden" controls autoplay
        muted
        loop
        controls
        poster="">
      </div>

      <div class="right-side">
        <!-- creator info -->
        <div class="top-section">
          <div class="image-text">
            <a href="profilepage.html">
              <img src="/Images/ (1).jpg" alt="" />
            </a>

            <div class="name-time">
              <a href="profilepage.html">
                <h3>Alan Dalani</h3>
              </a>
              <p>12 days ago</p>
            </div>
          </div>
          <button class="follow">Follow</button>
        </div>

        <p class="caption">
          Art is where it all starts. The goal is simple, be the best to do it.
        </p>

        <hr />
        <!-- comments -->
        <div class="comments">
          <div class="image-text">
            <a href="profilepage.html">
              <img src="/Images/ (2).jpg" alt="" />
            </a>

            <div class="name-time">
              <a href="profilepage.html">
                <h3>Jenni Addo</h3>
              </a>
              <p>Im enthralled😍</p>
            </div>
          </div>

          <div class="image-text">
            <a href="profilepage.html">
              <img src="/Images/ (5).jpg" alt="" />
            </a>
            <div class="name-time">
              <a href="profilepage.html">
                <h3>Ronald the Conqueror</h3>
              </a>
              <p>Interesting, how much to conquer?</p>
            </div>
          </div>

          <div class="image-text">
            <a href="profilepage.html">
              <img src="/Portfolio/jennifer_s works/" alt="" />
            </a>
            <div class="name-time">
              <a href="profilepage.html">
                <h3>Brago</h3>
              </a>

              <p>An amazing piece</p>
            </div>
          </div>
        </div>

        <hr />

        <div class="actions">
          <div class="interactions">
            <img src="/Icons/likeicon1.svg" class="like" alt="" />
            <!-- <img src="/Icons/saveicon1.svg" class="save" alt="" /> -->
            <img src="/Icons/saveicon1.svg" class="fave" alt="" />
          </div>

          <p>Liked by <span>Jess Asante</span> and <span>23</span> others</p>
        </div>

        <hr />

        <div class="add-comment">
          <input type="text" placeholder="Add comment.." />
          <button type="submit">Post</button>
        </div>
      </div>

      <hr />
    </div>


    ```

    /**
     * 
     * @param {String} baseURL base url to be used
     * @param {Number} id id of the selected post element 
     * @param {String} typoOfPost typeof of selected post
     *  
     */
    const getDetailedPost = async (baseUrl, id, typoOfPost) => {
        const url = `${baseUrl}/${typoOfPost}/${id}`;
        console.log(url)

        try {
            
            const response = await fetch(url);

            if (!response.ok){
                console.log(response.status, response.statusText);
                throw Error("Something happened")
            }

            const resJon = await response.json();
            console.log(resJon);
            return resJon;

        } catch (error) {
            console.log(error)
        }


    }


  /**
   * 
   * @param {Number} creator_id id of the creator to be followed 
   */
const followAndUnfollow = async function(creator_id){
  const url = `http://localhost:8000/actions/follow/${creator_id}/`;

  try {
      const response = await fetch(url, {
    headers: {
      ContentType: "application/json",
    },
    credentials: "include",
    method: "POST"
  })

  if (!response.ok) {
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
   * @param {Number} creator_id id of the creator to check status 
   */
const checkFollowStatus = async function(creator_id){
  const url = `http://localhost:8000/actions/check_follow_status/${creator_id}/`;

  try {
      const response = await fetch(url, {
    headers: {
      ContentType: "application/json",
    },
    credentials: "include",
    method: "POST"
  })

  if (!response.ok) {
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
 * @param {String} content_type type of post object 
 * @param {Number} object_id id of post object
 */
const getComments = async (content_type, object_id) => {
  const url = `http://localhost:8000/comment/all/?content_type=${content_type}&object_id=${object_id}`

  try {
    
    const response = await fetch(url, {
      "X-CSRFToken": csrf_token,
    },)

    if (!response.ok) {
      console.log(response.status, response.statusText, response)
      throw Error("An error occurred in comment async await")
    }

    const resJson = await response.json();
    console.log(resJson)

    return resJson;

  } catch (error) {
    console.log(error)
  }
}


const commentContainerEl = document.querySelector("#comment-container")
/**
 * 
 * @param {Array} data data to be rendered on the dom
 */
function renderComments(data){
  const renderedCommentsHTML = data.length === 0 ? "" : data.map((el) => {

    `    <div class="image-text">
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

}






/**
 * 
 * @param {String} content_type type of post object 
 * @param {Number} object_id id of post object
 * @param {String} msg comment of user
*/
const postUserComment = async (content_type, object_id, msg) => {
  // const url = `http://localhost:8000/comment/all/?content_type=${content_type}&object_id=${object_id}`

  const url = `http://localhost:8000/comment/create/`;
  
  const message = {
    target_obj: object_id,
    content_type: content_type,
    text: msg
  }

  try {
    
    const response = await fetch(url,
    
      {
        headers: {
          "X-CSRFToken": csrf_token,
          "Content-Type": "application/json",
        },

      method: "POST",
      credentials: "same-origin",
      body: JSON.stringify(message)
    },
  )

    if (!response.ok) {
      console.log(response.status, response.statusText, response)
      throw Error("An error occurred in comment async await")
    }

    const resJson = await response.json();
    console.log(resJson)

    return resJson;

  } catch (error) {
    console.log(error)
  }
}





