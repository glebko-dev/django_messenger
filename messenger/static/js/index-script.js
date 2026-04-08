'use strict'

let addChatButtonOpen = document.getElementById('addChatButtonOpen');
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

addChatButtonOpen.addEventListener('click', toggleStyles);

let activeChat = document.getElementById('activeChat');
let currentUser = document.getElementById('currentUser').innerHTML;

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

let showMessages = (data) => {
    activeChat.innerHTML = '';

    data.forEach((message) => {
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
};

let reloadChats = () => {
    let chats = document.querySelectorAll('.chat');

    chats.forEach((chat) => {
        chat.addEventListener('click', () => {
            let csrftoken = getCSRFToken();

            let xhr = new XMLHttpRequest();

            xhr.open('POST', '/get_chat_messages', true);

            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.onload = () => {
                if (xhr.status == 200) {
                    const response = JSON.parse(xhr.responseText);

                    showMessages(response);
                }

                else if (xhr.status == 404)
                    window.location.reload();
            };

            const data = JSON.stringify({'id': chat.id});

            if (currentChatId != chat.id) {
                currentChatId = chat.id;

                xhr.send(data);
            }
        });
    });
};

reloadChats();

let allChats = document.getElementById('chats');

let sendMessageButton = document.getElementById('sendMessageButton');
let messageText = document.getElementById('messageText');

let addChat = (data) => {
    let chatDiv = document.createElement('div');

    chatDiv.classList.add('chat')
    chatDiv.id = data['id'];

    let chatImg = document.createElement('div');

    chatImg.classList.add('chat-img');

    let chatLabel = document.createElement('h2');

    chatLabel.classList.add('chat-name');
    chatLabel.innerHTML = data['name'];

    chatDiv.appendChild(chatImg);
    chatDiv.appendChild(chatLabel);

    allChats.appendChild(chatDiv);

    currentChatId = chatDiv.id;

    reloadChats();
};

sendMessageButton.addEventListener('click', () => {
    let csrftoken = getCSRFToken();

    let xhr = new XMLHttpRequest();

    xhr.open('POST', '/send_message', true);

    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = () => {
        if (xhr.status == 200) {
            const response = JSON.parse(xhr.responseText);

            showMessages(response);
        }

        else if (xhr.status == 404)
            window.location.reload();
    };

    const data = JSON.stringify({'chat_id': currentChatId, 'message': messageText.value});

    xhr.send(data);

    messageText.value = '';
});

let addChatButton = document.getElementById('addChatButton');
let usernameToAdd = document.getElementById('usernameToAdd');

addChatButton.addEventListener('click', () => {
    let csrftoken = getCSRFToken();

    let xhr = new XMLHttpRequest();

    xhr.open('POST', '/create_new_chat', true);

    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = () => {
        if (xhr.status == 200) {
            const response = JSON.parse(xhr.responseText);

            addChat(response);

            toggleStyles();
        }

        else if (xhr.status == 404)
            window.location.reload();
    };

    const data = JSON.stringify({'username': usernameToAdd.value});

    xhr.send(data);

    usernameToAdd.value = '';
});
