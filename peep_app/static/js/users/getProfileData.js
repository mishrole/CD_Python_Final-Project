const getProfileData = () => {
    const profileId = getLastItem(window.location.pathname);

    const config = {
        method: 'GET'
    }

    fetch(`${APP_URL}/api/users/profile/${profileId}`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);

            const user = jsonResponse.data.user;
            const currentUser = jsonResponse.currentUser;

            const profileContainer = document.querySelector('#profile-container');
            profileContainer.innerHTML = "";

            // Generate Profile Header
            profileContainer.appendChild(createProfileHeader(user, currentUser));

            const postsContainer = document.querySelector('#posts-container');
            postsContainer.innerHTML = "";

            // Generate Profile Posts
            postsContainer.appendChild(createProfilePosts(user.posts, currentUser));

        });
}

(function() {
    getProfileData();
})();

const createProfileHeader = (user, currentUser) => {

    const flexContainer = document.createElement('div');
    flexContainer.classList.add('d-flex', 'justify-content-center', 'flex-column', 'py-4');


    // Row
    const rowContainer = document.createElement('div');
    rowContainer.classList.add('row', 'align-items-center', 'justify-content-center');
    

    // Profile Image
    const colImageContainer = document.createElement('div');
    colImageContainer.classList.add('col-2','align-self-start');
    const profileImage = document.createElement('img');
    profileImage.classList.add('img-fluid', 'rounded-circle');
    profileImage.src = '/static/img/chicken-profile.svg';
    profileImage.alt = 'Chicken Profile Image';
    
    
    // Profile Name
    const colNameContainer = document.createElement('div');
    colNameContainer.classList.add('col-12');
    const name = document.createElement('h1');
    name.classList.add('text-center','py-2');
    name.textContent = `${user.firstname} ${user.lastname}`;
    
    
    // Profile Counter
    const colCounterContainer = document.createElement('div');
    colCounterContainer.classList.add('col-12');
    const flexCounterContainer = document.createElement('div');
    flexCounterContainer.classList.add('d-flex', 'justify-content-between', 'align-items-center', 'fw-bold');
    
    const pFollowers = document.createElement('p');
    const spanFollowers = document.createElement('span');
    spanFollowers.id = 'followers';
    spanFollowers.textContent = `${user.followers.length}`;
    pFollowers.append(spanFollowers);
    pFollowers.innerHTML += ' Followers';
    
    const pFollowing = document.createElement('p');
    const spanFollowing = document.createElement('span');
    spanFollowing.id = 'Following';
    spanFollowing.textContent = `${user.following.length}`;
    pFollowing.append(spanFollowing);
    pFollowing.innerHTML += ' Following';

    const pPosts = document.createElement('p');
    pPosts.textContent = `${user.posts.length} Posts`;
    
    
    // Follow and unfollow 
    const flexFollowUnfollowContainer = document.createElement('div');
    flexFollowUnfollowContainer.classList.add('d-flex', 'justify-content-center', 'align-items-center');
    flexFollowUnfollowContainer.id = 'follow-unfollow-container';

    if ( user.id !== currentUser ) {
        if ( user.followed ) {
            const buttonUnfollow = document.createElement('button');
            buttonUnfollow.type = 'button';
            buttonUnfollow.classList.add('btn', 'btn-outline-danger');
            buttonUnfollow.textContent = 'Unfollow';
            buttonUnfollow.onclick = () => unfollow(user.id, currentUser, 'profile-data');
            flexFollowUnfollowContainer.append(buttonUnfollow);
        } else {
            const buttonFollow = document.createElement('button');
            buttonFollow.type = 'button';
            buttonFollow.classList.add('btn', 'btn-outline-primary');
            buttonFollow.textContent = 'Follow';
            buttonFollow.onclick = () => follow(user.id, currentUser, 'profile-data');
            flexFollowUnfollowContainer.append(buttonFollow);
        }
    }
    
    colImageContainer.appendChild(profileImage);
    colNameContainer.appendChild(name);
    flexCounterContainer.append(pFollowers, pFollowing, pPosts);
    colCounterContainer.appendChild(flexCounterContainer);
    rowContainer.append(colImageContainer, colNameContainer, colCounterContainer, flexFollowUnfollowContainer);
    flexContainer.appendChild(rowContainer);

    return flexContainer;

}

