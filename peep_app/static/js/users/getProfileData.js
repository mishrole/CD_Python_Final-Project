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
            const profileContainer = document.querySelector('#profile-container');
            profileContainer.innerHTML = "";

            const user = jsonResponse.data.user;
            const currentUser = jsonResponse.currentUser;

            profileContainer.innerHTML = `
            <div class="d-flex justify-content-center flex-column py-4">
                <div class="row align-items-center justify-content-center">
                    <div class="col-2 align-self-start">
                        <img class="img-fluid rounded-circle" src="/static/img/chicken-profile.svg" alt="Chicken Profile image">
                    </div>
                    <div class="col-12">
                        <h1 class="text-center py-2">${user.firstname} ${user.lastname}</h1>
                    </div>
                    <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center fw-bold">
                            <p><span id="followers">${user.followers.length}</span> Followers</p>
                            <p><span id="following">${user.following.length}</span> Following</p>
                            <p>${user.posts.length} Posts</p>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center align-items-center" id="follow-unfollow-container">
                        ${ user.id !== currentUser ? 
                            `
                            ${ user.followed ?
                                 `<button type="button" onclick="unfollow(${user.id}, ${currentUser})" class="btn btn-outline-danger">Unfollow</button>` : 
                                 `<button type="button" onclick="follow(${user.id}, ${currentUser})" class="btn btn-outline-primary">Follow</button>`
                                }
                            `
                            : ``
                        }
                    </div>
                </div>
            </div>
            `

            const postsContainer = document.querySelector('#posts-container');
            postsContainer.innerHTML = "";
            
            if (user.posts.length == 0) {
                postsContainer.innerHTML = `
                    <div class="mt-3 text-center">
                    <p>😢 No posts yet 😢</p>
                </div>`;
            }

            user.posts.forEach(post => {
                postsContainer.innerHTML += `
                <div class="card mb-3 p-3">
                    <div class="d-flex flex-column">
                        <div class="p-2">
                            <div class="row align-items-center justify-content-center">
                                <div class="col-2 col-lg-1 align-self-start">
                                    <a href="/users/profile/${post.author.id}">
                                        <img class="img-fluid rounded-circle" src="/static/img/chicken-profile.svg" alt="Chicken Profile image">
                                    </a>
                                </div>
                                <div class="col-10 col-lg-11">
                                    <h5>
                                        <a class="text-black text-decoration-none" href="/users/profile/${post.author.id}">${post.author.firstname} ${post.author.lastname}</a> 
                                        <span class="text-primary fs-6">
                                            ${post.author.username != null ? '@'+post.author.username : ''}
                                            • ${post.time_ago}</span>
                                    </h5>
                                    <div class="post-content">${post.content}</div>
                                </div>
                            </div>
                            <div class="d-flex align-items-center justify-content-around mt-2">
                                ${ post.isLiked ? 
                                    `
                                    <span>
                                    <button type="button" class="btn btn-default" onclick="unlikePost(${post.id}, ${currentUser}, 'profile-data')"><i class="bi bi-heart-fill"></i></button>
                                    <button class="btn btn-default" type="button" onclick="showLikesModal(${post.id})">${post.likes}</button>
                                    </span>
                                    `
                                :
                                    `
                                    <span>
                                    <button type="submit" class="btn btn-default" onclick="likePost(${post.id}, ${currentUser}, 'profile-data')"><i class="bi bi-heart"></i></button>
                                    <button class="btn btn-default" type="button" onclick="showLikesModal(${post.id})">${post.likes}</button>
                                    </span>
                                    `
                                }
                                <button class="btn btn-default" type="button" onclick="showCommentsModal(${post.id})"><i class="bi bi-chat"></i></button>
                                <button class="btn btn-default" type="button" id="btnBookmarkModal" onclick="showBookmarkModal(${post.id})"><i class="bi bi-bookmark"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            });

        });
}

(function() {
    getProfileData();
})();