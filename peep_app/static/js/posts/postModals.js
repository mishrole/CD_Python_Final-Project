// Collections

const btnBookmarkModal = document.querySelectorAll('.btnBookmarkModal');

const bookmarkModal = new bootstrap.Modal(document.querySelector('#bookmarkModal'), {
    keyboard: false
});

function showBookmarkModal(id) {
    bookmarkModal.show();
    // alert(id);
}

// const createCollectionBtn = document.querySelector('#collectionCreateButton');
const inputSearch = document.querySelector('#collectionSearchInput');

inputSearch.addEventListener('keyup', (e) => {
    // console.log(inputSearch.value);
    searchCollectionByNameAndOwner(inputSearch.value);
});


// Comments

const btnCommentsModal = document.querySelectorAll('.btnCommentsModal');
const commentsContainer = document.querySelector('#commentsModal');

const commentsModal = new bootstrap.Modal(commentsContainer, {
    keyboard: false
});

function showCommentsModal(id) {
    commentsModal.show();
    alert(id);
}


// Likes

const btnLikesModal = document.querySelectorAll('.btnLikesModal');
const likesContainer = document.querySelector('#likesContainer');
const likesModal = document.querySelector('#likesModal');

const likesModalBootstrap = new bootstrap.Modal(likesModal, {
    keyboard: false
});

likesModal.addEventListener('hidden.bs.modal', (event) => {
    likesContainer.innerHTML = "";
})

const showLikesModal = (postId) => {
    getLikesFromPost(postId);
    likesModalBootstrap.show();
}

const getLikesFromPost = (postId) => {
    const config = {
        method: 'GET'
    }

    fetch(`${APP_URL}/api/posts/usersWhoLike/${postId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);

            if (jsonResponse.length == 0) {
                likesContainer.innerHTML = `
                <div class="d-flex flex-column">
                    <div class="p-2">
                        <div class="row align-items-center justify-content-center">
                            <div class="col-12 text-center">
                                <p class="fw-bold">😢 No likes yet 😢</p>
                            </div>
                        </div>
                    </div>
                </div>
                `
            }
            
            jsonResponse.forEach(user => {
                likesContainer.innerHTML += `
                    <div class="d-flex flex-column">
                        <div class="p-2">
                            <div class="row align-items-center justify-content-center">
                                <div class="col-2 col-lg-1 align-self-start">
                                    <img class="img-fluid rounded-circle" src="/static/img/chicken-profile.svg" alt="Chicken Profile image">
                                </div>
                                <div class="col-10 col-lg-11">
                                    <div class="d-flex align-items-center justify-content-between">
                                        <p class="fw-bold">${user.firstname} ${user.lastname}</p>
                                        <a href="/users/profile/${user.id}" class="btn btn-primary">View Profile</a>
                                    </div>
                                </div>
                        </div>
                    </div>
                </div>`
            });
        });
}
