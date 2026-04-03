# API Usage for FlaskApp

This file documents API endpoints for Categories. Use with Postman or curl.

## Base URL

`http://localhost:8000/api`

---

## Categories

### GET all categories
- URL: `GET /api/categories`

### GET category by ID
- URL: `GET /api/categories/<id>`

### POST create category
- URL: `POST /api/categories`
- Body JSON:
  ```json
  {
    "name": "General",
    "description": "General category"
  }
  ```

### PUT replace category
- URL: `PUT /api/categories/<id>`

### PATCH update category
- URL: `PATCH /api/categories/<id>`

### DELETE category
- URL: `DELETE /api/categories/<id>`

---

## Postman Steps

1. Start server:
   ```bash
   python main.py
   ```
2. Open Postman.
3. Set request URL, method, and JSON body where needed.
4. Set header:
   - `Content-Type: application/json`
5. Click Send.
6. Check JSON response and status code.

## Example with curl

- Create category:
  ```bash
  curl -X POST http://localhost:8000/api/categories -H "Content-Type: application/json" -d '{"name":"Tech","description":"Technology category"}'
  ```
- Update category:
  ```bash
  curl -X PATCH http://localhost:8000/api/categories/1 -H "Content-Type: application/json" -d '{"description":"Updated technology category"}'
  ```
- Delete category:
  ```bash
  curl -X DELETE http://localhost:8000/api/categories/1
  ```
