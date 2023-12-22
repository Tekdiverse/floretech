// Your frontend JavaScript
function updateUserData() {
    // Make an AJAX request to your Django proxy view
    fetch('https://www.profitopit.net/?url=https://www.profitopit.net/get_user_data/')
        .then(response => response.json())
        .then(data => {
            // Update your HTML elements with the received data
            document.getElementById('total_balance').innerText = data.total_balance;
            document.getElementById('total_invested').innerText = data.total_invested;
            document.getElementById('total_deposit').innerText = data.total_deposit;
        })
        .catch(error => console.error('Error:', error));
}

// Call the function every certain seconds
setInterval(updateUserData, 3000);  // Adjust the interval as needed (5000 milliseconds = 5 seconds)
