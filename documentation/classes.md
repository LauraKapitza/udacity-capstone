# Classes


### `GET '/classes?page=${integer}'`

- Returns a list of paginated dance classes.
- Request Query: 
  - page - integer (optional)
- Required token with:
  - "classes:read"
- Response schema:
```
{
  "success": <Boolean>,
  "classes: List<Dict>,
  "total_classes": <int>
}
```

- Response example:
```json
{
    "classes": [
        {
            "dance_types": [
                "ballet"
            ],
            "date": "Sat, 25 Mar 2023 00:00:00 GMT",
            "description": "This a ballet dance class",
            "end_time": "20:00",
            "id": 1,
            "max_participants": 15,
            "participants": [
                {
                    "first_name": "Jane",
                    "id": 1,
                    "last_name": "Doe"
                }
            ],
            "start_time": null,
            "teacher": {
                "first_name": "John",
                "id": 1,
                "last_name": "Doe"
            },
            "title": "Ballet for Everyone"
        }
    ],
    "success": true,
    "total_classes": 12
}
```

---

### `GET '/classes/${class_id}'`

- Gets a dance class by its given id
- Request Parameter: 
  - class_id (required)
- Required token with:
  - "classes:read"
- Response schema:

```
{
  "success": <Boolean>,
  "class": <Dict>
}
```

- Response example:
```json
{
    "success": true,
    "class": {
        "dance_types": [
            "hiphop"
        ],
        "date": "Mon, 20 Mar 2023 00:00:00 GMT",
        "description": "I am an amazing dance class",
        "end_time": "20:00",
        "id": 2,
        "max_participants": 15,
        "participants": [],
        "start_time": "18:00",
        "teacher": {
            "first_name": "John",
            "id": 1,
            "last_name": "Doe"
        },
        "title": "Amazing class"
    }
}
```

---

### `POST '/classes'`

- Creates a dance class with given properties if user is a teacher
- Request body (in alphabetical order): 
  - date (required)
  - dance_types (required)
  - description (required)
  - end_time (required)
  - max_participants (required)
  - start_time (required)
  - title (required)
- Required token with:
  - "classes:create"
- Response schema:
```
{
  "success": <Boolean>,
  "class": <Dict>
}
```

- Response example:
```json
{
    "class": {
        "dance_types": [
            "hiphop"
        ],
        "date": "Mon, 20 Mar 2023 00:00:00 GMT",
        "description": "I am an amazing dance class",
        "end_time": "20:00",
        "id": 2,
        "max_participants": 15,
        "participants": [],
        "start_time": "18:00",
        "teacher": {
            "first_name": "John",
            "id": 1,
            "last_name": "Doe"
        },
        "title": "Amazing class"
    },
    "success": true
}
```

---

### `DELETE '/classes/${class_id}'`

- Deletes a dance class by its given id
- Request Parameter: 
  - class_id (required)
- Required token with:
  - "classes:delete"
- Response schema:

```
{
  "success": <Boolean>,
  "deleted": <int>
}
```

- Response example:
```json
{
    "success": true,
    "deleted": 1
}
```

---

### `PATCH '/classes/${class_id}'`

- Updates a specific dance class if user is a teacher
- Request body (in alphabetical order): 
  - date (optional)
  - dance_types (optional)
  - description (optional)
  - end_time (optional)
  - start_time (optional)
  - title (optional)
- Required token with:
  - "classes:update"
- Response schema:
```
{
  "success": <Boolean>,
  "class": <Dict>
}
```

- Response example:
```json
{
    "class": {
        "dance_types": [
            "hiphop"
        ],
        "date": "Mon, 20 Mar 2023 00:00:00 GMT",
        "description": "I am an amazing dance class",
        "end_time": "20:00",
        "id": 2,
        "max_participants": 15,
        "participants": [],
        "start_time": "18:00",
        "teacher": {
            "first_name": "John",
            "id": 1,
            "last_name": "Doe"
        },
        "title": "Amazing class"
    },
    "success": true
}
```

---

### `POST '/classes/${class_id}/participants'`

- Adds a student as a new participant to an existing dance class
- Request Parameter: 
  - class_id (required)
- Request body: 
  - user_id (required)
- Required token with:
  - "classes:join"
- Response schema:
```
{
  "success": <Boolean>,
  "class_id": <Int>,
  "added_participant": <Dict>
}
```

- Response example:
```json
{
  "added_participant": {
    "first_name": "Joe",
    "id": 1,
    "last_name": "Doe"
  },
  "class_id": 5,  
  "success": true
}
```

---

### `DELETE '/classes/${class_id}/participants'`

- Removes a participant from a dance class
- Request Parameter: 
  - class_id (required)
- Request body: 
  - user_id (required)
- Required token with:
  - "classes:join"
- Response schema:

```
{
  "success": <Boolean>,
  "class_id": <Int>,
  "removed_participant": <Dict>
}
```

- Response example:
```json
{
  "class_id": 5,  
  "success": true,
    "removed_participant": {
      "first_name": "Joe",
      "id": 1,
      "last_name": "Doe"
    }
}
```

---