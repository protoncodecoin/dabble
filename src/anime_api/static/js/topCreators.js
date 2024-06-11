const baseURL = `/userprofiles/top_creators/?limit=5`;
const rootElement = document.getElementById("topCreator");
/**
 * Fetch the top creators from the API
 */
const fetchTopCreators = async () => {
  try {
    const res = await fetch((url = baseURL));

    if (!res.ok) throw new Error("res.statusText");

    const jsonData = await res.json();
    const results = jsonData.results;

    // render Data and display in the browser
    renderHTML(results);
  } catch (error) {
    console.log(error, "from the topCreator.js file 💥");
  }

  // console.log(rootElement);
};

/**
 * @param {Array} data accept response data from the server and renders it in the browser
 */
const renderHTML = (data) => {
  let htmlData = data
    .map((el) => {
      return `
            <a class="post" href="/${el.id}/${el.slug}/">
              <img src="${el.creator_logo}" alt="image of ${el.username}" />
              <span>
                <h5>${el.username}</h5>
                <p>${el.programme}</p>
              </span>
              <div class="active">Active</div>
            </a>
        `;
    })
    .join("");

  rootElement.insertAdjacentHTML("beforeend", htmlData);
};

fetchTopCreators();
