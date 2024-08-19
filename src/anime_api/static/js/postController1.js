const rootElementPost = document.getElementById("rootPost");
const postBaseURL = "127.0.0.7:8000/";
let recommendationURL = `/content/recommendation`;
let currentPage = 1;
let total = 0;
let limit = 7;



/**
 *Swaps each selected element in the array with a randomly selected element from the remaining un-shuffled portion of the array.
 *@param {array} array The array to be shuffled
 *
 */
const shuffleRecommedation = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));

    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};



/**
 * 
 * @param {Number} page 
 * @param {Number} limit 
 * @param {String} url 
 * @returns json array of the data
 */
const getRecommendedPosts = async (page, limit = 7, url = recommendationURL) => {
  try {
      let URL = url.endsWith("&")
    ? `${url}page=${page}&limit=${limit}`
    : `${url}/?page=${page}&limit=${limit}`;


  const response = await fetch(URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token
    },
    credentials: "include"
  });

  if (!response.ok)
    throw new Error(`An error occurred from recommended posts: ${response.statusText, response.status}`);


  const data = await response.json();
 
  
  return data;
} catch (error) {
  console.log(error)
  }

};


/**
 *
 * @param {Array} posts to render list of recommended posts in the dom
 */
const showRecommendedPosts = (posts) => {
  const htmlData =
    posts.length <= 0
      ? 0
      : posts
        .map((el) => {
                switch (el.typeof) {
                    case "anime":
                      return `           
                      <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                          <img src="${el.thumbnail}" alt="${el.series_name}" />
                          <p>${el.series_name} | ${el.episode_title}</p>
                      </div>`;

                    case "writtenstory":
                      return `
                              
                      <div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                        <p class="hidden" id="story-content">${el.content}</p>
                      
                        <img src="${el.thumbnail}" alt="${el.series_name}" />
                        <p>${el.episode_title}</p>
                        <p>${el.series_name}</p>
                        <button class="show-card">Read</button>
                    </div>
                        `;
                    case "video":
                      return `

                        <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}content">
                          <!-- <a href="#"> -->
                            <video
                            src="${el.video_file}"
                            muted
                            loop
                            poster="${el.thumbnail}"
                          ></video>
                          <p>${el.title}</p>
                          <!-- </a> -->
                        </div>
                      `
                    // case "text":
                    case "design":
                        return ` 
                        
                          <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}content">
                            <img src="${el.thumbnail || el.illustration}" alt="${el.title}" />
                            <p>${el.title}</p>
                          </div>
                        `;

                    case "photography":
                      return `
                      <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                        <img src="${el.image}" alt="${el.title}" />
                          <p>${el.title}</p>
                      </div>
                      `

                      default:
                        console.log(
                          "Something wasn't rendered in the all posts of the profile section."
                        );
                  };
        })
        .join("");

  htmlData == 0
    ? (rootElementPost.innerHTML = "<h3>No content</h3>")
    : rootElementPost.insertAdjacentHTML("beforeend", htmlData);
};

/**
 * @param {Array} data accept response data from the server and renders it in the browser
 */
const renderPostHTML = function (data) {
  let renderedHTML = data
    .map((el) => {
      return `
        <div class="page-content-card">
          <a href="${el.typeof}/${el.pk ? el.pk : el.id}/${el.slug}">
            <img src="${el.thumbnail || el.illustration}" alt="${
        el.title || el.series_name
      }" />
          <p>${el.title || el.series_name}</p>
          </a>
        </div>
      `;
    })
    .join("");

  // rootElementPost.insertAdjacentHTML("after", renderedHTML);
  rootElementPost.insertAdjacentHTML("afterbegin", renderedHTML);
};

const hasMoreRecommendedPosts = (page, limit, total) => {
  const startIndex = (page - 1) * limit + 1;
  // return total === 0 || startIndex < total;
  return total === 0 || startIndex < total;
};




// load more recommendposts
const loadRecommendedPosts = async (page, limit, callback = showRecommendedPosts) => {
  // show the loader
  // showLoader();

  try {
    // if having more recommendposts to fetch
    if (hasMoreRecommendedPosts(page, limit, total)) {
      // call the API to get recommended posts
      const response = await getRecommendedPosts(page, limit);

      // shuffle data to make appearance
      const shuffledData = shuffleRecommedation(response.results)

      // show recommended posts
      callback(shuffledData);

      // update the total
      total = response.count;
    }
  } catch (error) {
    console.log(error);
  } finally {
    // hide animation
    // hideLoader();
  }
};

window.addEventListener(
  "scroll",
  () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    if (
      scrollTop + clientHeight >= scrollHeight - 10 &&
      hasMoreRecommendedPosts(currentPage, limit, total)
    ) {
      currentPage++;
      loadRecommendedPosts(currentPage, limit);
    }
  },
  {
    passive: true,
  }
);

loadRecommendedPosts(currentPage, limit);
