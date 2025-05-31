const name_regex = /^[А-Яа-я]+$/;
const email_regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$/;

function validate(field, regex = /.*/, length_error = "_length_error", regex_error = "_error") {
    if (length_error)
        document.getElementById(field.id + length_error).hidden = field.value !== '';
    if (regex_error)
        document.getElementById(field.id + regex_error).hidden = regex.test(field.value);
    return regex.test(field.value) && field.value.length !== 0;
}