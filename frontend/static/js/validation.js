const name_regex = /^[А-Яа-я]+$/;
const email_regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const password_regex = /^[A-Za-z0-9@$!%*?&._-]{8,}$/;

function validate(field, regex = /.*/, length_error = "_length_error", regex_error = "_error") {
    if (length_error) {
        const lengthElem = document.getElementById(field.id + length_error);
        if (lengthElem) {
            lengthElem.hidden = field.value !== '';
        }
    }
    if (regex_error) {
        const regexElem = document.getElementById(field.id + regex_error);
        if (regexElem) {
            regexElem.hidden = regex.test(field.value);
        }
    }

    // if (!(regex.test(field.value) && field.value.length !== 0)) hideLoading();
    return regex.test(field.value) && field.value.length !== 0;
}

function validate_time(strTime) {
    const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
    return timeRegex.test(strTime);
}

function validate_date(strDate, format = 'DD-MM-YYYY') {
    try {
        let date;
        
        if (format === 'DD-MM-YYYY') {
            const parts = strDate.split('-');
            if (parts.length !== 3) return false;
            date = new Date(parts[2], parts[1] - 1, parts[0]);
        }
        
        return !isNaN(date.getTime()) && 
               date.toISOString().slice(0,10) === strDate;
    } catch (e) {
        return false;
    }
}