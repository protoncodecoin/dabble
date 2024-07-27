const mostViewedURL = "viewed/most_viewed/";
const rootMostViewed = document.getElementById("rootMostViewed");

console.log(mostViewedURL);
/**
 *
 * @param {Array} data Returns none if data is empty
 * @returns {Array}
 */
const filterData = (data) => {
  console.log("========================")
  console.log(data)
  let result = [];
  if (data.length !== 0 || data.length > 0) {
    for (let i = 0; i < data.length; i++) {
      result.push(data[i]);
    }
    console.log("===============")
    console.log(result)
    console.log("============")
    return result;
  }
  return "None";
};

const mostViewedPost = async () => {
  try {
    let res = await fetch(mostViewedURL);

    if (!res.ok) throw new Error(res.statusText);

    const jsonData = await res.json();

    const {
      anime_most_viewed,
      writtenstory_most_viewed,
      video_most_viewed,
      text_most_viewed,
      design_most_viewed,
    } = jsonData;

    console.log(design_most_viewed)

    const mergedData = [
      ...anime_most_viewed.slice(0, 1),
      ...writtenstory_most_viewed.slice(0, 1),
      ...video_most_viewed.slice(0, 1),
      ...text_most_viewed.slice(0, 1),
      ...design_most_viewed.slice(0, 1),
    ];

    console.log("merged", mergedData)

    const newRank = filterData(mergedData);

    // Render data in browser
    renderMostViewedHTML(newRank.slice(0, 6));
  } catch (error) {
    console.log("error from mostViewed💥", error);
  }
};

/**
 * @param {Array} data accept response data from the server and renders it in the browser
 */
function renderMostViewedHTML(data) {
  let htmlData = data
    .filter((el) => el !== "None")
    .map((el) => {
      return `
          <a class="post" href="/${el.typeof}/${el.id}/${el.slug}/">
                <img src="${el.thumbnail || el.illustration}" alt="${
        el.episode_title
      }" />
              <span>
                <p>${el.title || el.episode_title}</p>
                <h5>${el.creator_username}</h5>
              </span>
            </a>
        `;
    })
    .join("");

  rootMostViewed.insertAdjacentHTML("beforeend", htmlData);
}

mostViewedPost();
