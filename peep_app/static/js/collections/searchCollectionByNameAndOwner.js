const searchCollectionByNameAndOwner = (name, limit) => {

    const ownerId = getItemByReferenceAndReversePosition(path = window.location.pathname, reference = '', position = 1);

    const config = {
        method: 'GET'
    }

    fetch( `${APP_URL}/api/collections/${ownerId}/search?name=${name}&limit=${limit}`, config)    
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
        const collectionsContainer = document.querySelector('#collectionsContainer');

        collectionsContainer.innerHTML = ""

        if (collections.length === 0) {
            collectionsContainer.innerHTML = '<div class="d-flex justify-content-center align-items-center"><p>😢 No collections yet. 😢</p></div>'
        }

        collections.forEach(collection => {
            collectionsContainer.innerHTML +=`
            <div class="row justify-content-center align-items-center pt-4">
                <div class="col-1">
                    <i class="bi bi-journal"></i> 
                </div>
                <div class="col-8">
                    <p class="m-0 fw-bold">${collection.name}</p>
                </div>
                <div class="col-3 d-flex justify-content-end gap-3">
                    <button class="btn btn-outline-secondary"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-outline-danger"><i class="bi bi-trash"></i></button>
                </div>
            </div>
            `
        });

    })
    .catch(error => {
        console.log(error);
    })
    .finally(() => {
    })

}