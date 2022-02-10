const getAllPosts = () => {

    const config = {
        method: 'GET'
    }

    fetch(`${APP_URL}/api/posts/all`, config)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error(response.status);
            }
        })
        .then (jsonResponse => {
            console.log(jsonResponse);
            const container = document.querySelector('#posts-container');
            container.innerHTML = "";

            const posts = jsonResponse.data.posts;
            const currentUser = jsonResponse.currentUser;

            if (posts.length == 0) {
                container.innerHTML = `
                    <div class="mt-3 text-center">
                    <p>😢 No posts yet 😢</p>
                </div>`;
            }

            posts.forEach(post => {
                container.innerHTML += `
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
                                        <span class="text-primary fs-6 fw-normal">
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
                                    <button type="button" class="btn btn-default" onclick="unlikePost(${post.id}, ${currentUser}, 'all-posts-data')"><i class="bi bi-heart-fill"></i></button>
                                    <button class="btn btn-default" type="button" onclick="showLikesModal(${post.id})">${post.likes}</button>
                                    </span>
                                    `
                                :
                                    `
                                    <span>
                                    <button type="submit" class="btn btn-default" onclick="likePost(${post.id}, ${currentUser}, 'all-posts-data')"><i class="bi bi-heart"></i></button>
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
        })
        .catch(error => {
            console.error(error);
        })
}

(function() {
    getAllPosts();
})()