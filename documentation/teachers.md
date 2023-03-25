# Teachers


### `GET '/teachers?page=${integer}'`

- Returns a list of paginated teachers.
- Request Query: 
  - page - integer (optional)
- Required token with:
  - "teachers:read"
- Response schema:
```
{
  "success": <Boolean>,
  "teachers: List<Dict>,
  "total_teachers": <int>
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
          "id": 2,
          "max_participants": 1,
          "start_time": "18:00",
          "title": "Amazing class"
        }
      ],
      "first_name": "John2",
      "id": "auth0|6416251ae32ba6997a88d75a",
      "last_name": "Doe2"
    }
  ],
  "success": true
}
```

---

### `GET '/teachers/${teacher_id}'`

- Gets a teacher by its given id
- Request Parameter: 
  - teacher_id (required)
- Required token with:
  - "teachers:read"
- Response schema:

```
{
  "success": <Boolean>,
  "teacher": <Dict>
}
```

- Response example:
```json
{
    "success": true,
    "teacher": {
        "classes": [
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
        "dance_types": [
            "hiphop"
        ],
        "first_name": "John",
        "id": "auth0|63f7e8eefa1ca7f48b811c93",
        "last_name": "Doe"
    }
}
```

---

### `POST '/teachers'`

- Creates a teacher with given properties
- Request body (in alphabetical order): 
  - user_id (required)
  - first_name (required)
  - last_name (required)
  - dance_types (required)
- Required token with:
  - "teachers:create"
- Response schema:
```
{
  "success": <Boolean>,
  "teacher": <Dict>
}
```

- Response example:
```json
{
    "success": true,
    "teacher": {
        "classes": [],
        "dance_types": [
            "hiphop"
        ],
        "first_name": "John",
        "id": "auth0|63f7e8eefa1ca7f48b811c932",
        "last_name": "Doe"
    }
}
```

---

### `DELETE '/teachers/${teacher_id}'`

- Deletes a teacher by its given id
- Request Parameter: 
  - teacher_id (required)
- Required token with:
  - "teachers:delete"
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

### `PATCH '/teachers/${teacher_id}'`

- Updates a specific teacher
- Request body : 
  - dance_types (optional)
  - first_name (optional)
  - last_name (optional)
- Required token with:
  - "teachers:update"
- Response schema:
```
{
  "success": <Boolean>,
  "teacher": <Dict>
}
```

- Response example:
```json
{
    "success": true,
    "teacher": {
        "classes": [],
        "dance_types": [
            "hiphop"
        ],
        "first_name": "John2",
        "id": "auth0|63f7e8eefa1ca7f48b811c93",
        "last_name": "Doe2"
    }
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
        "classes": [],
        "dance_types": [
            "hiphop"
        ],
        "first_name": "John2",
        "id": "auth0|63f7e8eefa1ca7f48b811c93",
        "last_name": "Doe2"
    },
    "success": true
}
```

---