const addPostToCollection = (collectionId, postId, fn) => {
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
        fn.fn();
        searchCollectionByNameAndLoggedUser("", postId);
    })
}

const removePostFromCollection = (collectionId, postId, fn) => {
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
        fn.fn();
        searchCollectionByNameAndLoggedUser("", postId);
    })
}