ANIMAL LIVESTOCK EXPENSE AND INCOME TRACKER

Technology
- Python 3.x
- Flask
- SQLite
- HTML, CSS and JavaScript
- Chart.js (loaded from CDN in the dashboard/report pages)

Run the project
1. Open this folder in VS Code.
2. Open a terminal in this folder.
3. Create and activate a virtual environment if needed:
   python -m venv venv
   Windows PowerShell: .\venv\Scripts\Activate.ps1
4. Install Flask:
   pip install flask
5. Start the application:
   python app.py
6. Open http://127.0.0.1:5000 in your browser.

Shared database
- The application uses only livestock.db.
- database.py is the only database connection module.
- Required tables: animals, income, expenses.
- The database is stored beside database.py, so starting the app from another
  working directory will not accidentally create a second database.

Member 4 updates in this repaired version
- Dashboard total animals is the sum of animals.quantity.
- Dashboard and reports use the shared connection from database.py.
- Reports include monthly income/expense/profit-loss totals.
- Reports include category-wise income and expense totals and charts.

Data migration note
- Existing records from the supplied database.db were copied into livestock.db.
- The supplied animals table had an extra gender column, which is not part of
  the team's agreed schema. The four animal records and all other records were
  preserved; the unsupported gender field was not copied.
- Keep the separately supplied pre-migration database backup if you need to
  refer to the old gender values.
