# Task 10 - SQL

The educational project on the FoxMinded platform.

The task was creating a Flask application, making requests to a database, creating an API.

## Beginning

The application consists of three elements:

- [creation](#creating-a-database) of a database and filling it with experimental data;
- [web](#flask-based-web-application) application based on Flask;
- [API](#Flask-based-API) based on Flask.

### Preparation

This application was created with pipenv usage.
That`s why, to begin your work you need to install dependencies:

`pipenv install`

Next you need to activate the virtual environment:

`pipenv shell`

The project has an `.env` file.
Except usual `FLASK_APP` and `FLASK_ENV` variables in this file there is data for accessing the remote db:
`DATABASE_URL`.
As an alternative these files can be used: 
`DB_USER`, `DB_PW`, `DB_NAME`, `DB_PATH`.


### Creating a database

> **Warning**
> When using this operation data of the existent database will be deleted.

Actions are performed in console with active virtual environment.

Command ```flask init-db``` 

- clear current database structure;
- create a new structure;
- generate experimental data;
- place it in the database.

Main steps will be shown in console.

If the command usage was successful you can start using the app.

### Flask based web application

Elements common for all pages:

- On the navbar:
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house" viewBox="0 0 16 16">
      <path fill-rule="evenodd" d="M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/>
      <path fill-rule="evenodd" d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"/>
      </svg> - starting page.
    - **Students** - students table.
    - **Groups** - groups table.
  
- <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up-square" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm8.5 9.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V11.5z"/>
  </svg> - scrolling to top. This button is disabled, if scrolling is impossible.

#### Starting page:

- "en" and "ua" buttons allow switching languages of this document (only starting page).

#### Students table:

  - On the navbar:
    
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg> - Studens search by: name, surname, group, course or any their combination. The search result will be a table with filtered students. If all fields are empty the list of all students will be shown.
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-plus" viewBox="0 0 16 16">
      <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
      <path fill-rule="evenodd" d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"/>
      </svg> - calls a new student creation window. Only name and surname are required. Group is assigned automatically from the list of groups the size of which is bigger then 10 but lower than 30. Course or courses can be added in the student redaction window.
  
  - pressing on a table's filled row calls the student redaction window. It is possible to add or delete courses or to delete a student from the database. Only courses which the student didn't choose yet can be added.

> After student redaction process finishes, the table will be scrolled to the students position, last redacted or created student will be highlighted green for a short period of time. After students deletion on the position of the deleted student a row with "Deleted" will appear. It will glow red an after a small period of time it will disappear.

#### Groups table:
 
- On navbar:
    - <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg> - calls a window which filtrates groups by amounts of students. The entered symbols belonging to numbers is dynamically checked. 
    
> The groups list is shown with their names and the amounts of students. 

### Flask based API

Same functions as in the web app are supported.
Detailed documentation by link: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)
