const creatorURL = "http://127.0.0.1:8000/userprofiles";
const allFavoritesURL = "/content/action/favorite";
const urlParamater = window.location.href.split("/");
const id = urlParamater[3];
const username = urlParamater[4];
const profilePicEl = document.getElementById("profile-pic");
const creatorNameEl = document.getElementById("creator-name");
const creatorProgrammeEl = document.getElementById("creator-programme");
const creatorBioEl = document.getElementById("biography");
const allCreatorPostsEl = document.querySelector(".allCreatorPosts");
const numOfWorksEl = document.getElementById("numOfWorks");
const postsBtn = document.getElementById("post-tab");
const watchlistEl = document.querySelector(".watchlist-container");
const bannerEl = document.querySelector("#banner");

// const csrftoken = Cookies.get("csrftoken");

const getPostData = async function (baseURL) {
  try {
    const url = baseURL;
    const data = await fetch(url);

    if (!data.ok)
      throw new Error({
        errorType: "fetch error",
        message: data.message || "fetching data failed",
      });

    const res = await data.json();
    return res;
  } catch (error) {
    // throw new Error(error);
    console.log(error);
  }
};

const creatorProfileController = async () => {
  try {
    const res = await fetch(`${creatorURL}/${id}`);

    if (!res.ok) throw new Error(res.statusText);

    const creatorResData = await res.json();

    // update profile
    let {
      creator_logo: logo,
      programme = "Not available",
      biography,
      background_image,
    } = creatorResData;

    // profile pic
    profilePicEl.src = logo;
    profilePicEl.alt = `Profile of ${username}`;

    // banner pic
    bannerEl.src = background_image;
    bannerEl.alt = `Banner of ${username}`;

    // profile username
    creatorNameEl.textContent = username;

    // profile programme
    creatorProgrammeEl.textContent =
      programme == "" ? "Not available" : programme;

    // profile biography // description
    creatorBioEl.textContent =
      biography === null ? "Biography not available" : biography;
  } catch (error) {
    console.log("This error is from profileCreator 😥", error);
  }
};

/**
 * @param {Array} favorites data to render in the browser
 */
const renderUserFavorites = (favorites) => {


  const renderFavData = favorites
    .map((el) => {
      switch (el.typeof) {
        case "anime":
          return `               
               <div class="page-content-card show-modal" data-id="${el.id || el.pk}" data-posttype="${el.typeof}">
                <img src="${el.thumbnail}" alt="${el.series_name}" />
                <p>${el.series_name} | ${el.episode_title}</p>
              </div>
              
              
              `;

        case "writtenstory":
          return `<div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                        <p class="hidden" id="story-content">${el.content}</p>
                      
                        <img src="${el.thumbnail}" alt="${el.series_name}" />
                        <p>${el.episode_title}</p>
                        <p>${el.series_name}</p>
                        <button class="show-card">Read</button>
            </div>
            `;
            
        case "text":
        case "video":
        case "design":
          return `               
              <div class="page-content-card show-modal" data-id="${el.id}" data-posttype="${el.typeof}content">
                <img src="${el.thumbnail || el.illustration}" alt="${el.title}" />
                <p>${el.title}</p>
              </div>
              `;

        case "book":
          return `
               <div class="page-content-card show-modal" data-id="${el.id}" data-posttype="${el.typeof}">
                <img src="${el.cover}" alt="${el.title}" />
                <p>${el.title}</p>
              </div>
        `;

        default:
          console.log(
            "Something wasn't rendered in the all posts of the profile section."
          );
      }
    })
    .join("");

  watchlistEl.insertAdjacentHTML("afterbegin", renderFavData);
};

const creatorAllFavorites = async () => {
  try {
    const res = await fetch(`${allFavoritesURL}/${id}/all/`, {
      credentials: "include",
    });

    if (!res.ok) throw new Error(res.statusText);

    const favJson = await res.json();
    // const results = favJson.results.map((el) => el)[0].anime[0];
    const results = favJson.results
      .map((el) => el)
      .map((el) => el)
      .flat();

    renderUserFavorites(results);
  } catch (error) {
    console.log(error);
  }
};

/**
 * Get all user's post from the API
 * Includes "writtenstories, animations, textcontent, videocontent, designcontent"
 */
const allPostsOfCreator = async () => {
  const user_id = id;
  const query_param = `?id=${user_id}`;

  const resData = await Promise.all([
    await getPostData(`/content/anime/${query_param}`),
    await getPostData(`/content/stories/${query_param}`),
    await getPostData(`/content/textcontent/${query_param}`),
    await getPostData(`/content/designcontent/${query_param}`),
    await getPostData(`/content/videocontent/${query_param}`),
  ]);

  // console.log("all posts of creator", resData);

  const results = resData.map((el) => el.results).flat();
  // console.log(results, "this is the result");

  renderAllUserPosts(results);
};

/**
 *
 * @param {Array} postData data to render in the browser
 */
const renderAllUserPosts = (postData) => {
  numOfWorksEl.textContent =
    postData.length > 1
      ? `${postData.length} artworks`
      : `${postData.length} artwork`;

  const renderedPostHtml = postData
    .map((el) => {
      // console.log(el.typeof, "from all posts");
      switch (el.typeof) {
        case "anime":
          return ` 
          
          <div class="page-content-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                <img src="${el.thumbnail}" alt="${el.series_name}-${el.episode_title}" />
                <p>${el.series_name} | ${el.episode_title}</p>
              </div>
        `;
        case "writtenstory":
          return `
           <div class="book-card show-modal" data-id="${el.id | el.pk}" data-posttype="${el.typeof}">
                        <p class="hidden" id="story-content">${el.content}</p>
                      
                        <img src="${el.thumbnail}" alt="${el.series_name}" />
                        <p>${el.episode_title}</p>
                        <p>${el.series_name}</p>
                        <button class="show-card">Read</button>
            </div>
            `;
        case "text":
        case "video":
        case "design":
          return `

              <div class="page-content-card show-modal" data-id="${el.id || el.pk}" data-posttype="${el.typeof}content">
                <img src="${el.thumbnail || el.illustration}" alt="${el.title}" />
                <p>${el.title}</p>
              </div>
              `;

        default:
          console.log(
            "Something wasn't rendered in the all posts of the profile section."
          );
      }
    })
    .join("");

  allCreatorPostsEl.insertAdjacentHTML("afterbegin", renderedPostHtml);
};

creatorProfileController();
allPostsOfCreator();
creatorAllFavorites();

