document.addEventListener('DOMContentLoaded', () => {

    // Create password visibility toggler for modal form
    const password = document.getElementById('password')
    const check = document.getElementById('flexCheckDefault')

    check.addEventListener('click', () => {

        const passwordType = password.getAttribute('type')

        if (passwordType == 'password') {
            password.setAttribute('type', 'text')
        } else {
            password.setAttribute('type', 'password')
        }
    })

    
    // Create confirmation interface for deleting a password
    const rows = document.getElementsByName('tbody-row')
    const deleteButtons = document.getElementsByName('delete')
    
    for (let i = 0, length = deleteButtons.length; i < length; i++) {

        const row = rows[i]
        const deleteButton = deleteButtons[i]
        deleteButton.addEventListener('click', () => {

            // Remenber password row
            const id = row.getAttribute('id')

            // Send a DELETE http request if user's confirmation is true
            // Adapted from: https://www.youtube.com/watch?v=cuEtnrL9-H0
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
                        window.location.reload()
                    } else {
                        console.log('Error: ' + response.statusText)
                    }
                })
                .catch(error => {
                    console.log('Error: ' + error)
                })
            }
        })
    }


    // Create password visibility toggler for items in the table
    const visibilityButtons = document.getElementsByName('visibility')
    const passwordFields = document.getElementsByName('password-field')
    const eyeIcons = document.getElementsByName('eye')

    for (let i = 0, length = visibilityButtons.length; i < length; i++) {
        
        const eyeIcon = eyeIcons[i]
        const password = passwordFields[i]
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
        })
    }


    // Create 'copy to clipboard' functionality
    // Adapted from https://www.youtube.com/watch?v=9-vBx7F0lns
    const usernameFields = document.getElementsByName('username-field')
    const copyButtonsUsername = document.getElementsByName('copy-button-username')
    const copyButtonsPassword = document.getElementsByName('copy-button-password')
    const usernameClipboards = document.getElementsByName('clipboard-username')
    const passwordClipboards = document.getElementsByName('clipboard-password')

    for (let i = 0, length = copyButtonsUsername.length; i < length; i++) {

        const copyButtonUsername = copyButtonsUsername[i]
        const copyButtonPassword = copyButtonsPassword[i]
        const username = usernameFields[i]
        const password = passwordFields[i]
        const usernameClipboard = usernameClipboards[i]
        const passwordClipboard = passwordClipboards[i]

        // Copies username input field value on click
        copyButtonUsername.addEventListener('click', () => { 

            username.select()
            document.execCommand('copy')

            usernameClipboard.setAttribute('src', '../static/images/clipboard-check.svg')
            window.getSelection().removeAllRanges()
            setTimeout(() => {
                usernameClipboard.setAttribute('src', '../static/images/clipboard.svg')
            }, 1500)

        })
        
        // Copies password input field value on click
        copyButtonPassword.addEventListener('click', () => {
            
            const value = password.getAttribute('value')
            
            // Workaround to allow copying "type: password" input fields
            const hiddenText = document.createElement('input')
            hiddenText.setAttribute('value', `${value}`)

            document.body.appendChild(hiddenText)

            hiddenText.select()
            document.execCommand('copy') // Deprecated, but it'll do for now...
            
            document.body.removeChild(hiddenText)
            
            passwordClipboard.setAttribute('src', '../static/images/clipboard-check.svg')
            window.getSelection().removeAllRanges()
            setTimeout(() => {
                passwordClipboard.setAttribute('src', '../static/images/clipboard.svg')
            }, 1500)
        })
    }


    // Create edit interface
    const editButtons = document.getElementsByName('edit-button')
    const domainCells = document.getElementsByName('domain-cell')
    const usernameCells = document.getElementsByName('username-cell')
    const passwordCells = document.getElementsByName('password-cell')
    const utilityCells = document.getElementsByName('utility-cell')

    for (i = 0, length = editButtons.length; i < length; i++) {
         
        const row = rows[i]
        const editButton = editButtons[i]
        const domainCell = domainCells[i]
        const usernameCell = usernameCells[i]
        const usernameField = usernameFields[i]
        const passwordCell = passwordCells[i]
        const utilityCell = utilityCells[i]
        const passwordField = passwordFields[i]

        // Remember row id
        const id = row.getAttribute('id')
        
        editButton.addEventListener('click', () => {

            // Get domain, username and password values
            const domain = domainCell.textContent
            const username = usernameField.getAttribute('value')
            const password = passwordField.getAttribute('value')

            // Change selected row cells into input fields for editing
                // Remove previous elements
                // Create and append input elements
                    // Insert previous values into the input fields
            
            row.removeChild(domainCell)
            row.removeChild(usernameCell)
            row.removeChild(passwordCell)
            row.removeChild(utilityCell)

            const newDomainCell = document.createElement('td')
            const domainInput = document.createElement('input')
            domainInput.setAttribute('autocomplete', 'off')
            domainInput.setAttribute('autofocus', 'true')
            domainInput.setAttribute('class', 'form-control mb-0 mx-0 w-auto')
            domainInput.setAttribute('value', `${domain}`)
            newDomainCell.appendChild(domainInput)

            const newUsernameCell = document.createElement('td')
            const usernameInput = document.createElement('input')
            usernameInput.setAttribute('autocomplete', 'off')
            usernameInput.setAttribute('autofocus', 'true')
            usernameInput.setAttribute('class', 'form-control mb-0 mx-0 w-auto')
            usernameInput.setAttribute('value', `${username}`)
            newUsernameCell.appendChild(usernameInput)

            const newPasswordCell = document.createElement('td')
            const passwordInput = document.createElement('input')
            passwordInput.setAttribute('autocomplete', 'off')
            passwordInput.setAttribute('autofocus', 'true')
            passwordInput.setAttribute('class', 'form-control mb-0 mx-0 w-auto')
            passwordInput.setAttribute('value', `${password}`)
            newPasswordCell.appendChild(passwordInput)

            const newUtilityCell = document.createElement('td')

            row.appendChild(newDomainCell)
            row.appendChild(newUsernameCell)
            row.appendChild(newPasswordCell)
            row.appendChild(newUtilityCell)

    
            // Create button for sending edit changes to the server
            const confirmButton = document.createElement('button')
            confirmButton.setAttribute('class', 'btn')
            confirmButton.setAttribute('title', 'Save Changes')
            confirmButton.setAttribute('type', 'button')

            const confirmIcon = document.createElement('img')
            confirmIcon.setAttribute('src', '../static/images/check-circle.svg')
            confirmIcon.setAttribute('alt', 'Save')

            confirmButton.appendChild(confirmIcon)
            newUtilityCell.appendChild(confirmButton)

            // Create button for canceling edition
            const cancelButton = document.createElement('button')
            cancelButton.setAttribute('class', 'btn')
            cancelButton.setAttribute('title', 'Cancel')
            cancelButton.setAttribute('type', 'button')

            const cancelIcon = document.createElement('img')
            cancelIcon.setAttribute('src', '../static/images/x-circle.svg')
            cancelIcon.setAttribute('alt', 'Cancel')
            
            cancelButton.appendChild(cancelIcon)
            newUtilityCell.appendChild(cancelButton)

            cancelButton.addEventListener('click', () => {location.reload()})
            
            domainInput.setAttribute('id', 'input-test')
            
            
            // Handle edit request
            confirmButton.addEventListener('click' , () => {

                const newDomain = domainInput.value
                const newUsername = usernameInput.value
                const newPassword = passwordInput.value
                
                // Send a UPDATE http request when user confirms edition
                // Adapted from: https://www.youtube.com/watch?v=cuEtnrL9-H0
                fetch('/', {
                    method: 'UPDATE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        id: id,
                        domain: newDomain,
                        username: newUsername,
                        password: newPassword
                    })
                })
                .then(response => {
                    if (response.ok) {
                        window.location.reload()
                    } else {
                        console.log('Error: ' + response.statusText)
                    }
                })
                .catch(error => {
                    console.log('Error: ' + error)
                })
            })
        })
    }
})
