document.addEventListener('DOMContentLoaded', () => {
    
    // Create form for user input
    const addButton = document.querySelector('#add');
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
                input.setAttribute('id', 'username');
                input.setAttribute('name', 'username');
                input.setAttribute('placeholder', 'Username');
                input.setAttribute('type', 'text');
            } else if (i == 1) {
                input.setAttribute('id', 'domain');
                input.setAttribute('name', 'domain');
                input.setAttribute('placeholder', 'Domain');
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
    const deleteButtons = document.getElementsByName('delete');
    
    for (let i = 0, buttons = deleteButtons.length; i < buttons; i++) {

        const deleteButton = deleteButtons[i];
        deleteButton.addEventListener('click', () => {

            // Remenber password row
            const id = deleteButton.getAttribute('id');

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
});