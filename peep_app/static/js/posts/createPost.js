const createPost = (data) => {

    const config = {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify(data)
    };

    fetch( `${APP_URL}/api/posts/new`, config)
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
            getAllPosts();
        })
}