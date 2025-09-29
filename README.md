# 🍳 Recipes Full-Stack Application

Monorepo with **FastAPI backend** and **React + TypeScript frontend**.

---

## 🚀 Run with Docker

### 1. Start Recipe App
```bash
docker compose up --build
```

- Backend Swagger: http://localhost:8000/docs  
- Frontend SPA:    http://localhost:5173  

Stop all services:
```bash
docker compose down
```

---

### 2. Start App Backend Only
```bash
docker compose up backend --build
```

- Swagger docs: http://localhost:8000/docs  

---

### 3. Start App Frontend Only
⚠️ Make sure the backend is running (via Docker or locally).

```bash
docker compose up frontend --build
```

- Frontend: http://localhost:5173  

---

### 4. Detached Mode
Run in background:
```bash
docker compose up -d
```

Stop:
```bash
docker compose down
```

---

## 💻 Run Without Docker

### Backend (FastAPI)
1. Create and activate a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:
   ```bash
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Run tests:
    ```bash
    pytest

- Backend available at: http://localhost:8000  
- Swagger docs: http://localhost:8000/docs  


---

### Frontend (React + Vite)
1. Navigate to the frontend:
   ```bash
   cd recipe_app_ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```

4. Run tests:
    ```bash
    npm test
    ```

5. Run CI-mode tests (JUnit XML output):
    ```bash
    npm run test:ci
    ```

- Frontend available at: http://localhost:5173  
- By default, API calls go to http://localhost:8000  



---

## 🧪 Running Tests with Docker

### Run All Tests (Backend + Frontend)
```bash
docker compose -f docker-compose.test.yml up --build
```
Runs both backend and frontend test suites, then exits.

---

### Run Only Backend Tests
```bash
docker compose -f docker-compose.test.yml up --build backend-test
```

Pytest logs report: `./backend/test-logs/pytest.log`

---

### Run Only Frontend Tests
```bash
docker compose -f docker-compose.test.yml up --build frontend-test
```

JUnit XML report: `./recipe_app_ui/test-logs/frontend-tests.xml`

---

## 🖥 Tech Stack

### Backend
- **FastAPI**, in-memory **SQLite**
- Endpoints:
  - `GET /recipes?search=text`
  - `GET /recipes/{id}`
- Features: exception handling, validation, logging, layered architecture

### Frontend
- **React + TypeScript (Vite)**
- Features: global search, client-side sort/filter, responsive grid, lazy-loaded grid
- Uses **Tailwind CSS**, **lucide-react icons**, and **React Intersection Observer**

---

## 📝 Dev Notes
- In-memory DB seeded from [dummyjson.com/recipes](https://dummyjson.com/recipes) at startup.  
- To proxy API calls during local dev, add to `vite.config.ts`:

  ```ts
  export default {
    server: {
      proxy: {
        "/recipes": "http://localhost:8000",
      },
    },
  };
  ```

