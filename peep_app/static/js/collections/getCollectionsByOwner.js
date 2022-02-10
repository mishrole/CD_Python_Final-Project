const ownerId = getItemByReferenceAndReversePosition(path = window.location.pathname, reference = '', position = 1);

const getCollectionsByOwner = (ownerId) => {

    const config = {
        method: 'GET'
    }

    fetch( `${APP_URL}/api/collections/${ownerId}`, config)    
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
        
    })
}

(function() {
    getCollectionsByOwner(ownerId);
})();