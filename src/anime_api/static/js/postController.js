const rootElementPost = document.getElementById("rootPost");
const postBaseURL = "127.0.0.7:8000/";
let blockRequest = false;
let emptyPage = false;
// const {scrollTop, scrollHeight, clientHeight } = document.documentElement;
// console.log("===========================")
// console.log("scrollTop: ", scrollTop)
// console.log("clientHeight: ", clientHeight)
// console.log("scrollHeight: ", scrollHeight)
// console.log("===========================")


const stateURLS = {
  animation: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: `http://127.0.0.1:8000/content/anime`,
    previousURL: "",
  },

  writtenstory: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: `http://127.0.0.1:8000/content/stories`,
    previousURL: "",
  },

  textContent: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: `http://127.0.0.1:8000/content/textcontent`,
    previousURL: "",
  },

  videoContent: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: `http://127.0.0.1:8000/content/videocontent`,
    previousURL: "",
  },

  designContent: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: `http://127.0.0.1:8000/content/designcontent`,
    previousURL: "",
  },

  books: {
    pageNum : 1,
    offset: 3,
    limit: 3,
    nextURL: "",
    previousURL: "",
  },
};


/**
 * 
 * @param {Object} state Checks if there is a value in the state to make a next 
 * @returns bool
 */
const hasMorePosts = function(state){
  if (state.nextURL) return true;
  return false;
}


/**
 *Swaps each selected element in the array with a randomly selected element from the remaining un-shuffled portion of the array.
 *@param {array} array The array to be shuffled
 *
 */
const shuffle = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));

    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

/**
 * Concatenates postBaseURL with endpoint to fetch data from the restAPI. eg: 0.0.0.0:8000/endpoint
 * Do not authentication and errrors returned from the server.
 * @param {string} postBaseURL - base url of the restapi. This is set by default but can be overwritten.
 */
const getData = async function (postBaseURL) {
  try {
    const url = postBaseURL;
    // let access_token = window.localStorage.getItem("dabble_access");
    // const data = await fetch(url, {
    //   headers: {
    //     "Content-type": "application/json",
    //     AUthorization: `Bearer ${access_token}`,
    //   },
    // });
    const data = await fetch(url);

    if (!data.ok)
      throw new Error({
        errorType: "fetch error",
        message: data.message || "fetching data failed",
      });

    const res = await data.json();
    return res;
  } catch (error) {
    // throw new Error(error);
    console.error(error, " 💥💥");
  }
};

/**
 * Returns a random shuffle of data including animation, books, written stories, videos and designs/illustrations and shuffle them before rendering it.
 */
const getPostController = async function () {
  const resData = await Promise.all([
    await getData(`/content/anime/?limit=${stateURLS.animation.limit}`),
    await getData(`/content/stories/?limit=${stateURLS.writtenstory.limit}`),
    await getData(`/content/textcontent/?limit=${stateURLS.textContent.limit}`),
    await getData(`/content/designcontent/?limit=${stateURLS.designContent.limit}`),
    await getData(`/content/videocontent/?limit=${stateURLS.videoContent.limit}`),
    // await getData(`library/books`),
  ]);

  const result = resData.map((el) => el);
  console.log(result, "This is the results from the api")

  // const urlsState = [];
  // const stateConstructorVariables = ['animation', 'stories', 'text', 'design', 'video',]

  // set the state of the urls for the next request
    // for (let i = 0; i < result.length; i++) {
    //   let data = {
    //     next: result[i].next,
    //     previous: result[i].previous,
    //     stateFor: stateConstructorVariables[i],
    //   };

    //   urlsState.push(data);
    // }
  //   console.log(urlsState, "this is the state=====");
  // console.log("from the post controller: ", result, "===========")
  // console.log(stateURLS)

  const flattenResult = result.map((el) => el.results).flat();
  // let shuffledData = shuffle(flattenResult);

  //   Render data in Browser
  renderPostHTML(flattenResult);
};


/**
 * 
 * return Array[json] 
 */
