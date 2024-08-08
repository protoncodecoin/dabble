const booksContainer = document.querySelector("#books_container");
const loaderEl = document.querySelector(".loaderx");
const innerCircleEl = document.querySelector(".inner-circle");
const authenticatedUser = document.querySelector("#request-user")
const userFavBooksEl = document.querySelector("#fav_books");
let currentPage = 1;
let total = 0;
let limit = 10;
let filteredResStatus = true;
let currentURL = `/library/books`;



const getBooks = async (page, limit, url = currentURL) => {
  let URL = url.endsWith("&")
    ? `${url}page=${page}&limit=${limit}`
    : `${url}/?page=${page}&limit=${limit}`;
  const response = await fetch(URL);

  if (!response.ok)
    throw new Error(`An error occurred from books: ${response.statusText}`);

  const data = await response.json();
  // filteredResStatus = data.results.length == 0 ? false : true;
  return data;
};

// show books

/**
 *
 * @param {Array} books to render list of books in the dom
 */
const showBooks = (books) => {
  const htmlData =
    books.length <= 0
      ? 0
      : books
        .map((el) => {
          return `
        <div class="book-post">
            <img src="${el.cover}" alt="${el.title}">
            <p>${el.title}</p>
            <button>
              <a href="#">Read</a></button>
          </div>
    `;
        })
        .join("");

  htmlData == 0
    ? (booksContainer.innerHTML = "<h3>No content</h3>")
    : booksContainer.insertAdjacentHTML("beforeend", htmlData);
};

const hideLoader = () => {
  loaderEl.style.display = "none";
  innerCircleEl.style.display = "none";
};

const showLoader = () => {
  loaderEl.style.display = "flex";
  innerCircleEl.style.display = "flex";
};

const hasMoreBooks = (page, limit, total) => {
  const startIndex = (page - 1) * limit + 1;
  // return total === 0 || startIndex < total;
  return total === 0 || startIndex < total;
};

// load more books
const loadBooks = async (page, limit, callback = showBooks) => {
  // show the loader
  showLoader();

  try {
    // if having more books to fetch
    if (hasMoreBooks(page, limit, total)) {
      console.log("has more posts");
      // call the API to get books
      const response = await getBooks(page, limit);
      // show books
      callback(response.results);

      // update the total
      total = response.count;
      console.log("total: ", total);
    }
  } catch (error) {
    console.log(error);
  } finally {
    // hide animation
    hideLoader();
  }
};

// Filtering posts
// when user clicks on filtered card
// get what the user clicked on
// build a url with with what the user clicked on
// reset the global url variable to the new variable
// call the api to get the data and replace the old data with
// the new data

document
  .querySelector(".categories_post")
  .addEventListener("click", function (e) {
    if (e.target.classList.contains("crd")) {
      const targetValue = e.target.dataset.category;

      const buildURL =
        targetValue == "general"
          ? `/library/books`
          : `/library/books/?book_category=${targetValue}&`;

      console.log("currentURL: ", buildURL);
      // Reset the URL and load the filtered books
      currentURL = buildURL;
      // booksContainer.innerHTML = ""; // Clear the previous books
      total = 0; // Reset the total count
      currentPage = 1; // Reset the current page
      loadBooks(currentPage, limit, showFilteredBooks);
    }
  });

// show filtered books
/**
 *
 * @param {Array} books render list of filtered books in the browser
 */
const showFilteredBooks = (books, rootContainerEl = booksContainer) => {
  const htmlData =
    books <= 0
      ? 0
      : books
        .map((el) => {
          return `
        <div class="book-post">
            <img src="${el.cover}" alt="${el.title}">
            <p>${el.title}</p>
            <button>
              <a href="#">Read</a></button>
          </div>
    `;
        })
        .join("");

  if (htmlData) {
    rootContainerEl.innerHTML = ""; // Clear previous books
    rootContainerEl.insertAdjacentHTML("beforeend", htmlData);
  } else {
    rootContainerEl.innerHTML = `
      <div style='padding:10px;margin:20px;text-align:center;'>
          <h2 style='margin: 0 auto;'>No Content Yet</h2>
      </div>
    `; // Clear previous books
    // booksContainer.textContent = "<h2>No Content </h2>";
  }
};

/**
 * Get books authenticated user has added to their favorite 
 */
const favoritedBooks = async () => {
  const authUserId = authenticatedUser.textContent;
  if (authUserId) {
    try {
      showLoader()

      const resData = await fetch(`/library/books/${authUserId}/favorites`);

      if (!resData.ok) throw Error("'something went wrong", resData.statusText, resData.status);

      const jsonData = await resData.json();

      console.log("favoritedbooks: ", jsonData.results)

      // render books in the DOM
      showFilteredBooks(jsonData.results, userFavBooksEl);

    } catch (error) {
      console.log("An error occurred", error)
    } finally {
      hideLoader()
    }
  } else {
    // either user is not authenticated or user hasn't added any books to favorite
    userFavBooksEl.innerHTML = `
     <div style='padding:10px;margin:20px;text-align:center;'>
          <h2 style='margin: 0 auto;'>No Books Added to Favorites Yet!.</h2>
      </div>
    
    `
  }


}


window.addEventListener(
  "scroll",
  () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    if (
      scrollTop + clientHeight >= scrollHeight - 10 &&
      hasMoreBooks(currentPage, limit, total)
    ) {
      currentPage++;
      loadBooks(currentPage, limit);
    }
  },
  {
    passive: true,
  }
);

loadBooks(currentPage, limit);
favoritedBooks()