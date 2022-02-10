const searchCollectionByNameAndLoggedUser = (name, currentPostId) => {
    const config = {
        method: 'GET'
    }

    fetch( `${APP_URL}/api/collections/search?name=${name}`, config)    
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            throw new Error(response.status);
        }
    })
    .then (jsonResponse => {
        console.log(jsonResponse);
        const collections = jsonResponse.data.collections;
        const createCollectionBtn = document.querySelector('#collectionCreateButton');
        const collectionsContainer = document.querySelector('#collectionsContainer');

        if (collections.length === 0) {
            createCollectionBtn.classList.remove('d-none');
        } else {
            createCollectionBtn.classList.add('d-none');
        }

        collectionsContainer.innerHTML = ""

        collections.forEach(collection => {
            collectionsContainer.innerHTML +=`
            <div class="row justify-content-center align-items-center pt-4">
                <div class="col-1">
                    <i class="bi bi-journal"></i> 
                </div>
                <div class="col-8">
                    <p class="m-0">${collection.name}</p>
                </div>
                <div class="col-3 d-flex justify-content-end">
                    ${ typeof collection.posts.find(post => post.id == currentPostId) === 'undefined' ?
                    `<button class="btn btn-secondary" onclick="addCurrentPostToCollection(${collection.id})"><i class="bi bi-plus"></i></button>` 
                    : 
                    `<button class="btn btn-danger" onclick="removeCurrentPostFromCollection(${collection.id})"><i class="bi bi-x"></i></button>`
                    }
                    
                </div>
            </div>
            `
        })
    })
    .catch(error => {
        console.log(error);
    })
    .finally(() => {
    })

}
  