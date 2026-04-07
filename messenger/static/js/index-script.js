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
