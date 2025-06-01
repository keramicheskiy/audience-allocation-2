const BACKEND_URL = "http://localhost:8080";


const ROLES_CHOICES = {
    "teacher": "Преподаватель",
    "moderator": "Модератор",
    "admin": "Админ",
    "Преподаватель": "teacher",
    "Модератор": "moderator",
    "Админ": "admin",
};

const ROLES_COLORS = {
    "teacher": "green",
    "moderator": "blue",
    "admin": "red"
};

const ROLES = ["teacher", "moderator", "admin"];

function showError(message, duration = 3000) {
    const popup = document.getElementById('error-popup');
    popup.textContent = message;
    popup.style.display = 'block';

    setTimeout(() => {
        popup.style.display = 'none';
    }, duration);
}

function showMessage(message, duration = 3000) {
    const popup = document.getElementById('message-popup');
    popup.textContent = message;
    popup.style.display = 'block';

    setTimeout(() => {
        popup.style.display = 'none';
    }, duration);
}


function setCookie(name, value, days = 30) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(nameEQ)) {
            return decodeURIComponent(cookie.substring(nameEQ.length));
        }
    }
    return null;
}

function deleteCookie(name) {
    setCookie(name, "", -1);
}

function initTelegramWebApp() {
    if (window.Telegram && Telegram.WebApp) {
        Telegram.WebApp.ready();
    }
}

function isModerator(role) {
    return ["moderator", "admin"].includes(role);
}

function isAdmin(role) {
    return role === "admin";
}








