const editProfile = (data) => {

    const userId = getItemByReferenceAndReversePosition(path = window.location.pathname, reference = '', position = 1);

    const config = {
        method : 'PUT',
        headers : {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify(data)
    };

    fetch( `${APP_URL}/api/users/${userId}/edit`, config)
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
            // getAllPosts();
            // window.history.back();
            window.location.href = `/users/profile/${userId}`;
        })
}