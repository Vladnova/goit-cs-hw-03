-- 1. Отримати всі завдання певного користувача
SELECT * FROM tasks WHERE user_id = 3;

-- 2. Вибрати завдання за певним статусом
SELECT * FROM tasks WHERE status_id = (SELECT id FROM statuses WHERE name = 'new');

-- 3. Оновити статус конкретного завдання
UPDATE tasks SET status_id = (SELECT id FROM statuses WHERE name = 'in progress') WHERE id = 5;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task', 'Description', 1, 3);

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks WHERE status_id != (SELECT id FROM statuses WHERE name = 'completed');

-- 7. Видалити конкретне завдання
DELETE FROM tasks WHERE id = 10;

-- 8. Знайти користувачів з певною електронною поштою
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- 9. Оновити ім'я користувача
UPDATE users SET fullname = 'Updated Name' WHERE id = 2;

-- 10. Отримати кількість завдань для кожного статусу
SELECT status_id, COUNT(*) FROM tasks GROUP BY status_id;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
SELECT tasks.* FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@ukr.net';

-- 12. Отримати список завдань, що не мають опису
SELECT * FROM tasks WHERE description IS NULL;

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT users.fullname, tasks.title FROM users
JOIN tasks ON users.id = tasks.user_id
WHERE tasks.status_id = (SELECT id FROM statuses WHERE name = 'in progress');

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT users.fullname, COUNT(tasks.id) AS task_count FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id;
