const container = document.querySelector('#follow-unfollow-container');

function follow(followedId, followerId)  {

    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/users/follow/${followedId}/by/${followerId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error(response.status);
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);
            const followers = document.querySelector('#followers');
            followers.innerHTML = parseInt(followers.textContent) + 1;
            container.innerHTML = `<button type="button" onclick="unfollow(${followedId}, ${followerId})" class="btn btn-outline-danger">Unfollow</button>`;
        })
        .catch(error => {
            console.log(error);
        })

}

function unfollow(followedId, followerId) {

    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/users/unfollow/${followedId}/by/${followerId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error(response.status);
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);
            const followers = document.querySelector('#followers');
            followers.innerHTML = parseInt(followers.textContent ) - 1;
            container.innerHTML = `<button type="button" onclick="follow(${followedId}, ${followerId})" class="btn btn-outline-primary">Follow</button>`
        })
        .catch(error => {
            console.log(error);
        })

}