// Validate new post form
const formNewPost = document.querySelector('#form-new-post');
formNewPost.addEventListener('submit', (event) => {
    event.preventDefault();

    const inputs = document.querySelectorAll('.requires-validation.validate-new-post');
    const isValid = Validate(Array.from(inputs));

    if (isValid) {
        const data = {
            'content': event.target.content.value,
        };

        createPost(data);
        Clear(Array.from(inputs));
        formNewPost.reset();
    }
});