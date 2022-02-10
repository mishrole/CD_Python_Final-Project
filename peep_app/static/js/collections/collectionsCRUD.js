const inputCollectionSearch = document.querySelector('#collectionSearchInput');
const createCollectionModalBtn = document.querySelector('#collectionCreateButton');
// Collection Form
const newCollectionForm = document.querySelector('#newCollectionForm');

createCollectionModalBtn.addEventListener('click', () => {
    // Populates form name with search value
    const collectionNameForm = document.querySelector('#floatCollectionName');
    collectionNameForm.value = inputCollectionSearch.value;
    showCollectionsModal();
})

inputCollectionSearch.addEventListener('keyup', (e) => {
    searchCollectionByNameAndOwner(inputCollectionSearch.value);
});

// Validate new Collection form and request
newCollectionForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const inputs = document.querySelectorAll('.requires-validation.validate-new-collection');
    const isValid = Validate(Array.from(inputs));

    if (isValid) {
        const data = {
            'name': event.target.name.value,
            'description': event.target.description.value,
        };

        createCollection(data);
        Clear(Array.from(inputs));
        hideCollectionsModal();
    }
});

// Collection Modal
const collectionsModal = document.querySelector('#collectionsModal');
const collectionsModalBoostrap = new bootstrap.Modal(collectionsModal, {
    keyboard: false
});

collectionsModal.addEventListener('hidden.bs.modal', (event) => {
    newCollectionForm.reset();
});

function showCollectionsModal() {
    collectionsModalBoostrap.show();
}

function hideCollectionsModal() {
    collectionsModalBoostrap.hide();
}

(function() {
    searchCollectionByNameAndOwner("");
})();
