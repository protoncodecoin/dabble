const trendsURL = "viewed/most_viewed/";
const rootTrends = document.getElementById("rootTrends");

const trendingPosts = async () => {
  try {
    let res = await fetch(mostViewedURL);

    if (!res.ok) throw new Error(res.statusText);

    const jsonData = await res.json();
    const {
      anime_trends,
      story_trends,
      design_trends,
      video_trends,
      text_trends,
    } = jsonData;

    const mergedTrendsData = [
      ...anime_trends,
      ...story_trends,
      ...design_trends,
      ...video_trends,
      ...text_trends,
    ];

    // Render data in browser
    renderTrendsHTML(mergedTrendsData.slice(0, 6));
  } catch (error) {
    console.log("error from mostViewed💥", error);
  }
};

/**
 * @param {Array} data accept response data from the server and renders it in the browser
 */
function renderTrendsHTML(data) {
  let trendshtmlDATA = data
    .filter((el) => el !== "None")
    .map((el) => {
      return `

                <div class="trend-card">
                  <a href="${el.id || el.pk}/${el.typeof}">
                    <img src="${el.thumbnail || el.illustration}" alt="${el.episode_title}" />
                  <p>${el.title || el.episode_title}</p>
                  </a>
                </div>`
    })
    .join("");
  rootTrends.insertAdjacentHTML("beforeend", trendshtmlDATA);
}

trendingPosts();
