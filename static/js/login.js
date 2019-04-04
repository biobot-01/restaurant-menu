$(document).ready(function() {
    $('#signinButton').click(function() {
        function signInCallback(authResult) {
            if (authResult['code']) {
                // Hide the sign-in button now that the user is authorized
                $('#signinButton').attr('style', 'display: none');

                // Send the one-time-code to the server, if the server
                // responds, write a 'login successful' message & redirect
                // back to the main restaurants page
                $.ajax({
                    type: 'POST',
                    url: '/gconnect?state={{ STATE }}',
                    // Include `X-Requested-With` header
                    // to protect against CSRF attacks
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    contentType: 'application/octet-stream; charset=utf-8',
                    processData: false,
                    data: authResult['code'],
                    success: function(result) {
                        // Handle or verify the server response
                        $('#result').text(function() {
                            return 'Login Successful! Redirecting... ' + result
                        });

                        setTimeout(function() {
                            window.location.href = '/';
                        }, 2000);
                    }
                });
            } else if (authResult['error']) {
                // Handle the error
                console.log('There was an error: ' + authResult['error']);
            } else {
                // Handle no response
                $('#result').text(function() {
                    return 'Failed to make a server call. Check your configuration and console.'
                });
            }
        }

        auth2.grantOfflineAccess().then(signInCallback);
    });
});
