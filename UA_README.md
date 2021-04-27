# Task 10 - SQL

Навчальний проєкт на платформі FoxMinded.

Завдання полягало у створенні Flask застосунку, створенні запитів до бази даних, створенні API.

## Початок

Застосунок складається із трьох елементів:

- [створення](#створення-бази-даних) бази даних та заповнення її експериментальними даними;
- [веб](#веб-застосунок-на-основі-Flask) застосунок на основі Flask;
- [API](#API-на-основі-Flask) на основі Flask.

### Підготовка

Проєкт створений із застосуванням pipenv.
Відтак, для початку роботи Вам необхідно встановити залежності:

`pipenv install`

Потім слід активувати середовище розробки:

`pipenv shell`

Проєкт містить файл `.env`.
Крім стандартних змінних `FLASK_APP` та `FLASK_ENV` у даному файлі збережено дані для доступу до віддаленої бази даних:
`DATABASE_URL`.
При потребі використовувати власну базу даних, необхідно змінити `DATABASE_URL`. Якщо ця змінна не буде визначена, застосунок намагатиметься з'єднатись із базою даних із застосуванням змінних
`DB_USER`, `DB_PW`, `DB_NAME`, `DB_PATH`.


### Створення бази даних

> **Warning**
> Під час виконання цієї операції данні наявної бази даних будуть знищені.

Дії виконуються у консолі з активованим середовищем.
Команда ```flask init-db``` 

- очистить наявну структуру бази даних;
- створить нову структуру;
- згенерує експериментальні дані;
- помістить їх у базу даних.

Основні кроки будуть показані у консолі.
У разі успішного завершення команди можна починати використовувати застосунок.

### Веб застосунок на основі Flask

Спільні для всіх сторінок елементи:

- На навігаційній панелі:
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
      <path fill-rule="evenodd" d="M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/>
      <path fill-rule="evenodd" d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"/>
      </svg> - перехід на початкову сторінку.
    - **Students** - таблиця студентів.
    - **Groups** - таблиця груп.
  
- <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up-square" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm8.5 9.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V11.5z"/>
  </svg> - гортання догори. Ця кнопка зникає, якщо гортання неможливе.


#### Початкова сторінка:

- кнопки "en" та "ua" дозволяють перемкнути мову даного документу (не всього застосунку).


#### Таблиця студентів:

  - На навігаційній панелі:
    
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg> - викликає вікно пошуку студентів. Можливий пошук за ім'ям, прізвищем, групою, курсом або будь-яка їх комбінація. Результатом пошуку буде таблиця студентів з відфільтрованими результатами. Якщо жоден з параметрів пошуку не буде заповнено, буде відображено список усіх студентів.
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-plus" viewBox="0 0 16 16">
      <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
      <path fill-rule="evenodd" d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"/>
      </svg> - викликає вікно додавання нового студента. Необхідними є лише ім'я та прізвище. Група додається автоматично на виконання умови завдання про розмір груп від 10 до 30 студентів. Курс або курси можуть бути додані пізніше у вікні редагування студента.
  
  - натискання на заповнену стрічку таблиці викликає вікно редагування студента. Можливо додавати або видаляти курси або видалити студента з бази даних. Додати можна лише курси, які студент ще не обрав.  

> Після завершення редагування студента таблицю буде перегорнуто до його позиції, останній редагований (створений) студент буде на короткий проміжок виділений у таблиці зеленим кольором.
Після видалення студента буде показаний рядок з написом "Deleted" в позиції видаленого студента. Він буде виділений червоним та згодом зникне.

#### Таблиця груп:
 
- На навігаційній панелі:
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg> - викликає вікно пошуку груп за кількістю студентів. Динамічно перевіряється належність введених символів до цифр.

> Список груп показується з назвами та кількістю студентів у групі.


### API на основі Flask

Підтримуються ті ж функції що й у веб застосунку.
Детальна документація за адресою: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)