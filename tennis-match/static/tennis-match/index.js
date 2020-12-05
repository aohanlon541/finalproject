document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#complete-user-info').style.display = 'none';
    document.querySelector('#match-view').style.display = 'none';

    document.querySelector('#new-matches-nav-link').addEventListener('click', () => load_new())
    document.querySelector('#existing-matches-nav-link').addEventListener('click', () => load_existing())

  // By default, load the inbox
  load_matches();
});

function load_matches() {
    fetch('/matches', {
        method: 'POST',
    }).then(response => response.json()
    ).then((results) => {
        if (results.user['gender'] === null) {
                document.querySelector('#complete-user-info').style.display = 'block';
                document.querySelector('#new-matches-div').style.display = 'none';
                document.querySelector('#existing-matches-div').style.display = 'none';
                document.querySelector("#update-user-submit").addEventListener('click', () => update_user())
        }
        let newMatchesDiv = document.querySelector('#new-matches');
        newMatchesDiv.innerHTML = '';
        results['new_matches'].forEach(match => {
            const matchElement = create_match_card(match);
            newMatchesDiv.appendChild(matchElement);
        });
        let existingMatchesDiv = document.querySelector('#existing-matches');
        existingMatchesDiv.innerHTML = '';
        results['existing_matches'].forEach(match => {
            const matchElement = create_match_card(match);
            existingMatchesDiv.appendChild(matchElement);
        });
   });
}

function load_new() {
    document.querySelector('#complete-user-info').style.display = 'none';
    document.querySelector('#new-matches-div').style.display = 'block';
    document.querySelector('#existing-matches-div').style.display = 'none';
    document.querySelector('#match-view').style.display = 'none';

    fetch('/new-matches', {
        method: 'GET',
    }).then(response => response.json()
    ).then((results) => {
        let newMatchesDiv = document.querySelector('#new-matches');
        newMatchesDiv.innerHTML = '';
        results['new_matches'].forEach(match => {
            const matchElement = create_match_card(match);
            newMatchesDiv.appendChild(matchElement);
        });
    });
}

function load_existing() {
    document.querySelector('#complete-user-info').style.display = 'none';
    document.querySelector('#new-matches-div').style.display = 'none';
    document.querySelector('#existing-matches-div').style.display = 'block';
    document.querySelector('#match-view').style.display = 'none';

    fetch('/existing-matches', {
        method: 'GET',
    }).then(response => response.json()
    ).then((results) => {
        let newMatchesDiv = document.querySelector('#new-matches');
        newMatchesDiv.innerHTML = '';
        results['existing_matches'].forEach(match => {
            const matchElement = create_match_card(match);
            newMatchesDiv.appendChild(matchElement);
        });
    });
}

function load_match(id) {
    event.preventDefault();
    document.querySelector('#complete-user-info').style.display = 'none';
    document.querySelector('#new-matches-div').style.display = 'none';
    document.querySelector('#existing-matches-div').style.display = 'none';
    document.querySelector('#match-view').style.display = 'block';

    fetch(`/match/${id}`, {
        method: 'PUT'
    }).then(response => response.json()
    ).then((results) => {
        const matchView = document.querySelector('#match-view');
        matchView.innerHTML = '';
        const body = create_match_view(results);
        const messages = create_messages_view(results);
        matchView.appendChild(body);
        matchView.appendChild(document.createElement('hr'));
        matchView.appendChild(messages);
    });
}

function update_user() {
    event.preventDefault();
    const body = map_edit_user();
    fetch('/edit-user', {
        method: 'POST',
        body: body
    }).then(() => {
        document.querySelector('#complete-user-info').style.display = 'none';
        load_matches();
    });
}

function add_message(matchId, currentUser) {
    event.preventDefault();
    fetch(`message/${matchId}`, {
        method: 'POST',
        body: JSON.stringify({
            text: document.querySelector('#message-textarea').value
        })
    }).then(response => response.json()
    ).then((results) => {
        const newMessage = append_message(results['new_message'], currentUser);
        document.querySelector('#message-container').appendChild(newMessage);
        document.querySelector('#message-textarea').value = '';
    });
}

function post_edit_message(matchId, messageId) {
    event.preventDefault();
    fetch(`message/${matchId}`, {
        method: 'POST',
        body: JSON.stringify({
            id: messageId,
            text: document.querySelector('#message-textarea-edit').value
        })
    }).then(response => response.json()
    ).then((results) => {
        const updatedMessage = results['updated_message'];
        console.log(updatedMessage);
        const messageText = document.getElementById(`${updatedMessage['id']}-message-text`);
        messageText.innerHTML = updatedMessage['text'];
        messageText.replaceWith(messageText);
    });
}

function edit_message(matchId, messageId) {
    const messageText = document.getElementById(`${messageId}-message-text`);
    const text = messageText.innerText;
    const editForm = document.createElement('form');
    editForm.className = 'message-form';
    editForm.setAttribute('id', `${messageId}-message-text`);
    const formGroupDiv = document.createElement('div');
    formGroupDiv.className = 'form-group';
    const textarea = document.createElement('textarea');
    textarea.setAttribute('id', 'message-textarea-edit');
    textarea.innerText = text;
    formGroupDiv.appendChild(textarea);
    const submitButton = document.createElement('input');
    submitButton.setAttribute('type', 'submit');
    submitButton.setAttribute('id', 'message-edit-submit');
    submitButton.className = 'btn btn-primary btn-sm';
    editForm.appendChild(formGroupDiv);
    editForm.appendChild(submitButton);
    messageText.replaceWith(editForm);

    submitButton.addEventListener('click', () => post_edit_message(matchId, messageId));
}

