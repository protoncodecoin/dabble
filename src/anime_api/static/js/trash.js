```

books

        
              <div class="book-card">
                <img src="${el.cover}" alt="${el.title}" />
                <<p>${el.title}</p>
                <p>${el.author}</p>
                <button><a href="books/${el.id}/${el.slug}/${el.category}">Read</a></button>
              </div>




text video design

<div class="page-content-card">
                <a href="/${el.typeof}/${el.id || el.pk}/${
            el.slug
          }/"><img src="${el.thumbnail || el.illustration}" alt="${el.title}" />
                <p>${el.title}</p></a>
              </div>



anime


<div class="page-content-card">
                <a href="/${el.typeof}/${el.id || el.pk}/${
            el.slug
          }/"><img src="${el.thumbnail}" alt="${el.series_name}-${
            el.episode_title
          }" />
                <p>${el.series_name} | ${el.episode_title}</p></a>
              </div>
              
              
```


  //  {% comment %} watchlistContainerEl.addEventListener("click", function(e){
  //   const selectedWatchListEl = e.target.parentElement;

  //   if (selectedWatchListEl.classList.contains("show-modal")){
  //     modal.classList.remove("hidden");
  //     overlay.classList.remove("hidden");

  //     const selectedWatchListImgSrc = selectedWatchListEl.querySelector("img").getAttribute("src");

  //     // <!-- Fill Modal with necessary data from the selected component -->
  //     modal.querySelector(".post-view").querySelector("img").classList.remove("hidden")
  //     modal.querySelector(".post-view").querySelector("img").setAttribute("src", selectedWatchListImgSrc);


  //     // <!-- Call API to get detail information about selected post-->
  //     const selectedPostId = e.target.parentElement.dataset.id;
  //     const selectedPostType = e.target.parentElement.dataset.posttype;

  //     <!-- use the id and typeof dataset value to compose the url for the detail page-->
  //     const detailData = getDetailedPost(baseDetailURL, selectedPostId, selectedPostType);

  //     if (detailData){
  //       const data = detailData;
  //     }

  //   }
    

  //  }) {% endcomment %}


  /**
   * 
   * @param {String} content_type content_type of the post
   * @param {Number} content_id id of the post
   */
  const likeAndUnlike = async (content_type, content_id) => {
    const url = `localhost:8000/content/action/like/${content_type}/${content_id}/`;

    try {
      
      const response = await fetch(url, {
        headers: {
          'X-CSRFToken': csrf_token,
        },
      })

      if (!response.ok) {
        console.log(response, response.status, response.statusText);
        throw new Error("Couldn't post data to the api")
      }

      const resJon = await response.json();
      console.log(resJon)
    } catch (error) {
      console.log(error)
    }

  }


/**
 * Set the like and fav buttons to their default values
 */ 
  const setDefaultValues = () => {
    //  const likeButton = document.querySelector(".like");
    //   const faveButton = document.querySelector(".fave");

      document.querySelector(".like").setAttribute("src", "{% static 'icons/likeicon2.svg' %}");
      document.querySelector(".fave").setAttribute("src", "{% static 'icons/saveicon2.svg' %}");
  }

  document.querySelectorAll(".slide-btn").forEach((e) => {
    e.addEventListener("click", function(e){

      // check if the btn selected 
      let btn = e.target;

      let dataset = btn.dataset;

      if (btn){
        dataset
      }
    })
  })