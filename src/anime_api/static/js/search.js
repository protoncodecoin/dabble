const searchResultContainerEl = document.querySelector("#search-result-container");

document.querySelector("#search-btn").addEventListener("click", async function(e){
  e.preventDefault();

  // get what user has entered into the search field
  const user_query = document.querySelector("#query").value;

  // search endpoint
  console.log("i got clicked")


  if (user_query){
    // send query to api to get information
    const result = await searchQuery("anime", user_query);

    // loop through the data to display the data
    if (result.length > 0){
      renderSearchResults(result);
    }
  }
})

/**
 * 
 * @param {String} content_type type of post
 * @param {*} query user query
 */
const searchQuery = async (content_type, query) => {
    let searchURL = `http://localhost:8000/content/search/${content_type}/?query=${query}`;

    try {
      const response = await fetch(searchURL);

      if (!response.ok){
        throw new Error(response.status, response.statusText);
      }

      const {result} = await response.json();

      return result;
    } catch (error) {
      console.log(error)
    }


}

const renderSearchResults = (data) => {
  const renderedResult = data.map((el) => {

    switch(el.typeof){
      case "anime":
      case "video":
        return `
        <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                <video
                src="${el.video_file}"
                muted
                autoplay 
                contriols
                poster="${el.thumbnail}"
              ></video>
                <p>${el.episode_title || el.title }</p>
          </div>
        `

      case "book":
        return `
          <div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
            <p class="hidden">${el.content}</p>
          
            <img src="${el.thumbnail}" alt="" />
            <p>${el.title}</p>
            <p>${el.author}</p>
            <button class="show-card">Read</button>
          </div>
        `

      case "writtenstory":
        return `
            <div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                    <p class="hidden">${ el.content}</p>
                  
                    <img src="${el.thumbnail}" alt="${el.episode_title}" alt="${el.episode_title}" />
                    <p>${el.series_name}</p>
                    <p>${el.episode_title}</p>
                    <button class="show-card">Read</button>
              </div>        
        `
      
        case "design":
        case "photography":
          return `
          <div class="page-content-card show-modal">
                <img src="/Portfolio//jennifer_s works/sub.jpg" alt="" />
                <p>Photography</p>
          </div>
          `

        default:
          console.log("something wasn't rendered")
    }
  }).join("");

  searchResultContainerEl.insertAdjacentHTML("beforeend", renderedResult);

}