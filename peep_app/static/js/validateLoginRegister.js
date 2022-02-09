// Validate all date controls : Max date === todays date
(function() {
    const dateControl = document.querySelectorAll('.date-control');
    const today = new Date().toISOString().split('T')[0];

    dateControl.forEach((control) => {
        control.setAttribute('max', today);
    });
})();

// Validate register form
const formRegister = document.querySelector('#form-register');
formRegister.addEventListener('submit', (event) => {
    const inputs = document.querySelectorAll('.requires-validation.validate-register');

    const isValid = Validate(Array.from(inputs));

    if (isValid) {
        return true;
    } else {
        event.preventDefault();
    }
});

// Validate login form
const formLogin = document.querySelector('#form-login');
formLogin.addEventListener('submit', (event) => {
    const inputs = document.querySelectorAll('.requires-validation.validate-login');

    const isValid = Validate(Array.from(inputs));

    if (isValid) {
        return true;
    } else {
        event.preventDefault();
    }
});