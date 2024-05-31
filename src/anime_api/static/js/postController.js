const rootElement = document.getElementById("rootPost");

const baseURL = "127.0.0.7:8000/";

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
 * Concatenates baseURL with endpoint to fetch data from the restAPI. eg: 0.0.0.0:8000/endpoint
 * Do not authentication and errrors returned from the server.
 * @param {string} baseURL - base url of the restapi. This is set by default but can be overwritten.
 */
const getData = async function (baseURL) {
  try {
    const url = baseURL;
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
    console.log(error);
  }
};

/**
 * Returns a random shuffle of data including animation, books, written stories, videos and designs/illustrations and shuffle them before rendering it.
 */
const getPostController = async function () {
  const resData = await Promise.all([
    await getData("/content/anime/"),
    await getData("/content/stories/"),
    await getData("/content/textcontent/"),
    await getData("/content/designcontent/"),
    await getData("/content/videocontent/"),
    // await getData(`library/books`),
  ]);

  const result = resData.map((el) => el);

  // set the state of the urls for the next request
  //   for (let i = 0; i < result.length; i++) {
  //     let data = {
  //       next: result[i].next,
  //       previous: result[i].previous,
  //       stateFor: stateConstructorVariables[i],
  //     };

  //     urlsState.push(data);
  //   }
  //   console.log(urlsState);

  const flattenResult = result.map((el) => el.results).flat();
  let shuffledData = shuffle(flattenResult);

  //   Render data in Browser
  renderHTML(shuffledData);
};

/**
 * @param {Array} data accept response data from the server and renders it in the browser
 */
const renderHTML = function (data) {
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

  rootElement.insertAdjacentHTML("beforeend", renderedHTML);
};

getPostController();
