const booksURL = "http://127.0.0.1:8000/library/books/";
const recommendedBooksEl = document.getElementById("recommended__books");
console.log(recommendedBooksEl);

const renderBooks = (booksData) => {
  const booksHtml = booksData
    .map((el) => {
      return `
            <div class="book-card">
              <img src="${el.cover}" alt="${el.title}"  />
              <p>${el.title}</p>
              <p>${el.book_category}</p>
              <button><a target="_blank" href="${el.external_link}">Read</a></button>
            </div>`;
    })
    .join("");

  recommendedBooksEl.insertAdjacentHTML("afterbegin", booksHtml);
};

const getBooks = async () => {
  try {
    const resData = await fetch(booksURL);
    if (!resData.ok) return resData.statusText;

    const data = await resData.json();

    const result = data.results;

    renderBooks(result);
  } catch (error) {
    console.log(error);
  }
};

getBooks();
