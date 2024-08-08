const loadTrigger = document.getElementById("load-trigger");
const imageClass = "page-content-card";
const skeletonImageClass = "skeleton-image";
const postAnimationContainerEl = document.querySelector("#gallery_stories");
const throttleTime = 1000;
let throttleTimer = false;
let offset = 0;
let limit = 10;
let blockAnimationRequest = false;
let emptyAnimationPage = false;
let totalPosts;

/**
 *
 * @param {Function} callback function to call after throttling
 * @param {Number} time seconds to wait before performing next action
 */
function throttle(callback, time) {
  // Prevent additional calls until timeout elapses
  if (throttleTimer) {
    console.log("throttling");
    return;
  }
  throttleTimer = true;

  setTimeout(() => {
    callback();

    // Allow additional requests to be made
    throttleTimer = false;
  }, time);
}

const observer = detectScroll();

function detectScroll() {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        throttle(() => {
          loadMorePosts();
        }, throttleTime);
      }
    },
    { rootMargin: "-30px" }
  );

  // start watching load-trigger div
  observer.observe(loadTrigger);

  return observer;
}

async function loadMorePosts() {
  // const newPostsElements = [];
  // for (let i = 0; i < limit; i++) {
  //   const postCard = document.createElement("div");

  //   // Indicate image load
  //   postCard.classList.add(imageClass, skeletonImageClass);

  //   // include postcard in container
  //   postAnimationContainerEl.appendChild(postCard);

  //   // store in temp array to update with actual pst when loaded
  //   newPostsElements.push(postCard);
  // }

  // load more post from the server
  // getPosts(0, 1);-
  if (!emptyAnimationPage && !blockAnimationRequest) {
    blockAnimationRequest = true;

    const results = await getPosts(offset, limit);

    if (results.length === 0) {
      emptyAnimationPage = true;
      observer.unobserve(loadTrigger);
    } else {
      console.log(results);
      blockAnimationRequest = false;

      // render data into the browser
      // for (let i = 0; i < limit; i++) {
      //   const post = results[i];
      //   newPostsElements[i].classList.remove(skeletonImageClass);

      //   // create child element
      //   let childAnchorEl = document.createElement("a");
      //   childAnchorEl.href = "";

      //   let imageEl = document.createElement("img");
      //   imageEl.src = `${post.thumbnail}`;
      //   childAnchorEl.appendChild(imageEl);

      //   let paragraph = document.createElement("p");
      //   paragraph.textContent = `${post.episode_title}`;
      //   childAnchorEl.appendChild(paragraph);

      //   console.log(childAnchorEl);

      //   newPostsElements[i].appendChild(childAnchorEl);
      //   console.log(newPostsElements[i]);

      // render data into the browser
      const htmlData = results
        .map((el) => {
          return `
              <div class="page-content-card">
                <a href="postpage.html"
                  ><img src="${el.thumbnail}" alt="${el.episode_title}" />
                  <p>${el.episode_title}</p></a
                >
              </div>
        `;
        })
        .join("");

      console.log(htmlData);
      postAnimationContainerEl.insertAdjacentHTML("beforeend", htmlData);
    }

    // increase offset by 1
    offset += limit;
    console.log(offset);

    // set the total posts
  }
}
// }

/**
 * @param { Number } offset page number
 * @param { limit } limit return data limit
 */
const getPosts = async (offset, limit) => {
  const API_Endpoint = `/content/anime/?limit=${limit}&offset=${offset}`;

  const response = await fetch(API_Endpoint);

  if (!response.ok)
    throw new Error(
      `An error occurred from animationPosts: ${response.statusText}`
    );

  const jsonData = await response.json();
  return jsonData.results;

  // renderPosts(jsonData.results);
};

/**
 * @param { Array } data array of data to be rendered in the browser
 */
const renderPosts = (data, dataElements) => {
  for (let i = 0; i < dataElements.length; i++) {
    const post = dataElements[i];
  }
  //   const htmlData = data
  //     .map((el) => {
  //       return `

  //     <div class="page-content-card">
  //         <a href="postpage.html"><img src="${el.thumbnail}" alt="" />
  //         <p>${el.episode_title}</p></a>
  //     </div>

  //     `;
  //     })
  //     .join("");

  //   animationContainerEl.insertAdjacentHTML("beforeend", htmlData);
};
