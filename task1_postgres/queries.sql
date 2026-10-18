-- 1. Отримати всі завдання певного користувача (за user_id = 1)
SELECT * FROM tasks 
WHERE user_id = 1;

-- 2. Вибрати завдання за певним статусом, використовуючи підзапит ('new')
SELECT * FROM tasks 
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання (наприклад, завдання id = 1 перевести в 'in progress')
UPDATE tasks 
SET status_id = (SELECT id FROM status WHERE name = 'in progress') 
WHERE id = 1;

-- 4. Отримати список користувачів, які не мають жодного завдання (SELECT, WHERE NOT IN і підзапит)
SELECT * FROM users 
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL);

-- 5. Додати нове завдання для конкретного користувача (user_id = 1)
INSERT INTO tasks (title, description, status_id, user_id) 
VALUES ('Підготувати звіт з HW03', 'Оформити репозиторій та відправити ментору', 1, 1);

-- 6. Отримати всі завдання, які ще не завершено (чиший статус не є 'completed')
SELECT * FROM tasks 
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити конкретне завдання (наприклад, id = 5)
DELETE FROM tasks 
WHERE id = 5;

-- 8. Знайти користувачів з певною електронною поштою (умова LIKE)
SELECT * FROM users 
WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача (для id = 1)
UPDATE users 
SET fullname = 'Тарас Шевченко' 
WHERE id = 1;

-- 10. Отримати кількість завдань для кожного статусу (SELECT, COUNT, GROUP BY)
SELECT s.name AS status_name, COUNT(t.id) AS total_tasks 
FROM status s 
LEFT JOIN tasks t ON s.id = t.status_id 
GROUP BY s.name;

-- 11. Отримати завдання, призначені користувачам з певною доменною частиною електронної пошти
SELECT t.* 
FROM tasks t 
JOIN users u ON t.user_id = u.id 
WHERE u.email LIKE '%@example.com';

-- 12. Отримати список завдань, що не мають опису (IS NULL або порожній)
SELECT * FROM tasks 
WHERE description IS NULL OR description = '';

-- 13. Вибрати користувачів та їхні завдання у статусі 'in progress' (INNER JOIN)
SELECT u.fullname, t.title, t.description, s.name AS status_name
FROM users u 
INNER JOIN tasks t ON u.id = t.user_id 
INNER JOIN status s ON t.status_id = s.id 
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань (LEFT JOIN та GROUP BY)
SELECT u.id, u.fullname, COUNT(t.id) AS total_tasks 
FROM users u 
LEFT JOIN tasks t ON u.id = t.user_id 
GROUP BY u.id, u.fullname;