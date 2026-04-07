'use strict'

let addChatButton = document.getElementById('addChatButton');
let addChatPopUp = document.getElementById('addChatPopUp');

let chatsHeader = document.querySelector('.chats-header');
let chatsWrapper = document.querySelector('.chats-wrapper');

let popUpOpened = false;

let toggleStyles = () => {
    if (addChatPopUp.style.display == 'none') {
        addChatPopUp.style.display = 'block'

        chatsHeader.style.filter = 'brightness(50%)';
        chatsWrapper.style.filter = 'brightness(50%)';

        chatsHeader.style.userSelect = 'none';
        chatsWrapper.style.userSelect = 'none';
    }

    else if (addChatPopUp.style.display == 'block') {
        addChatPopUp.style.display = 'none';

        chatsHeader.style.removeProperty('filter');
        chatsWrapper.style.removeProperty('filter');

        chatsHeader.style.removeProperty('user-select');
        chatsWrapper.style.removeProperty('user-select');
    }

    popUpOpened = !popUpOpened;
};

document.addEventListener('keydown', (event) => {
    if (event.key == 'Escape' && popUpOpened)
        toggleStyles();
});

addChatButton.addEventListener('click', toggleStyles);

let chats = document.querySelectorAll('.chat');

let activeChat = document.getElementById('activeChat');
let currentUser = document.getElementById('currentUser').innerHTML;

let currentChatIdInput = document.getElementById('id_chat_id');

let currentChatId = JSON.parse(document.getElementById('userCurrentChat').textContent).toString();

let getCSRFToken = () => {
    let csrftoken;
    const cookieParsed = document.cookie.split("; ");

    for (let i = 0; i < cookieParsed.length; i++) {
        if (cookieParsed[i].includes("csrftoken")) {
            csrftoken = cookieParsed[i].slice(10);

            break;
        }
    }

    return csrftoken;
};

chats.forEach((chat) => {
    chat.addEventListener('click', () => {
        currentChatIdInput.value = chat.id;

        let csrftoken = getCSRFToken();

        let xhr = new XMLHttpRequest();

        xhr.open('POST', '/get_chat_messages', true);

        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onload = () => {
            if (xhr.status == 200) {
                const response = JSON.parse(xhr.responseText);

                activeChat.innerHTML = '';

                response.forEach((message) => {
                    let sender = message['sender__username'];
                    let text = message['text'];

                    let messageWrapperEl = document.createElement('div');
                    let messageEl = document.createElement('div');

                    messageWrapperEl.appendChild(messageEl);

                    messageEl.innerHTML = text;

                    if (currentUser == sender) {
                        messageWrapperEl.classList.add('my-message-wrapper');
                        messageEl.classList.add('my-message');
                    }

                    else {
                        messageWrapperEl.classList.add('other-message-wrapper');
                        messageEl.classList.add('other-message');
                    }

                    activeChat.appendChild(messageWrapperEl);
                });
            }
        };

        const data = JSON.stringify({'id': chat.id});

        if (currentChatId != chat.id) {
            currentChatId = chat.id;

            xhr.send(data);
        }
    });
});
