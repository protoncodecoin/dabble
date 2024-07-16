const booksContainer = document.querySelector("#books_container");
const loaderEl = document.querySelector(".loaderx");
const innerCircleEl = document.querySelector(".inner-circle");
let currentPage = 1;
let total = 0;
let limit = 7;

const getBooks = async (page, limit) => {
  const API_URL = `/library/books/?page=${page}&limit=${limit}`;

  const response = await fetch(API_URL);

  if (!response.ok)
    throw new Error(`An error occurred from books: ${response.statusText}`);

  const data = await response.json();
  console.log("books: ", data.results);
  return data;
};

// show books
const showBooks = (books) => {
  const htmlData = books
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

  //   console.log(htmlData);

  booksContainer.insertAdjacentHTML("beforeend", htmlData);
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
  return total === 0 || startIndex < total;
};

// load more books
const loadBooks = async (page, limit) => {
  // show the loader
  // showLoader();

  try {
    // if having more quotes to fetch
    if (hasMoreBooks(page, limit, total)) {
      console.log("has more posts");
      // call the API to get quotes
      const response = await getBooks(page, limit);
      // show books
      showBooks(response.results);

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

document
  .querySelector(".categories_post")
  .addEventListener("click", function (e) {
    if (e.target.classList.contains("crd")) {
      console.log(e.target.dataset.category);
    }
  });

const getFilteredPost = async (page, limit, category) => {
  total = 0;
  currentPage = 1;
  const API_URL = `/library/books/book_category=${category}?page=${page}&limit=${limit}`;

  const response = await fetch(API_URL);

  if (!response.ok)
    throw new Error(`An error occurred from books: ${response.statusText}`);

  const data = await response.json();
  console.log("books: ", data.results);
  //   return data;

  //   showBooks(data.results);
  //   total = data.count;
};

// show books
const showFilteredBooks = (books) => {
  const htmlData = books
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

  //   console.log(htmlData);
  booksContainer.insertAdjacentHTML = "";
  booksContainer.insertAdjacentHTML("beforeend", htmlData);
};

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
