const singleVideoEl = document.querySelector("#create-single-video");

/**
 * Post individual videos to the API
 */
singleVideoEl.addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.currentTarget;
  const formdata = new FormData(form);

  //   split tags string to get individual tags to post
  let tags = formdata.get("tags").split(",");

  // delete initial tags from the form data
  formdata.delete("tags");

  // append new tags to the formdata 
  tags.map((el) => {
    formdata.append("tags", el);
  });

  //   add the creator to the form
  formdata.append("creator", creatorName);

  //   console.log(csrf_token, "this is the token");

  try {
    let response = await fetch("http://127.0.0.1:8000/content/videocontent/", {
      headers: {
        "X-CSRFToken": csrf_token,
        // "Content-Type": "multipart/form-data",
      },
      credentials: "same-origin",
      method: "POST",
      body: formdata,
    });
    if (!response.ok)
      throw new Error("failed to post data", response.statusText);
    const resData = await response.json();
    console.log(resData, "this is the response data from the form endpoint");
  } catch (error) {
    console.error(error.message, "🤔 from the video form submission");
  }
});

const submitPost = async () => {};


fetch("", {
  
})