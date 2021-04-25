# Task 10 - SQL

Навчальний проект в рамках навчальної платформи FoxMinded.
Задвання полягало у створенні Flask застосунку, створенні запитів до бази данних, створенні API.

## Початок

Застуосунок складається із трьох елементів:

- створення бази даних та заповнення її експериментальними даними;
- Веб застосунок на основі Flask;
- API на основі Flask.

### Підготовка

Проект створений із застосуванням pipenv.
Відтак, для початку роботи Вам необхідно встановити залежності:

`pipenv install`

Потім слді активувати середовище розробки:

`pipenv shell`

Проект містить файл `.env`.
Крім стандартних змінних `FLASK_APP` та `FLASK_ENV` у даниму файлі збережено дані для доступу до відддаленої бази даних:
`DATABASE_URL`.
При потребі використовувати власну базу даних, необхідно змінити `DATABASE_URL`. Якщо ця змінна не буде визначена, застосунок намагатиметься підключиться до бази даних, із застосуванням змінних
`DB_USER`, `DB_PW`, `DB_NAME` , `DB_PATH`.


### Створення бази даних.

> ### <i class="fas fa-exclamation-triangle" aria-hidden="true"></i> **Warning**
> Під час виконання цієї обперації данні існуючої бази даних будуть знищені.
{: #warning}



Create an application that inserts/updates/deletes data in the database using sqlalchemy and flask resp framework.


Use PostgreSQL DB.

Models have to have next fields:
    
- GroupModel:

    - name


- StudentModel:

    - group_id

    - first_name

    - last_name


- CourseMode:

    - name

    - description 
  
1. Create SQL files with data:

create user and database. Assign all privileges on the database to the user.

create a file with tables creation

2. Create a python application

Generate test data:

10 groups with randomly generated names. The name should contain 2 characters, hyphen, 2 numbers

Create 10 courses (math, biology, etc)

200 students. Take 20 first names and 20 last names and randomly combine them to generate students.

Randomly assign students to groups. Each group could contain from 10 to 30 students. It is possible that some groups will be without students or students without groups

Create relation MANY-TO-MANY between tables STUDENTS and COURSES. Randomly assign from 1 to 3 courses for each student

3. Write SQL Queries:

Find all groups with less or equals student count.

Find all students related to the course with a given name.

Add new student

Delete student by STUDENT_ID

Add a student to the course (from a list)

Remove the student from one of his or her courses


Write tests using Unittest module or py.test.

Modify application using Flask Rest Framework. 


Write tests using Unittest module or py.test.