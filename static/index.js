document.addEventListener('DOMContentLoaded', () => {
    
    // Create form for user input
    const addButton = document.getElementById('add');
    addButton.addEventListener('click', () => {

        const form = document.createElement('form');

        form.setAttribute('action', '/');
        form.setAttribute('method', 'post');

        // Add form inputs
        for (let i = 0; i < 3; i++) {

            const div = document.createElement('div');
            const input = document.createElement('input');

            div.setAttribute('class', 'mb-3');
            input.setAttribute('autocomplete', 'off');
            input.setAttribute('autofocus', 'true');
            input.setAttribute('class', 'form-control mx auto w-auto');

            if (i == 0) {
                input.setAttribute('id', 'domain');
                input.setAttribute('name', 'domain');
                input.setAttribute('placeholder', 'Domain');
                input.setAttribute('type', 'text');
            } else if (i == 1) {
                input.setAttribute('id', 'username');
                input.setAttribute('name', 'username');
                input.setAttribute('placeholder', 'Username');
                input.setAttribute('type', 'text');
            } else {
                input.setAttribute('id', 'password');
                input.setAttribute('name', 'password');
                input.setAttribute('placeholder', 'Password');
                input.setAttribute('type', 'password');
            }

            // Append inputs to form
            div.appendChild(input);
            form.appendChild(div);
        }
        
        // Add confirm button
        const confirmButton = document.createElement('button');

        // Set confirm button attributes
        confirmButton.setAttribute('class', 'btn btn-primary btn-sm');
        confirmButton.setAttribute('type', 'submit');
        confirmButton.textContent = 'Confirm';

        // Append confirm button to form
        form.appendChild(confirmButton);

        // Add cancel button
        const cancelButton = document.createElement('button');

        // Set cancel button attributes
        cancelButton.setAttribute('class', 'btn btn-primary btn-sm');
        cancelButton.setAttribute('type', 'button');
        cancelButton.textContent = 'Cancel';
        
        // Append form to main
        const main = document.querySelector('main');
        main.appendChild(form);
    });


    // Create confirmation interface for deleting a password
    const rows = document.getElementsByName('tbody-row')
    const deleteButtons = document.getElementsByName('delete');
    
    for (let i = 0, length = deleteButtons.length; i < length; i++) {

        const row = rows[i]
        const deleteButton = deleteButtons[i];
        deleteButton.addEventListener('click', () => {

            // Remenber password row
            const id = row.getAttribute('id');

            // Send a DELETE http request if user's confirmation is true
            if (confirm('Are you sure you want to delete this password?')) {
                fetch('/', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ id: id })
                })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        console.log('Error: ' + response.statusText);
                    }
                })
                .catch(error => {
                    console.log('Error: ' + error);
                });
            }
        });
    }


    // Create password visibility toggler functionality
    const visibilityButtons = document.getElementsByName('visibility')
    const passwords = document.getElementsByName('password-field')
    const eyeIcons = document.getElementsByName('eye')

    for (let i = 0, length = visibilityButtons.length; i < length; i++) {
        
        const eyeIcon = eyeIcons[i]
        const password = passwords[i]
        const visibilityButton = visibilityButtons[i]
        visibilityButton.addEventListener('click', () => {
            
            const passwordType = password.getAttribute('type')

            if (passwordType == 'password') {
                password.setAttribute('type', 'text')
                visibilityButton.setAttribute('title', 'Hide')
                eyeIcon.setAttribute('src', '../static/images/eye-slash.svg')
                eyeIcon.setAttribute('alt', 'Hide')
            } else {
                password.setAttribute('type', 'password')
                visibilityButton.setAttribute('title', 'Show')
                eyeIcon.setAttribute('src', '../static/images/eye.svg')
                eyeIcon.setAttribute('alt', 'Show')
            }
        });
    }


    // Create 'copy to clipboard' functionality
    // Adapted from https://www.youtube.com/watch?v=9-vBx7F0lns
    const copyButtons = document.getElementsByName('copy-button')
    const clipboards = document.getElementsByName('clipboard')

    for (let i = 0, length = copyButtons.length; i < length; i++) {

        const copyButton = copyButtons[i]
        const password = passwords[i]
        const clipboard = clipboards[i]

        copyButton.addEventListener('click', () => {
            
            const value = password.getAttribute('value')
            
            // Workaround to allow copying "type: password" input fields
            const hiddenText = document.createElement('input')
            hiddenText.setAttribute('value', `${value}`)

            document.body.appendChild(hiddenText)

            hiddenText.select()
            document.execCommand('copy') // Deprecated, but it'll do for now...
            
            document.body.removeChild(hiddenText)
            
            clipboard.setAttribute('src', '../static/images/clipboard-check.svg')
            window.getSelection().removeAllRanges()
            setTimeout(() => {
                clipboard.setAttribute('src', '../static/images/clipboard.svg')
            }, 1500);
        });
    }
});