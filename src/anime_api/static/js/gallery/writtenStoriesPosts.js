const loadTrigger = document.getElementById("load-trigger");
const imageClass = "page-content-card";
const skeletonImageClass = "skeleton-image";
const postAnimationContainerEl = document.querySelector("#gallery_stories");
const throttleTime = 1000;
let throttleTimer = false;
let offset = 1;
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

  // load more post from the server
  // getPosts(0, 1);-
  if (!emptyAnimationPage && !blockAnimationRequest) {
    blockAnimationRequest = true;

    try {
      const results = await getPosts(offset, limit);

    if (results.length === 0) {
      emptyAnimationPage = true;
      observer.unobserve(loadTrigger);
    } else {
      console.log(results);
      blockAnimationRequest = false;

      // render data into the browser
      const htmlData = results
        .map((el) => {
          return `
              <div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                <p class="hidden">${ el.content}</p>
              
                <img src="${el.thumbnail}" alt="${el.episode_title}" alt="${el.episode_title}" />
                <p>${el.series_name}</p>
                <p>${el.episode_title}</p>
                <button class="show-card">Read</button>
              </div>

        `;
        })
        .join("");

      postAnimationContainerEl.insertAdjacentHTML("beforeend", htmlData);

          // increase offset by 1
    offset += limit;
    console.log(offset);
    }
      
    } catch (error) {
      console.log("done")
    }


    // set the total posts
  }
}
// }

/**
 * @param { Number } offset page number
 * @param { limit } limit return data limit
 */
const getPosts = async (offset, limit) => {

  try {
    const API_Endpoint = `/content/writtenstory/?limit=${limit}&page=${offset}`;
    console.log(API_Endpoint)

    const response = await fetch(API_Endpoint);

  if (!response.ok)
    throw new Error(
      `${response.statusText}`
    );

  const jsonData = await response.json();
  return jsonData.results;

  } catch (error) {
    throw new Error(error);
  }
  

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
