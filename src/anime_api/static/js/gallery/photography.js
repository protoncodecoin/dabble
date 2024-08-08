const loadTrigger = document.getElementById("load-trigger");
const postPhotographyContainerEl = document.querySelector("#root_photography");
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
      const htmlData = results
        .map((el) => {
          return `
              <div class="page-content-card">
                <a href="postpage.html"
                  ><img src="${el.image}" alt="${el.title}" />
                  <p>${el.title}</p></a
                >
              </div>
        `;
        })
        .join("");

      postPhotographyContainerEl.insertAdjacentHTML("beforeend", htmlData);
    }

    // increase offset by 1
    offset += limit;

    // set the total posts
  }
}
// }

/**
 * @param { Number } offset page number
 * @param { limit } limit return data limit
 */
const getPosts = async (offset, limit) => {
  const API_Endpoint = `/content/photography/?limit=${limit}&offset=${offset}`;

  const response = await fetch(API_Endpoint);

  if (!response.ok)
    throw new Error(
      `An error occurred from photography: ${response.statusText}`
    );

  const jsonData = await response.json();
  return jsonData.results;

};
