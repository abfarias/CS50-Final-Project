document.addEventListener('DOMContentLoaded', () => {
    
    // Create table row for user input
    const addButton = document.querySelector('#add');
    addButton.addEventListener('click', () => {

        // Select currente table body
        const table = document.querySelector('tbody');

        // Get number of colums
        const row = table.querySelector('tr:first-child');
        const columns = row.children.length - 1; 
        
        // Add Row
        const newRow = document.createElement('tr');
        
        // Add form
        const form = document.createElement('form');

        // Set form attributes
        form.setAttribute('action', '/');
        form.setAttribute('method', 'post');

        // Append form to new row
        newRow.appendChild(form);

        // Add input field cells
        for (let i = 0, n = columns - 2; i < n; i++) {
            const cell = document.createElement('td');
            const input = document.createElement('input')

            // Set generic attributes
            input.setAttribute('autocomplete', 'off');
            input.setAttribute('autofocus', 'true');
            input.setAttribute('class', 'form-control mx auto w-auto')
            cell.setAttribute('class', 'text-start')

            // Set specific attributes
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

            // Append input cells to new row
            cell.appendChild(input);
            newRow.appendChild(cell);

        }

        // Add confirm button cell
        const confirmButtonCell = document.createElement('td');
        const confirmButton = document.createElement('button');

        // Set confirm button attributes
        confirmButton.setAttribute('class', 'btn btn-primary btn-sm');
        confirmButton.setAttribute('type', 'submit');
        confirmButton.textContent = 'Confirm';

        // Append confirm button cell to new Row
        confirmButtonCell.appendChild(confirmButton);
        newRow.appendChild(confirmButtonCell);

        // Add cancel button cell
        const cancelButtonCell = document.createElement('td');
        const cancelButton = document.createElement('button');

        // Set cancel button attributes
        cancelButton.setAttribute('class', 'btn btn-primary btn-sm');
        cancelButton.setAttribute('type', 'button');
        cancelButton.textContent = 'Cancel';

        // Append cancel button cell to new row
        cancelButtonCell.appendChild(cancelButton);
        newRow.appendChild(cancelButtonCell);

        // Append new row to table
        table.appendChild(newRow);
        
    });

});