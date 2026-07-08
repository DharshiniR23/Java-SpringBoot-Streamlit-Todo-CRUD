# 📝 Full Stack Todo CRUD Application

A complete **Todo Management System** developed using **Java Spring Boot, MySQL, Streamlit, and REST API**.

This project demonstrates how a frontend application communicates with a backend REST API to perform CRUD operations and store data permanently in a MySQL database.

---

## 🚀 Project Overview

The Todo Application allows users to create, view, update, and delete tasks using an interactive Streamlit frontend.

All frontend actions are processed through Spring Boot REST APIs and changes are reflected instantly in the MySQL database and Postman API responses.

---

## ✨ Features

- ➕ Create new Todo tasks
- 📋 View all Todo records
- ✏️ Update Todo details and completion status
- 🗑️ Delete Todo tasks
- 🔗 REST API integration
- 💾 MySQL database connectivity
- 🌐 Interactive Streamlit dashboard
- 🧪 API testing using Postman

---

## 🛠️ Technologies Used

### Backend
- Java
- Spring Boot
- Spring Data JPA
- Hibernate
- Maven

### Frontend
- Python
- Streamlit

### Database
- MySQL

### API Testing Tool
- Postman

### Development Tools
- Visual Studio Code
- MySQL Workbench
- Git & GitHub

---

## 📂 Project Structure


Todo-CRUD-Application

│
├── demo                         # Spring Boot Backend
│
│   ├── src
│   │   └── main
│   │       ├── java
│   │       └── resources
│   │
│   ├── pom.xml
│
│
├── todo-frontend                # Streamlit Frontend
│
│   ├── app.py
│   └── requirements.txt
│
│
├── postman                      # API Collection
│
└── README.md

---

# Backend Configuration

## 1. Create MySQL Database

Open MySQL Workbench:

sql
CREATE DATABASE todo;


---

## 2. Configure application.properties

Path:


demo/src/main/resources/application.properties


Configuration:

properties
server.port=8087

spring.datasource.url=jdbc:mysql://localhost:3306/todo?allowPublicKeyRetrieval=true&useSSL=false

spring.datasource.username=root

spring.datasource.password=your_mysql_password

spring.jpa.hibernate.ddl-auto=update

spring.jpa.show-sql=true


---

## 3. Run Spring Boot Application

Run:

TodoApplication.java


Backend starts on:

http://localhost:8087

---

# REST API Endpoints

## Get All Todos


GET /api/todos

Example Response:

json
[
 {
  "id":1,
  "title":"Learn Java Spring Boot",
  "description":"Complete Todo Project",
  "completed":true
 }
]


---

## Create Todo


POST /api/todos

Request:

json
{
"title":"Learn Streamlit",
"description":"Connect frontend with backend",
"completed":false
}


---

## Update Todo


PUT /api/todos/{id}

Request:

json
{
"title":"Updated Task",
"description":"Task updated successfully",
"completed":true
}


---

## Delete Todo

DELETE /api/todos/{id}

---

# Frontend Setup (Streamlit)

Move to frontend folder:

cd todo-frontend


Install dependencies:

pip install -r requirements.txt

Run Streamlit:

streamlit run app.py

Frontend opens at:

http://localhost:8501

---

# Application Workflow


User
 |
 |
Streamlit Frontend
 |
 |
Spring Boot REST API
 |
 |
Spring Data JPA
 |
 |
MySQL Database


Postman → API Testing

---

# CRUD Operation Flow

### CREATE


Streamlit Form
      ↓
POST API
      ↓
MySQL Insert

---

### READ


GET API
   ↓
Fetch Data
   ↓
Display Dashboard

---

### UPDATE


Update Button
      ↓
PUT API
      ↓
Database Updated


---

### DELETE


Delete Button
      ↓
DELETE API
      ↓
Record Removed


---

# Testing

Tested using:

✔ Streamlit UI  
✔ Postman API  
✔ Browser API response  
✔ MySQL Database records  

---

# Learning Outcomes

Through this project, I learned:

- Building REST APIs using Spring Boot
- Connecting Java applications with MySQL
- Performing CRUD operations
- API testing using Postman
- Creating frontend dashboards using Streamlit
- Integrating frontend with backend services

---

# Future Enhancements

- User authentication
- Search and filter tasks
- Task priority levels
- Due date reminder
- Deployment

---

# Author

**Dharshini R**

Passionate about learning and building real-world applications 🚀

Skills:

Java
Spring Boot
MySQL 
Python
Streamlit
REST API

---

⭐ If you like this project, give it a star!
