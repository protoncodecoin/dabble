const trendsURL = "viewed/most_viewed/";
const rootTrends = document.getElementById("rootTrends");

const trendingPosts = async () => {
  try {
    let res = await fetch(trendsURL);

    if (!res.ok) throw new Error(res.statusText);

    const jsonData = await res.json();

    const {
      anime_trends,
      story_trends,
      design_trends,
      video_trends,
      // text_trends,
    } = jsonData;

    const mergedTrendsData = [
      ...anime_trends,
      ...story_trends,
      ...design_trends,
      ...video_trends,
      // ...text_trends,
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
    .map((el) => {
      return `
                 <div class="trend-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}${el.typeof == "anime" || el.typeof == "writtenstory" ? "" : "content" }">
                  <img src="${el.thumbnail || el.illustration}" alt="${el.series_name || el.title || el.episode_title}" />
                  <p>${el.episode_title || el.title }</p>
                </div>
                      `
    })
    .join("");

    // data.length === 0 ? rootTrends.innerHTML = "<h2> NO Trending Posts </h2>" : rootTrends.insertAdjacentHTML("beforeend", trendshtmlDATA);
    rootTrends.insertAdjacentHTML("beforeend", trendshtmlDATA);
}

trendingPosts();
