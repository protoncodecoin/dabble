const accordionContainerEl = document.querySelector("#accordion_container");


accordionContainerEl.addEventListener("click", async function(e){
    if (e.target.classList.contains("px-chat-component")){
        // get the id of the user
        let userID = e.target.dataset.id;

        
        // instantiate a web socket with the clicked user's id
         // INDIVIDUAL CHATTING FUNCTIONALITY
     const chatURL = 'ws://' + window.location.host + `/ws/chat/individual/${userID}/`;
     const individualSocket = new WebSocket(chatURL);

     // select the input field to get message
        const curSibling = e.target.nextElementSibling; // button element
        console.log(curSibling, "curslbiing");
        
        if (!curSibling){
            return;
        }else {

            // get chat messages from API and render chat in DOM
            const chatResults = await getChatMessages(+userID);
            
            // render chat in DOM
            const parentChatEl = curSibling.querySelector("#chat-body");
            renderChat(chatResults, parentChatEl)



            // select and add click event to the submit btn 
            let submitBtn = curSibling.querySelector("#submit-btn");
            submitBtn.addEventListener("click", function(e){
                const userInput = curSibling.querySelector("#user-input");
                const userMsg = userInput.value;

                const chat = `
                <div class="right-row">
                  <div class="bubble">
                   ${userMsg}
                  </div>
                  <p class="time">
                    9:36am
                  </p>
                </div>
                `

                curSibling.querySelector("#chat-body").insertAdjacentHTML("beforeends", chat)

                if (userMsg) {
                    // send message in JSON Format to other user
                    individualSocket.send(JSON.stringify({"message": userMsg}));

                    // clear input
                    userInput.value= "";
                }
            });

        }
    

        

    // Listen for new messages from consumer
      individualSocket.onmessage = function(event){
        const data = JSON.parse(event.data);

        const chatEL = document.querySelector("#chat-body")

        const dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true};
        const datetime = new Date(data.datetime).toLocaleString('en', dateOptions);

        
        let chatData = `
        <div class="left-row">
            <div class="name-img">
              <a href="profilepage.html">
                <img src="{% url 'anime_html:profile_page' user.creator_profile.id user.creator_profile.slug  %}" alt="" />
              </a>
              <p>${data.from_user}</p>
            </div>
            <div class="bubble">
              ${data.message}
            </div>
            <p class="time">
              ${datetime}
            </p>
          </div>
        
        `

        console.log(chatData);
        chatEL.insertAdjacentHTML("beforeend", chatData);

      }

      // Listen for close event from consumer 
        individualSocket.onclose = function(event){
          console.log("Socket close unexpectedly");
        }
    }
})


/**
 * 
 * @param {number} other_user_id id of the other user to get the messages between authenticated user  
 */
const getChatMessages = async (other_user_id) => {

    try {
        const results = await fetch(`/socialize/chat/messages/?other=${other_user_id}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': chat_csrf_token,
                },
                credentials: "include"
            });

        if (!results.ok) {
            console.log("An error occurred: ", results.status, results.statusText);
            throw Error("An error occurred");
        }
        
    const jsonData = await results.json();

    const fromUserProfile = jsonData.results[0].from_user.user_profile;
    const currentUserProfile = jsonData.results[0].to_who.user_profile;

        // get user profile
    const usersProfiles = await Promise.all([
        await getProfile(fromUserProfile), 
        await getProfile(currentUserProfile)
    ]);

    const resultProfiles = usersProfiles.map((el) => el.creator_logo);

    // renderChat([jsonData, resultProfiles])
    return [jsonData, resultProfiles];

    } catch (error) {
        console.log(error)
    }
    
}

const getProfile = async (url) => {
    try {
        const response = await fetch(url);

        if (!response.ok) throw Error("Could not get Profile");

        const jsonData = await response.json();

        return jsonData;
        
    } catch (error) {
        console.log(error);
    }

}

/**
 * 
 * @param {Array} data data of chat and user profile images
 */
const renderChat =  function (data, parentEl) {
    console.log(data, 'this is the data passed')
            // format date
        const dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true};
        
        const chatHTML = data[0].length <= 0 ? 0 : data[0].results.map((el) => {
            
            const datetime = new Date(el.sent_on).toLocaleString('en', dateOptions);
            if (el.from_user.username == requestUser){
            return `
                <div class="right-row">
                  <div class="bubble">
                    ${el.message}
                  </div>
                  <p class="time">
                    ${datetime}
                  </p>
                </div>             
            `
            }else 
                return `
                <div class="left-row">
                  <div class="bubble">
                   ${el.message}
                  </div>
                  <p class="time">
                    ${datetime}
                  </p>
                </div>               
                
                `
            }

           
        ).join("");
        parentEl.innerHTML = "";
        parentEl.insertAdjacentHTML("beforeend", chatHTML);
}