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
        method: 'GET',
    }).then(response => response.json()
    ).then((results) => {
        if (results.user['gender'] === null) {
                document.querySelector('#complete-user-info').style.display = 'block';
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
        const body = create_match_view(results);
        const matchView = document.querySelector('#match-view');
        matchView.appendChild(body);
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
    matchButton.innerHTML = "See details";
    //
    // const postText = document.createElement('p');
    // postText.setAttribute('key', card.post['id']);
    // postText.className = `card-subtitle mb-2 text-muted ${card.post['id']}`;
    // postText.innerHTML = card.post.text;

    matchBody.appendChild(matchTitle);
    matchBody.appendChild(matchSubTitle);
    matchBody.appendChild(matchButton);
    matchCard.appendChild(matchBody);

    console.log(match);
    matchButton.addEventListener('click', () => load_match(match['id']))

    return matchBody
}

function create_match_view(match) {
    const body = document.createElement('div');

    const preTitle = document.createElement('h4');
    preTitle.innerHTML = 'Game Set Match!';
    const title = document.createElement('h3');
    title.innerHTML = `${match['users'][0]['level']} Match ${match['match']['match'].join(' & ')}`;

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
    body.appendChild(title);
    body.appendChild(imageContainer);
    return body
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