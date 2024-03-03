
function updateUserData() {
    fetch('https://www.profitopit.net/get_user_data/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total_invested').innerText = data.total_invested;
            document.getElementById('total_deposit').innerText = data.total_deposit;
        })
}

setInterval(updateUserData, 3000);

function updateTotalDeposit() {
    fetch('https://www.profitopit.net/get_total_deposit/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total_deposits').innerText = data.total_deposits;
            document.getElementById('total_transactions').innerText = data.total_transactions;
        })

    
}

setInterval(updateTotalDeposit, 3000)

function triggerDailyTask() {
    fetch('https://www.profitopit.net/trigger_daily_task/', {
        method: 'GET',
    })
    .then(response => response.json())
}
setInterval(triggerDailyTask, 2 * 60 * 60 * 1000);

$(document).ready(function(){
    $('#ForgotPasswordForm').on('submit', function(e) {
        e.preventDefault();

        $('#ForgotPasswordBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
    
        $.ajax({
            type: 'POST',
            url: '/user/send-password-reset-email/', 
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {

                    $('.dissapear-content').html("")
                    $('#passwordCheckmark').html('<div style="display: flex; align-items: center; justify-content: center;"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12L9 18L21 6" stroke="rgba(0,0,0,0.95)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>')
                    $('#passwordMessage').html('<p>An email has been sent to your account to reset your password.</p>')
                } else {
                    $("#ForgotPasswordErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#ForgotPasswordErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
                
                
            },
            complete: function() {
                $('#ForgotPasswordBtn').prop('disabled', false).html('Submit');
            }
        });
    });


})