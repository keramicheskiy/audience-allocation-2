const email = document.getElementById('email');
const password = document.getElementById('password');

const loginButton = document.getElementById('login-button');

let tg_id = null;
if (window.Telegram && window.Telegram.WebApp) {
    const tg = window.Telegram.WebApp;
    tg.ready();

    if (tg.initDataUnsafe && tg.initDataUnsafe.user && tg.initDataUnsafe.user.id) {
        tg_id = tg.initDataUnsafe.user.id;
    }
}

loginButton.addEventListener('click', async () => {

    if (validate(email, email_regex) && validate(password, password_regex)) {
        let data = {
            email: email.value,
            password: password.value,
        };
        if (tg_id !== null) {
            data.tg_id = tg_id;
        }
        const response = await fetch(`${BACKEND_URL}/auth/login`, {
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
            document.getElementById('login-form').reset();
            showError(`Ошибка: ${errorData.message || "Что-то пошло не так"}`);
        }
    }
})

