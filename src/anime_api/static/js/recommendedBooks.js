const booksURL = "/library/books";
const recommendedBooksEl = document.getElementById("recommended__books");


const getBooks =  async () => {
    try {
        const resData = await fetch(booksURL);
        if (!resData.ok) return resData.statusText;

        const data = await resData.json();

        const result = data.result;
        // console.log(result)
       
        renderBooks(result);
    } catch (error) {
        console.log(error);
    }
    
}

const renderBooks = (booksData) => {
    const booksHtml = booksData.map((el) => {
        return `

         <div class="book-card">
            <img src="${el.cover}" alt="${el.title}" />
            <p>${el.title || "Not Specified"}</p>
            <p>${el.author || "Not Specified"}</p>
            <button><a href="/books/${el.id || el.pk}/${el.slug}/${el.book_category}/">Read</a></button>
        </div>
        `;
    }).join("");

recommendedBooksEl.insertAdjacentHTML("afterbegin", booksHtml);
}

getBooks()