/* Password Field */
document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password-field');
    const toggleIcon = document.getElementById('toggle-icon');
    const togglePassword = () => {
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordField.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    };
    
    if (toggleIcon) {
        toggleIcon.addEventListener('click', togglePassword);
    }
});


jQuery(document).ready(function($) {
        /*====================================
			Select2 JS
		======================================*/ 
		$('select').niceSelect();

	
});


