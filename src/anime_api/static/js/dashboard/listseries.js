const seriesRoot = document.querySelector("#series_container");
let seriesLoaderEl = document.querySelector(".loaderx");
let seriesInnerCircleEl = document.querySelector(".inner-circle");

"http://localhost:8000/content/episodes/all/"

let currentPage = 1;
let total = 0;
let limit = 7;

const hideLoader = () => {
  seriesLoaderEl.style.display = "none";
  seriesInnerCircleEl.style.display = "none";
};

const showLoader = () => {
  seriesLoaderEl.style.display = "flex";
  seriesInnerCircleEl.style.display = "flex";
};

const getSeries = async (page, limit) => {
  // const API_URL = `http://127.0.0.1:8000/content/series/?page=${page}&limit=${limit}`;
  const API_URL = `http://localhost:8000/content/episodes/all/`
  const response = await fetch(API_URL);

  if (!response.ok)
    throw new Error(`An error occurred from books: ${response.statusText}`);

  const {data} = await response.json();
  console.log(data, "series data");
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
            <div class="page-content-card show-card" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                          <!-- <a href="#"> -->
                            <video
                            src="${el.video_file }"
                            muted
                            loop
                            poster="${el.thumbnail}"
                          ></video>
                          <p>${el.series_name}</p>
                          <!-- </a> -->
                        </div>
    `;
          })
          .join("");

  htmlData == 0
    ? (seriesRoot.innerHTML = "<h3>No content</h3>")
    : seriesRoot.insertAdjacentHTML("beforeend", htmlData);
};

const hasMoreSeries = (page, limit, total) => {
  const startIndex = (page - 1) * limit + 1;
  // return total === 0 || startIndex < total;
  return total === 0 || startIndex < total;
};

// load more books
const loadSeries = async (page, limit, callback = showSeries) => {
  // show the loader
  showLoader();

  try {
    // if having more books to fetch
    // if (hasMoreSeries(page, limit, total)) {
    //   console.log("has more posts");
    //   // call the API to get books
    //   const response = await getSeries(page, limit);
    //   // show books
    //   callback(response.results);

    //   // update the total
    //   total = response.count;
    //   console.log("total: ", total);
    // }

    const response = await getSeries();
    callback(response[1])
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
//     const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

//     if (
//       scrollTop + clientHeight >= scrollHeight - 10 &&
//       hasMoreSeries(currentPage, limit, total)
//     ) {
//       currentPage++;
//       loadSeries(currentPage, limit);
//     }
//   },
//   {
//     passive: true,
//   }
// );

loadSeries(currentPage, limit);
