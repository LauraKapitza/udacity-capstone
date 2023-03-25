# Students


### `GET '/students?page=${integer}'`

- Returns a list of paginated students.
- Request Query: 
  - page - integer (optional)
- Required token with:
  - "students:read"
- Response schema:
```
{
  "success": <Boolean>,
  "students: List<Dict>,
  "total_students": <int>
}
```

- Response example:
```json
{
    "students": [
        {
            "dance_classes": [
                {
                    "dance_types": [
                        "hiphop"
                    ],
                    "date": "2023-03-20",
                    "description": "I am an amazing dance class",
                    "end_time": "20:00",
                    "id": 1,
                    "max_participants": 15,
                    "start_time": "18:00",
                    "title": "Amazing class"
                }
            ],
            "first_name": "John",
            "id": "auth0|6416251ae32ba6997a88d75a",
            "last_name": "Doe"
        }
    ],
    "success": true,
    "total_students": 1
}
```

---

### `GET '/students/${student_id}'`

- Gets a student by its given id
- Request Parameter: 
  - student_id (required)
- Required token with:
  - "students:read"
- Response schema:

```
{
  "success": <Boolean>,
  "student": <Dict>
}
```

- Response example:
```json
{
    "student": {
        "dance_classes": [
            {
                "dance_types": [
                    "hiphop"
                ],
                "date": "2023-03-20",
                "description": "I am an amazing dance class",
                "end_time": "20:00",
                "id": 1,
                "max_participants": 15,
                "start_time": "18:00",
                "title": "Amazing class"
            }
        ],
        "first_name": "John",
        "id": "auth0|6416251ae32ba6997a88d75a",
        "last_name": "Doe"
    },
    "success": true
}
```

---

### `POST '/students'`

- Creates a student with given properties
- Request body (in alphabetical order): 
  - user_id (required)
  - first_name (required)
  - last_name (required)
- Required token with:
  - "students:create"
- Response schema:
```
{
  "success": <Boolean>,
  "student": <Dict>
}
```

- Response example:
```json
{
    "student": {
        "dance_classes": [],
        "first_name": "John",
        "id": "auth0|6416251ae32ba6997a88d75a2",
        "last_name": "Doe"
    },
    "success": true
}
```

---

### `DELETE '/students/${student_id}'`

- Deletes a student by its given id
- Request Parameter: 
  - student_id (required)
- Required token with:
  - "students:delete"
- Response schema:

```
{
  "success": <Boolean>,
  "deleted": <str>
}
```

- Response example:
```json
{
    "deleted": "auth0|63f7e8eefa1ca7f48b811c93",
    "success": true
}
```

---

### `PATCH '/students/${student_id}'`

- Updates a specific student
- Request body : 
  - first_name (optional)
  - last_name (optional)
- Required token with:
  - "students:update"
- Response schema:
```
{
  "success": <Boolean>,
  "student": <Dict>
}
```

- Response example:
```json
{
    "student": {
        "dance_classes": [
            {
                "dance_types": [
                    "hiphop"
                ],
                "date": "2023-03-20",
                "description": "I am an amazing dance class",
                "end_time": "20:00",
                "id": 1,
                "max_participants": 15,
                "start_time": "18:00",
                "title": "Amazing class"
            }
        ],
        "first_name": "John2",
        "id": "auth0|6416251ae32ba6997a88d75a",
        "last_name": "Doe2"
    },
    "success": true
}
```

### `GET '/me'`

- Returns user information.
- Required token
- Response schema:
```
{
  "success": <Boolean>,
  "me: <Dict>,
}
```

- Response example:
```json
{
    "me": {
        "dance_classes": [
            {
                "dance_types": [
                    "hiphop"
                ],
                "date": "2023-03-20",
                "description": "I am an amazing dance class",
                "end_time": "20:00",
                "id": 1,
                "max_participants": 15,
                "start_time": "18:00",
                "title": "Amazing class"
            }
        ],
        "first_name": "John",
        "id": "auth0|6416251ae32ba6997a88d75a",
        "last_name": "Doe"
    },
    "success": true
}
```

---