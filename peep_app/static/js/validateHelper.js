'use strict';

const Validate = (inputs) => {
    let invalidCounter = 0;

    inputs.forEach(element => {
        // Validate checkbox
        if (element.type === 'checkbox') {
            if (!element.checked) {
                ShowInvalidFeedback(element);
            } else {
                ShowValidFeedback(element);   
            }
        } else {
            // Validate controls : min length === 1
            if (element.value.length === 0) {
                ShowInvalidFeedback(element);
            } else {
                ShowValidFeedback(element);
            }
        }

        if(element.classList.contains('is-invalid')) {
            invalidCounter++;
        }
    });

    if(invalidCounter > 0) {
        return false;
    }

    return true;
}

const ShowInvalidFeedback = (element) => {
    // Remove previous valid feedback
    element.classList.remove('is-valid');
    element.nextElementSibling.classList.remove('valid-feedback');
    // Change message
    element.nextElementSibling.innerHTML = 'This field is required';
    // Add new invalid feedback
    element.classList.add('is-invalid');
    element.nextElementSibling.classList.add('invalid-feedback');
    // Show message
    element.nextElementSibling.classList.add('show');
}

const ShowValidFeedback = (element) => {
    // Remove previous invalid feedback
    element.classList.remove('is-invalid');
    element.nextElementSibling.classList.remove('invalid-feedback');
    // Change message
    element.nextElementSibling.innerHTML = 'Looks good!';
    // Add new valid feedback
    element.classList.add('is-valid');
    element.nextElementSibling.classList.add('valid-feedback');
    // Show message
    element.nextElementSibling.classList.add('show');
}

// With fetch we don't need to reload
const Clear = (inputs) => {
    inputs.forEach(element => {
        HideAllFeedback(element);
    }
)};

const HideAllFeedback = (element) => {
    element.classList.remove('is-invalid');
    element.classList.remove('is-valid');
    element.nextElementSibling.classList.add('invalid-feedback');
    element.nextElementSibling.classList.remove('valid-feedback');
    element.nextElementSibling.classList.remove('show');
}