function create_match_card(match) {
    const matchCard = document.createElement('div');
    matchCard.setAttribute('key', match['id'])
    matchCard.className = "card post";

    const matchBody = document.createElement('div');
    matchBody.className = "card-body";

    const matchTitle = document.createElement('h5');
    matchTitle.className = "card-title";

    matchTitle.innerHTML = match['match'].join(' & ');

    const matchSubTitle = document.createElement('h6');
    matchSubTitle.className = `card-subtitle mb-2 text-muted author`;
    matchSubTitle.innerHTML = match['created_date'];

    const matchButton = document.createElement('button');
    matchButton.innerHTML = 'See details';
    matchButton.className = 'btn btn-primary';

    matchBody.appendChild(matchTitle);
    matchBody.appendChild(matchSubTitle);
    matchBody.appendChild(matchButton);
    matchCard.appendChild(matchBody);

    matchButton.addEventListener('click', () => load_match(match['id']))

    return matchBody
}

function create_match_view(match) {
    const body = document.createElement('div');

    const preTitle = document.createElement('h2');
    preTitle.innerHTML = 'Game Set Match!';
    preTitle.className = 'pretitle-profile';

    const title = document.createElement('h4');
    title.innerHTML = match['match']['match'].join(' & ');

    const subtitle = document.createElement('h3');
    subtitle.innerHTML = `${match['users'][0]['level']} ${find_game_type(match['match']['type'])} Match`;

    const imageContainer = document.createElement('div');
    imageContainer.className = 'image-container';
    match['users'].map(user => {
        let picture = document.createElement('img');
        picture.setAttribute('src', user['picture']);
        picture.setAttribute('alt', `${user['email']}'s profile picture`);
        picture.className = 'profile-picture';
        imageContainer.appendChild(picture);
    });

    body.appendChild(preTitle);
    body.appendChild(document.createElement('hr'))
    body.appendChild(title);
    body.appendChild(subtitle);
    body.appendChild(imageContainer);
    return body
}

function create_messages_view(match) {
    const messageContainer = document.createElement('div');
    messageContainer.setAttribute('id', 'message-container');
    const messages = match['messages'];

    const form = document.createElement('form');
    form.className = 'message-form';
    const formGroupDiv = document.createElement('div');
    formGroupDiv.className = 'form-group';
    const textarea = document.createElement('textarea');
    textarea.setAttribute('id', 'message-textarea');
    formGroupDiv.appendChild(textarea);
    const submitButton = document.createElement('input');
    submitButton.setAttribute('type', 'submit');
    submitButton.setAttribute('id', 'message-submit');
    submitButton.className = 'btn btn-primary btn-sm';
    form.appendChild(formGroupDiv);
    form.appendChild(submitButton);
    messageContainer.appendChild(form);

    submitButton.addEventListener('click', () =>
        add_message(match['match']['id']), match['current_user']['email']);

    let messageUl = document.createElement('ul');
    messages.map(message => {
        let messageLi = append_message(message, match['current_user']['email']);
        messageUl.className = 'list-group';
        messageUl.appendChild(messageLi);
        messageContainer.appendChild(messageUl);
    });

    return messageContainer;
}

function append_message(message, currentUser) {
    let messageLi = document.createElement('li');
    messageLi.className = 'list-group-item';

    let messageAuthor = document.createElement('p');
    messageAuthor.className = 'message-author';
    messageAuthor.innerHTML = message['created_by'];

    let messageText = document.createElement('p');
    messageText.innerHTML = message['text'];
    messageText.setAttribute('id',`${message['id']}-message-text`);

    let messageTimestamp = document.createElement('p');
    messageTimestamp.innerHTML = message['created_date'];
    messageTimestamp.className = 'message-created-date';

    messageLi.appendChild(messageAuthor);
    messageLi.appendChild(messageText);
    messageLi.appendChild(messageTimestamp);

    if (currentUser === message['created_by']) {
        let editButton = document.createElement('span');
        editButton.className = 'edit-icon-span'
        editButton.innerHTML = ('<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
            '  <path fill-rule="evenodd" d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>\n' +
            '</svg>');
        editButton.addEventListener('click', () => edit_message(message['match'], message['id']));
        messageLi.appendChild(editButton);
    }

    return messageLi;
}

function find_game_type(type) {
    switch(type) {
        case 'S':
            return 'Singles';
        case 'D':
            return 'Doubles';
    }
}

function map_edit_user() {
    return JSON.stringify({
        'level': document.querySelector('#level').value,
        'gender': document.querySelector('input[name=gender]:checked').value,
        'singles': document.querySelector('#singles').checked,
        'doubles': document.querySelector('#doubles').checked,
        'mixed_doubles': document.querySelector('#mixedDoubles').checked,
        'picture': document.querySelector('#picture').value,
    });
}