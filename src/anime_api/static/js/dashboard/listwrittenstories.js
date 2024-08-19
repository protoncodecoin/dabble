(function () {
  const storiesContainer = document.querySelector("#written_stories_root");
  let storiesLoaderEl = document.querySelector(".loaderx");
  let storiesInnerCircleEl = document.querySelector(".inner-circle");
  let currentPage = 1;
  let total = 0;
  let limit = 7;

  const hideLoader = () => {
    storiesLoaderEl.style.display = "none";
    storiesInnerCircleEl.style.display = "none";
  };

  const showLoader = () => {
    storiesLoaderEl.style.display = "flex";
    storiesInnerCircleEl.style.display = "flex";
  };

  const getWrittenStories = async (page, limit) => {
    // const API_URL = `http://127.0.0.1:8000/content/stories/?page=${page}&limit=${limit}`;
    const API_URL = `http://localhost:8000/content/episodes/all/`

    const response = await fetch(API_URL);

    if (!response.ok)
      throw new Error(`An error occurred from books: ${response.statusText}`);

    const {data} = await response.json();
    console.log(data, "writtenstories data");
    return data;
  };

  // show series

  /**
   *
   * @param {Array} series to render list of series in the dom
   */
  const showSeries = (series) => {
    console.log(series, "passed to the func");
    const htmlData =
      series.length <= 0
        ? 0
        : series
            .map((el) => {
              return `
        <div class="book-card show-card" data-id="${el.id || el.pk}" data-posttype="${el.typeof}">
            <p class="hidden">${el.content}</p>
             <img src="${el.thumbnail}" alt="${el.series_name}" />
            <p>${el.episode_title}</p>
            <p>${el.series_name}</p>
            <button class="show-card">Read</button>
        </div> 
    `;
            })
            .join("");

    htmlData == 0
      ? (storiesContainer.innerHTML = "<h3>No content</h3>")
      : storiesContainer.insertAdjacentHTML("beforeend", htmlData);
  };

  const hasMoreWrittenStories = (page, limit, total) => {
    const startIndex = (page - 1) * limit + 1;
    // return total === 0 || startIndex < total;
    return total === 0 || startIndex < total;
  };

  // load more books
  const loadWrittenStories = async (page, limit, callback = showSeries) => {
    // show the loader
    showLoader();

    try {
      // // if having more books to fetch
      // if (hasMoreWrittenStories(page, limit, total)) {
      //   console.log("has more posts");
      //   // call the API to get books
      //   const response = await getWrittenStories(page, limit);
      //   // show books
      //   callback(response.results);

      //   // update the total
      //   total = response.count;
      //   console.log("total: ", total);
      // }
      const response = await getWrittenStories(page, limit);
        // show books
        callback(response[0]);
    } catch (error) {
      console.log(error);
    } finally {
      // hide animation
      hideLoader();
    }
  };

  // window.addEventListener(
  //   "scroll",
  //   () => {
  //     const { scrollTop, scrollHeight, clientHeight } =
  //       document.documentElement;

  //     if (
  //       scrollTop + clientHeight >= scrollHeight - 10 &&
  //       hasMoreWrittenStories(currentPage, limit, total)
  //     ) {
  //       currentPage++;
  //       loadWrittenStories(currentPage, limit);
  //     }
  //   },
  //   {
  //     passive: true,
  //   }
  // );

  loadWrittenStories(currentPage, limit);
})();
