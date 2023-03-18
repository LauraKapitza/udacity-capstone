# Dancing Queen Studio Project

## Introduction

This project is a digital dancing school where dance teachers can create and manage dance courses. 
Students can register to a course they like.

## Models

![alt text](.github/dancing-queens-studio.drawio.png)


## API

GET /classes
GET /classes/:id
POST /classes
PATCH /classes/:id
DELETE /classes/:id

GET /teachers
GET /teachers/:id
POST /teachers
PATCH /teachers/:id
DELETE /teachers/:id

GET /students
GET /students/:id
POST /students
PATCH /students/:id
DELETE /students/:id

GET /dance_types

## Frontend

## Deployment

Render.com is linked to this Github repository, whenever a new commit is pushed on 
master, it triggers a new deployment using the last commit.


## Instruction
Models will include at least…
- Two classes with primary keys at at least two attributes each
- [Optional but encouraged] One-to-many or many-to-many relationships between classes

Roles will include at least…
- Two roles with different permissions
- Permissions specified for all endpoints
Tests will include at least….
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role