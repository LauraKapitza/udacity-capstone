# Roles

Authentication: This application requires authentication to perform various actions. All the endpoints require various permissions, except the root (or health) endpoint, that are passed via the Bearer token.

The application has three different types of roles:

## Students
can view students, teachers and classes. 
can join and leave a class
has:
```
classes:join
classes:read
students:read
teachers:read
```

## Dance teacher
can view students, teachers and classes. 
can update his own information
can create, edit and delete a class
has:
```
classes:create
classes:delete
classes:read
classes:update
students:read
teachers:read
teachers:update
```
    
    
## Dance studio manager
can view students, teachers and classes. 
can create and delete teachers
can create and delete students
can create and delete classes
has:
```
classes:delete
classes:read
students:create
students:delete
students:read
teachers:create
teachers:delete
teachers:read
```