const searchCollectionByNameAndOwner = (name) => {
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
                    <button class="btn btn-primary">Add</button>
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
  