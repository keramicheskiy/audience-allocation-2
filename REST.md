Ручки(пути) для общения с бэкэндом с помощью REST API.
Для каждой ручки настроена проверка роли по токену, возвращаемому при регистрации или входе.
Если попробовать просто послать любой запрос, не передав с помощью COOKIE токен, вернется ошибка.

### Регистрация, вход, проверка входа.

/auth/register - Зарегистрироваться (POST).
{"first_name": "", "patronymic": "", "last_name": "", "email": "", "password": "", "role": ""}
/auth/login - Войти (POST).
{"email": "", "password": ""}
/auth/verify-token - Проверить вход + вернуть пользователя (GET).
/auth/role/is-confirmed - Проверить, подтверждена ли роль или нет (GET).

### Управление пользователями.

/users - Получить всех пользователей (GET).
/users/{user_id} - Получить пользователя (GET), изменить пользователя (PATCH).
/users/{user_id}/delete - Удалить пользователя (DELETE).
/users/<user_id>/role - Поменять роль пользователю (PATCH).
{"role": ""}
/users/<user_id>/wannabe - Получить запрошенную роль, если она есть (GET).
/users/<user_id>/lectures - Получить лекции преподавателя (GET).
/users/<user_id>/lectures/<lecture_id> - Удалить лекцию преподавателя (DELETE).
/users/<user_id>/auditoriums> - 
Получить все (GET), разрешить (POST) или запретить аудиторию преподавателю (DELETE).
{"auditorium_id": 1}
/users/<user_id>/auditoriums - Получить все аудитории (GET).
/users/<user_id>/auditoriums/reset - Запретить все аудитории преподавателю (DELETE).
/users/<user_id>/limit/hours - Ограничить максимальное количество часов брони (PATCH).
{"amount": 1}
/users/<user_id>/limit/auditoriums - Ограничить максимальное количество броней (PATCH).
{"amount": 1}
/users/<user_id> - Получить пользователя по айди (GET).

### Управление лекциями.

/lectures - Получить все лекции (GET).
/lectures/upcoming - Получить все предстоящие лекции (GET).
/lectures/<lecture_id> - Получить (GET) или удалить лекцию (DELETE).

### Управление аудиториями.

/auditoriums?date=2025-12-31&start=10:45&end=12:15 - Получить все свободные разрешенные
(если указаны ключи date, start, end) аудитории для пользователя (GET).
/auditoriums/<auditorium_id> - Получить аудиторию, если она свободна и разрешена (GET).
/auditoriums/new - Создать аудиторию (POST).
{"number": "", "size": 1, "equipment": 1, "location": "", "description": ""}
/auditoriums/<auditorium_id>/change - Изменить аудиторию (PATCH).
{"number": "", "size": 1, "equipment": 1, "location": "", "description": ""}
/auditoriums/<auditorium_id>/delete - Удалить аудиторию (DELETE).
/auditoriums/<auditorium_id>/book - Забронировать аудиторию на указанное время для данного пользователя (POST).
{"date"="2025-12-31", "start"="10:45", "end"="12:15"}

### Управление оборудованием.

/equipments - Получить все виды оборудования (GET).
/equipments/new - Создать оборудование (POST).
{"name": ""}
/equipments/<equipment_id> - Получить (GET), изменить (PATCH) или удалить оборудование (DELETE).
{"name": ""}

### Всё связанное с пользователем, пославшим запрос.

/my/profile - Получить пользователя (GET).
/my/lectures - Получить все лекции пользователя (GET).
/my/lectures/upcoming - Получить все непрошедшие лекции данного пользователя (GET).

### Управление запросами о подтверждении роли, указанной пользователем при регистрации.

/requests - Получить все запросы на подтверждение роли (GET).
/requests/<request_id> - Подтвердить (PATCH) или удалить заявку (DELETE).
{}