const fetchMorePosts = async () =>{

  const resData = await Promise.all([
    await getData(`/content/anime/?limit=${stateURLS.animation.limit}&offset=${stateURLS.animation.offset}`),
    await getData(`/content/stories/?limit=${stateURLS.writtenstory.limit}&offset=${stateURLS.writtenstory.offset}`),
    await getData(`/content/textcontent/?limit=${stateURLS.textContent.limit}&offset=${stateURLS.textContent.offset}`),
    await getData(`/content/designcontent/?limit=${stateURLS.designContent.limit}&offset=${stateURLS.designContent.offset}`),
    await getData(`/content/videocontent/?limit=${stateURLS.videoContent.limit}&offset=${stateURLS.videoContent.offset}`),
    // await getData(`library/books`),
  ]);

  blockRequest = false;


  const result = resData.map((el) => el);
  const flattenResult = result.map((el) => el.results).flat();
  console.log("length of the data gotten is: 😍", result, flattenResult)
  if (flattenResult.length === 0) {
    emptyPage = true;
    console.log("Got an empty page '''''''''''''''''''--------------''''''''''")
    return;
  }
  else {

     // increase offset by the number of limit
     stateURLS.animation.offset += stateURLS.animation.limit
     stateURLS.writtenstory.offset += stateURLS.writtenstory.limit
     stateURLS.textContent.offset += stateURLS.textContent.limit
     stateURLS.designContent.offset += stateURLS.designContent.limit
     stateURLS.videoContent.offset += stateURLS.videoContent.limit
    renderRequestedPosts(flattenResult)

  };

  // const newData = [];
  // for (let i=0; i < urls.length; i++){
    
  //   if (urls[i].includes("anime")){
  //     let animeState = stateURLS.animation;
  //     let response = await getData(`${urls[i]}/?limit=${animeState.limit}&offset=${animeState.offset}`);
      
  //     newData.push(response);

  //     // change stateurl to reflect the new nextURL
  //     stateURLS.animation.nextURL = response.next;

  //   }else if(urls[i].includes("stories")){
  //     let storiesState = stateURLS.writtenstory;
  //     let response = await getData(`${urls[i]}/?limit=${storiesState.limit}&offset=${storiesState.offset}`);

  //     newData.push(response);

  //      // change stateurl to reflect the new nextURL
  //     stateURLS.writtenstory.nextURL = response.next;

  //   }else if(urls[i].includes("textcontent")){
  //     let textContentState = stateURLS.textContent;
  //     let response = await getData(`${urls[i]}/?limit=${textContentState.limit}&offset=${textContentState.offset}`);

  //     newData.push(response);

  //     // change stateurl to reflect the new nextURL
  //     stateURLS.textContent.nextURL = response.next;

  //   }else if(urls[i].includes("videocontent")){
  //     let videoContentState = stateURLS.videoContent;
  //     let response = await getData(`${urls[i]}/?limit=${videoContentState.limit}&offset=${videoContentState.offset}`);

  //     newData.push(response);

  //     // change stateurl to reflect the new nextURL
  //     stateURLS.videoContent.nextURL = response.next;

  //   }else {
  //     console.error("no urls found")
  //   }

  //   // newData.push(response);
  // }

  // console.log("fetchMorePosts: ", newData, "new data")

  // renderRequestedPosts(newData);

  // set block request to false after the request has been made
  // blockRequest = false;
}








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
  rootElementPost.insertAdjacentHTML("afterbegin", renderedHTML)
};

/**
 * 
 * @param {Array} data renders the subsequent data that was retrieved from the apii 
 */
const renderRequestedPosts = function(data){


  const processData = data.map((el) => {

    return `
     <div class="page-content-card">
          <a href="${el.typeof}/${el.pk ? el.pk : el.id}/${el.slug}">
            <img src="${el.thumbnail || el.illustration}" alt="${
        el.title || el.series_name
      }" />
          <p>${el.title || el.series_name}</p>
          </a>
        </div>
    `
  }).join("")

  rootElementPost.insertAdjacentHTML("beforeend", processData);
}



getPostController();



window.addEventListener('scroll', ()=> {
  const {scrollTop, scrollHeight, clientHeight } = document.documentElement;
  
  // const validRequestURLs = [];
  console.log("The value of empty page from the top is: ", emptyPage)
  
  if (scrollTop + clientHeight >= scrollHeight - 5 && !blockRequest){

    blockRequest = true;

    // call fetchMorePosts to get more data from the backend
      fetchMorePosts()

//     if (hasMorePosts(stateURLS.animation)){
//       validRequestURLs.push(stateURLS.animation.nextURL);
      
//     }
//     if (hasMorePosts(stateURLS.writtenstory)){
//       validRequestURLs.push(stateURLS.writtenstory.nextURL);
//       // stateURLS.writtenstory.offset *=2;
//       // stateURLS.writtenstory.pageNum += 1;stateURLS
//     }
//     if (hasMorePosts(stateURLS.videoContent)){
//       validRequestURLs.push(stateURLS.videoContent.nextURL);
//       // stateURLS.videoContent.offset *= 2
//       // stateURLS.videoContent.pageNum += 1;;
//     }
//     if (hasMorePosts(stateURLS.textContent)){
  //       validRequestURLs.push(stateURLS.textContent.nextURL);
  //       // stateURLS.textContent.offset *=2;
  //       // stateURLS.textContent.pageNum += 1;    
  // }
  
  //     if (validRequestURLs.length >= 1 && !blockRequest){
    //       console.log("============= validRequest urls =============\n")
    //       console.log(validRequestURLs)
    //       console.log("\n============= validRequest urls =============")
    
    //       blockRequest = true;
    //       // Make request to the API
    //       fetchMorePosts(validRequestURLs);
    //     }
    
  }{
    console.log("The value of empty page is now: ", emptyPage)
  }

  
}, {passive: true});