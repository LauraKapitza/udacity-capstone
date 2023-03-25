
# API Errors

When a request fails, the API will send on of the following errors:

- 400: Bad Request 
- 401: Unauthorized 
- 403: Forbidden 
- 404: Resource not found 
- 405: Method Not Allowed 
- 422: Unprocessable 
- 500: Internal Server Error

Error schema
```
{
  "success": <Boolean>,
  "error": <Int>,
  "message": <String>
}
```

Error example for 404:

```json
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```