const createProfilePosts = (posts, currentUser) => {
    const mainContainer = document.createElement('div');
    mainContainer.classList.add('container', 'py-4', 'border-top');

    if ( posts.length == 0 ) {
        const divNoPosts = document.createElement('div');
        divNoPosts.classList.add('mt-3', 'text-center');
        const pNoPosts = document.createElement('p');
        pNoPosts.textContent = '😢  No posts yet 😢';

        divNoPosts.appendChild(pNoPosts);
        mainContainer.append(divNoPosts)

        return mainContainer;
    }

    posts.forEach(post => {
        const card = document.createElement('div');
        card.classList.add('card', 'mb-3', 'p-3');
        const flexContainer = document.createElement('div');
        flexContainer.classList.add('d-flex', 'flex-column');
        const topContainer = document.createElement('div');
        topContainer.classList.add('p-2');
        const flexRowContainer = document.createElement('div');
        flexRowContainer.classList.add('row', 'align-items-center', 'justify-content-center');


        // Profile Image
        const flexColImageContainer = document.createElement('div')
        flexColImageContainer.classList.add('col-2', 'col-lg-1', 'align-self-start');

        const anchorAuthorProfile = document.createElement('a');
        anchorAuthorProfile.href = `/users/profile/${post.author.id}`;

        const imageProfile = document.createElement('img');
        imageProfile.src = '/static/img/chicken-profile.svg';
        imageProfile.alt = 'Chicken Profile image';
        imageProfile.classList.add('img-fluid', 'rounded-circle');


        // Name
        const flexColNameContainer = document.createElement('div');
        flexColNameContainer.classList.add('col-10', 'col-lg-11');
        const nameContainer = document.createElement('h5');
        
        const anchorAuthorNameProfile = document.createElement('a');
        anchorAuthorNameProfile.href = `/users/profile/${post.author.id}`;
        anchorAuthorNameProfile.classList.add('text-black', 'text-decoration-none');
        anchorAuthorNameProfile.textContent = `${post.author.firstname} ${post.author.lastname}`;

        const spanNameProfile = document.createElement('span');
        spanNameProfile.classList.add('text-primary', 'fs-6', 'fw-normal');

        if ( post.author.username != null ) {
            spanNameProfile.textContent = `@${post.author.username}`;
        }

        const postContent = document.createElement('div');
        postContent.classList.add('post-content');
        postContent.textContent = `${post.content}`;


        // Modals
        const buttonLikesModal = document.createElement('button');
        buttonLikesModal.classList.add('btn', 'btn-default');
        buttonLikesModal.type = 'button';
        buttonLikesModal.onclick = () => showLikesModal(post.id);
        buttonLikesModal.textContent = `${post.likes}`;

        const buttonCommentsModal = document.createElement('button');
        buttonCommentsModal.classList.add('btn', 'btn-default');
        buttonCommentsModal.type = 'button';
        buttonCommentsModal.onclick = () => showCommentsModal(post.id);
        buttonCommentsModal.innerHTML = `<i class="bi bi-chat"></i>`;

        const buttonBookmarkModal = document.createElement('button');
        buttonBookmarkModal.classList.add('btn', 'btn-default');
        buttonBookmarkModal.type = 'button';
        buttonBookmarkModal.onclick = () => showBookmarkModal(post.id);
        buttonBookmarkModal.innerHTML = `<i class="bi bi-bookmark"></i>`;

        // Likes
        const flexLikesContainer = document.createElement('div');
        flexLikesContainer.classList.add('d-flex', 'align-items-center', 'justify-content-around', 'mt-2');

        const buttonLike = document.createElement('button');
        buttonLike.classList.add('btn', 'btn-default');
        buttonLike.type = 'button';
        buttonLike.onclick = () => likePost(post.id, currentUser, 'profile-data');
        buttonLike.innerHTML = '<i class="bi bi-heart"></i>';
        
        const buttonUnlike = document.createElement('button');
        buttonUnlike.classList.add('btn', 'btn-default');
        buttonUnlike.type = 'button';
        buttonUnlike.onclick = () => unlikePost(post.id, currentUser, 'profile-data');
        buttonUnlike.innerHTML = '<i class="bi bi-heart-fill"></i>';

        const spanLikesContainer = document.createElement('span');

        if ( post.isLiked ) {
            spanLikesContainer.append(buttonUnlike, buttonLikesModal);
        } else {
            spanLikesContainer.append(buttonLike, buttonLikesModal);
        }


        nameContainer.append(anchorAuthorNameProfile, spanNameProfile);
        flexColNameContainer.append(nameContainer, postContent);

        anchorAuthorProfile.append(imageProfile);
        flexColImageContainer.append(anchorAuthorProfile);
        flexRowContainer.append(flexColImageContainer, flexColNameContainer);

        flexLikesContainer.append(spanLikesContainer, buttonCommentsModal, buttonBookmarkModal);

        topContainer.append(flexRowContainer, flexLikesContainer);
        flexContainer.appendChild(topContainer);
        card.appendChild(flexContainer);

        mainContainer.append(card);

    });

    return mainContainer;
}
