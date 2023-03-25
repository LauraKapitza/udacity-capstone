# Dance Types


### `GET '/dance-types?page=${integer}'`

- Returns a list of dance types.
e - integer (optional)

- Response schema:
```
{
  "success": <Boolean>,
  "dance_types: <List>,
  "total_dance_types": <int>
}
```

- Response example:
```json
{
    "dance_types": [
        "hiphop",
        "ballet",
        "ballroom",
        "contemporary",
        "afrobeat",
        "jazz",
        "tap",
        "folk",
        "dancehall",
        "modern",
        "swing"
    ],
    "success": true,
    "total_dance_types": 11
}
```

---