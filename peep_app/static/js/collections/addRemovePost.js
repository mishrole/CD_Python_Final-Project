const addPostToCollection = (collectionId, postId) => {
    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/collections/${collectionId}/add/${postId}`, config)
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
        searchCollectionByNameAndLoggedUser("", postId);
    })
}

const removePostFromCollection = (collectionId, postId) => {
    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        }
    };

    fetch( `${APP_URL}/api/collections/${collectionId}/remove/${postId}`, config)
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
        searchCollectionByNameAndLoggedUser("", postId);
    })
}