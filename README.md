# Django Boilerplate

Usually when working on a custom project we often have all the time the same boring code to rewrite over and over either users authentication and so much more...   
This project is a boilerplate for any Django (Django Rest Framework) project with 3rd party authentication.  

## Installation
### Basic installation
For installing this project you can run the following command:

Install python module:
```pip3 install -r requirements.txt``` (run this command in a virtual env if you have one)  
Install node modules:
```cd frontend && npm install```

### Docker
You can now use Docker to run this project. 
The command to use is the following:   
```docker-compose up --build```.  
The first time running the project, you'll have to make migrations with the following commands:  
```docker-compose exec api sh```  
Then:  
```python3 manage.py makemigrations && python3 manage.py migrate```

## Philosophy behind the project
Whenever I want to create a project, I always do the same boring part, the authentication related code.
Create the user, generate the basic authentication endpoints...  
To get rid of this, I decided to create this boilerplate. I can start every project by just cloning this repo and with little modification start working on the actual project.   
In order to have a correct starting point I wanted to add a lot of feature like social authentication... But the examples online are either outdated or not really what I needed. 
The aim to this project was to have a place where I have what I need (and I hope everyone else does).
To do this, I had to make some choices that are the followings:
-  I choosed some "over complicated" implementation way like working with custom user and social auth.
-  I did almost no design in the frontend (except the default vite.js design), because I believe that everyone will have his own design. The frontend part is only here to show you how everything works together. 

This project may contains features that you don't need for your project. 
I choosed to implement the most features possible for having in one place everything you can look for.
I believe that it's easier to remove some stuff that making work a lot of complicated feature.  

Before even running the project, please have a look at the *MyUser* in `accounts/models` and update it. As Django does not like users modification after a migration. 
If the model is ok with you, you can run the basic commands:  
```python3 manage.py makemigrations```  
```python3 manage.py migrate```

## Features
There are some of the current features:
-  Basic Custom User (check the *MyUser* model in `accounts/models`)
    - account creation ([localhost:3000/register](http://localhost:3000/register))
    - login ([localhost:3000/login](http://localhost:3000/login))
    - update password ([localhost:3000/update-password](http://localhost:3000/update-password))
    - generate a one time link for resetting password ([localhost:3000/password-reset-link](http://localhost:3000/password-reset-link))
    - reset password (click the link on the email)  
- Social User
    - Google
    - Facebook
- Custom permission (*CustomIsAuthenticated*)
- Unit testing  
- Docker  
- PostgreSQL  

  Next features to add:     
  -  Strip integretion
  -  Celery for queing
  -  Safer way to store JWT Token on the frontend (currently in the local storage)


## Usage

To run the project as is, follow these steps: 
-  rename the `.env.sample` into a `.env` file (with the correct values for your project).
-  run the following commands
    -  ```python3 manage.py runserver```
    -  ```npm run dev```

To use it as your own, please don't forget to delete (at least) the `.git` folder and the `README.md`.   
You can also remove the front folder. As I said, it's only here to show you how every parts work together. What I believe really important in this project are the Login component and the Services folder (contains methods related to the API).
