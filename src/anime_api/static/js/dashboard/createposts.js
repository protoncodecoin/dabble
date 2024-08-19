const singleVideoEl = document.querySelector("#create-single-video");

singleVideoEl.addEventListener("submit", async function (e) {
  e.preventDefault();

  const thumbnailInput = document.querySelector("#thumbnail").files[0]; // Correctly reference the file
  const captionInput = document.querySelector("#caption").value;
  const videoInput = document.querySelector("#video").files[0]; // Correctly reference the file
  const tags = document.querySelector("#tags").value;

  const formdata = new FormData();

  if (captionInput !== "") {
    formdata.append("title", captionInput);
  }
  if (thumbnailInput) { // Ensure the file exists before appending
    formdata.append("thumbnail", thumbnailInput);
  }
  if (videoInput) { // Ensure the file exists before appending
    formdata.append("video_file", videoInput);
  }

  const userTags = tags.split(",").map((el) => el.trim());

  userTags.forEach((el) => {
    formdata.append("tags", el);
  });

  // Add creator to the form
  formdata.append("creator", creatorName);

  try {
    let response = await fetch("http://localhost:8000/content/videocontent/", {
      headers: {
        "X-CSRFToken": csrf_token,
      },
      credentials: "same-origin",
      method: "POST",
      body: formdata,
    });

    if (!response.ok) {
      console.log("Response status:", response.status);
      console.log("Response text:", await response.text());
      throw new Error("Failed to post data", response);
    }

    const resData = await response.json();
    console.log(resData, "this is the response data from the form endpoint");
  } catch (error) {
    console.error(error, "🤔 from the video form submission");
  }
});


// post story
document.querySelector('#story-btn').addEventListener("submit", function(e){
  e.preventDefault();

  const story_title = document.querySelector("#story_title").value;
  const story_synopsis = document.querySelector("#story_synopsis").value;
  const story_content = document.querySelector("#story_content").value;
  const story_tags = document.querySelector("#story_tags");

  const newStoryForm = new FormData();

  if (story_title){
    newStoryForm.append("title", story_title)
  } if (story_content){
    newStoryForm.append("synopsis", story_synopsis)
  }
    


})