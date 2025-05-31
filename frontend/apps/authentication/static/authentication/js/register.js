let firstName = document.getElementById('first_name');
let patronymic = document.getElementById('patronymic');
let lastName = document.getElementById('last_name');
let email = document.getElementById('email');
let password = document.getElementById('password');
let registerButton = document.getElementById('register_button');

let tg_id = null;
if (window.Telegram && window.Telegram.WebApp) {
    const tg = window.Telegram.WebApp;
    tg.ready();

    if (tg.initDataUnsafe && tg.initDataUnsafe.user && tg.initDataUnsafe.user.id) {
        tg_id = tg.initDataUnsafe.user.id;
    }
}

registerButton.addEventListener('click', async () => {
    if (validate(firstName, name_regex) && validate(patronymic, name_regex) && validate(lastName, name_regex) &&
        validate(email, email_regex) && validate(password, password_regex)) {
        let data = {
            firstName: firstName.value,
            patronymic: patronymic.value,
            lastName: lastName.value,
            email: email.value,
            role: document.getElementById('role').value,
            password: password.value,
        };
        if (tg_id !== null) {
            data.tg_id = Telegram.WebApp.initDataUnsafe.user.id;
        }
        const response = await fetch(`${BACKEND_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            const data = await response.json();
            setCookie("Token", data.token);
            window.location.replace("/profile");
        } else {
            const errorData = await response.json();
            document.getElementById('registration-form').reset();
            showError(`Ошибка: ${errorData.message || "Что-то пошло не так"}`);
        }
    }
})