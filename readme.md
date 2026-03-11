# LLM App

## General Info
This project leverages Llama 2 running locally as the backend, with FastAPI handling the API endpoints. The frontend is built using Vue.js to provide an interactive dashboard.

## Clone the Repository
```bash
git clone https://github.com/najeeb464/llm-app.git
```

## Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv env
   ```
3. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source env/bin/activate
     ```
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
5. Run the backend server:
   ```bash
   python3 main.py
   ```

## Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend/llm-app
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Notes
- Ensure you have Python 3 and Node.js installed.
- Make sure to activate the virtual environment each time before running the backend.
- The frontend will be accessible at `http://localhost:3000` (default Vue.js dev server port).

## Enjoy exploring the LLM App!