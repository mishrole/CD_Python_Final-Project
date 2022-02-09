const likePost = (postId, userId, fn) => {

    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/posts/like/${postId}/by/${userId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error(response.status);
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);
        })
        .catch(error => {
            console.log(error);
        })
        .finally(() => {
            if (fn === 'all-posts-data') {
                getAllPosts();
            } else if (fn === 'profile-data') {
                getProfileData();
            }
        })

}

const unlikePost = (postId, userId, fn) => {

    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/posts/unlike/${postId}/by/${userId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error(response.status);
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);
        })
        .catch(error => {
            console.log(error);
        })
        .finally(() => {
            if (fn === 'all-posts-data') {
                getAllPosts();
            } else if (fn === 'profile-data') {
                getProfileData();
            }
        })

}