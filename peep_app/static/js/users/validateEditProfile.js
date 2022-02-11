(function() {
    const birthday = document.querySelector('#floatingBirthday');
    const today = new Date().toISOString().split('T')[0];
    birthday.setAttribute('max', today);
})();

// const radios = document.querySelectorAll('.radio-gender');
// const otherInput = document.querySelector('#other');

// radios.forEach((radio) => {
//     radio.addEventListener('click', (e) => {
//         console.log(e);
//         if (e.target.value === 'Self describe') {
//             otherInput.classList.remove('d-none');
//             otherInput.focus();
//         } else {
//             otherInput.classList.add('d-none');
//         }
//     });
// });

const formEditProfile = document.querySelector('#form-edit-profile');
formEditProfile.addEventListener('submit', (event) => {
    event.preventDefault();
    const inputs = document.querySelectorAll('.requires-validation.validate-edit-profile');
    const isValid = Validate(Array.from(inputs));

    // const password = event.target.password.value;
    // const confirmation = event.target.password_confirmation.value;

    if (isValid) {
        const data = {
            'firstname': event.target.firstname.value,
            'lastname': event.target.lastname.value,
            'birthday': event.target.birthday.value,
            'country': event.target.country.value,
        }

        editProfile(data);
        Clear(Array.from(inputs));
    }
});