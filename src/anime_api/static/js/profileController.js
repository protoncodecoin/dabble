const creatorURL = "http://127.0.0.1:8000/userprofiles";
const allFavoritesURL = "/content/action/favorite/all/";
const urlParamater = window.location.href.split("/");
const id = urlParamater[3];
const username = urlParamater[4];
const profilePicEl = document.getElementById("profile-pic");
const creatorNameEl = document.getElementById("creator-name");
const creatorProgrammeEl = document.getElementById("creator-programme");
const creatorBioEl = document.getElementById("biography");
// const csrftoken = Cookies.get("csrftoken");

const creatorProfileController = async () => {
  try {
    const res = await fetch(`${creatorURL}/${id}`);

    if (!res.ok) throw new Error(res.statusText);

    const creatorResData = await res.json();
    console.log(creatorResData);

    // update profile
    let {
      creator_logo: logo,
      programme = "Not available",
      biography,
    } = creatorResData;

    // profile pic
    profilePicEl.src = logo;

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

const creatorAllFavorites = async () => {
  try {
    const res = await fetch(allFavoritesURL, { credentials: "include" });

    if (!res.ok) throw new Error(res.statusText);

    const favJson = await res.json();
    console.log("This is the favorite data: ", favJson);
  } catch (error) {
    console.log(error);
  }
};

creatorProfileController();
creatorAllFavorites();
// console.log(`${allFavoritesURL}?${URLparam.toString()}`);
