const letterOnly = /^[A-Za-z ]+$/;
const phone = /^([0-9]{10})\b/;
const letterNumber = /^[A-Za-z0-9]+$/

function validateForm() {
    const fname = $("#fname").val();
    const phone = $("#phone").val();
    const username = $("#username").val();
    const password = $("#password").val();

    isValidName(fname);
    isValidPhone(phone);
    isValidUsername(username)
    isValidPassword(password)
}


function isValidName(fname) {
    if (fname.length < 2 || fname.length > 100) {
        $("#fname_Error").html("Last name must contain 2-100 characters");
    } else if (!letterOnly.test(fname)) {
        $("#fname_Error").html("Last name must contain letters and SPACE only");
    } else $("#fname_Error").html("");
}

function isValidUsername(username) {
    if (username.length < 2 || username.length > 100) {
        $("#username_Error").html("Username must contain 2-100 characters");
    } else if (!letterNumber.test(username)) {
        $("#username_Error").html("Username must contain letters and numbers only");
    } else $("#username_Error").html("");
}

function isValidPhone(phone) {
    if (phone.test(phone)) {
        $("#phone_Error").html("");
    } else $("#phone_Error").html("Invalid phone format. Phone must contain 10 digits");
}

function isValidPassword(password) {
    if (password.length < 6) {
        $("#password_Error").html("Password must contain at least 6 characters");
    }
}

$("#registerBtn").click(validateForm);
