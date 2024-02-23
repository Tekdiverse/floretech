// Your frontend JavaScript
function updateUserData() {
    // Make an AJAX request to your Django proxy view
    fetch('https://www.profitopit.net/get_user_data/')
        .then(response => response.json())
        .then(data => {
            // Update your HTML elements with the received data
            document.getElementById('total_invested').innerText = data.total_invested;
            document.getElementById('total_deposit').innerText = data.total_deposit;
        })
        .catch(error => console.error('Error:', error));
}

// Call the function every certain seconds
setInterval(updateUserData, 3000);  // Adjust the interval as needed (5000 milliseconds = 5 seconds)

function updateTotalDeposit() {
    // Make an AJAX request to your Django proxy view
    fetch('https://www.profitopit.net/get_total_deposit/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total_deposits').innerText = data.total_deposits;
            document.getElementById('total_transactions').innerText = data.total_transactions;
        })
        .catch(error => console.error('Error:', error));
}

// Call the function every certain seconds
setInterval(updateTotalDeposit, 3000)

function triggerDailyTask() {
    fetch('https://www.profitopit.net/trigger_daily_task/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}
setInterval(triggerDailyTask, 2 * 60 * 60 * 1000);

$(document).ready(function(){
    $('#ForgotPasswordForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#ForgotPasswordBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
    
        $.ajax({
            type: 'POST',
            url: '/user/send-password-reset-email/',  // Update with your login view URL
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Login success
                    
                    // Redirect to the user profile page
                    window.location.href = '/';  // Update with the actual URL
                } else {
                    // Login failure
                    $("#ForgotPasswordErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#ForgotPasswordErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
                // Handle error
                console.log(error.responseText);
                
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#ForgotPasswordBtn').prop('disabled', false).html('Submit');
            }
        });
    });


})