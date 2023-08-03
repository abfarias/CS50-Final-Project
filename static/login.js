document.addEventListener('DOMContentLoaded', () => {
    
    const password = document.getElementById('password')
    const masterPassword = document.getElementById('master_password')
    const check = document.getElementById('flexCheckDefault')

    // Create password visibility toggler
    check.addEventListener('click', () => {

        const passwordType = password.getAttribute('type');
        const masterPasswordType = masterPassword.getAttribute('type');

        if (passwordType && masterPasswordType == 'password') {
            password.setAttribute('type', 'text')
            masterPassword.setAttribute('type', 'text')
        } else {
            password.setAttribute('type', 'password')
            masterPassword.setAttribute('type', 'password')
        }
    })
})
