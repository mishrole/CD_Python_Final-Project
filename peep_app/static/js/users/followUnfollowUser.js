const container = document.querySelector('#follow-unfollow-container');

function follow(followedId, followerId, fn)  {

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
            if (fn === 'profile-data') {
                getProfileData();
            }
        })
        .catch(error => {
            console.log(error);
        })

}

function unfollow(followedId, followerId, fn) {

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
            if (fn === 'profile-data') {
                getProfileData();
            }
        })
        .catch(error => {
            console.log(error);
        })

}