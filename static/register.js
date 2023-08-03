document.addEventListener('DOMContentLoaded', () => {
    
    const password = document.getElementById('password')
    const confirmation = document.getElementById('confirmation')
    const masterPassword = document.getElementById('master_password')
    const check = document.getElementById('flexCheckDefault')

    // Create password visibility toggler
    check.addEventListener('click', () => {

        const passwordType = password.getAttribute('type')
        const confirmationType = confirmation.getAttribute('type')
        const masterPasswordType = masterPassword.getAttribute('type')

        if (passwordType && masterPasswordType && confirmationType == 'password') {
            password.setAttribute('type', 'text')
            confirmation.setAttribute('type', 'text')
            masterPassword.setAttribute('type', 'text')
        } else {
            password.setAttribute('type', 'password')
            confirmation.setAttribute('type', 'password')
            masterPassword.setAttribute('type', 'password')
        }
    })
})
