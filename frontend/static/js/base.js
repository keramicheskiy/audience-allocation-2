await verifyTokenAndPopulateUser();

const menuBtn = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');
menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
});
const logoutBtn = document.getElementById('logoutBtn'); // ВЫЙТИ МОЖНО ТОЛЬКО В ПРОФИЛЕ
logoutBtn.addEventListener('click', () => {
    deleteCookie('Token');
    window.location.reload();
})
const username = document.getElementById('username');
username.addEventListener('click', () => {
    window.location.replace('/users/profile');
})


async function verifyTokenAndPopulateUser() {
    try {
        const response = await fetch('http://localhost:8080/auth/verify-token', {
            method: 'GET',
            credentials: 'include' // Обязательно для отправки куки
        });

        if (!response.ok) {
            window.location.replace('/auth/login');
            return;
        }

        const user = await response.json();

        document.getElementById('user-role').textContent = user.role;

        document.getElementById('user-role-box').style.color = ROLES_COLORS[user.role];

        document.getElementById('username').textContent = `${user.first_name} ${user.patronymic} ${user.last_name}`;

        hideUnavailableElements(user.role);

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

function getPermittedRoles(role) {
    const ROLES = ["teacher", "moderator", "admin"];
    return ROLES.slice(ROLES.indexOf(role), ROLES.length);
}

function hideUnavailableElements(role) {
    const index = ROLES.indexOf(role);
    if (index === -1) window.location.replace("/errors/bad_role")
    let unavailable_roles = ROLES.slice(ROLES.indexOf(role) + 1, ROLES.length);
    for (let unavailable_role of unavailable_roles) {
        for (let element of document.getElementsByClassName(`menu ${unavailable_role}`)) {
            element.style.display = 'none';
        }
    }
}



