document.addEventListener('DOMContentLoaded', () => {
    
    const previousPassword = document.getElementById('previous_master_password')
    const password = document.getElementById('new_master_password')
    const confirmation = document.getElementById('confirmation')
    const check = document.getElementById('flexCheckDefault')

    // Create password visibility toggler
    check.addEventListener('click', () => {

        const previousPasswordType = previousPassword.getAttribute('type')
        const passwordType = password.getAttribute('type')
        const confirmationType = confirmation.getAttribute('type')

        if (previousPasswordType && passwordType && confirmationType == 'password') {
            previousPassword.setAttribute('type', 'text')
            password.setAttribute('type', 'text')
            confirmation.setAttribute('type', 'text')
        } else {
            previousPassword.setAttribute('type', 'password')
            password.setAttribute('type', 'password')
            confirmation.setAttribute('type', 'password')
        }
    })
})
