from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, create_tables

app = Flask(__name__)

# Use the single shared database connection from database.py.
create_tables()


# =========================
# DASHBOARD
# =========================

@app.route("/")
def dashboard():

    connection = get_db_connection()

    # Count every animal in the herd using the quantity column.
    total_animals = connection.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM animals"
    ).fetchone()[0]

    total_income = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income"
    ).fetchone()[0]

    total_expenses = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    net_profit = total_income - total_expenses

    monthly_income = connection.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            SUM(amount) AS total
        FROM income
        GROUP BY substr(date, 1, 7)
        ORDER BY month
    """).fetchall()

    monthly_expenses = connection.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            SUM(amount) AS total
        FROM expenses
        GROUP BY substr(date, 1, 7)
        ORDER BY month
    """).fetchall()

    connection.close()

    # Combine income and expenses by month for the dashboard table
    income_by_month = {row["month"]: row["total"] for row in monthly_income}
    expenses_by_month = {row["month"]: row["total"] for row in monthly_expenses}

    all_months = sorted(set(income_by_month.keys()) | set(expenses_by_month.keys()))

    monthly_summary = []
    for month in all_months:
        income_amt = income_by_month.get(month, 0)
        expense_amt = expenses_by_month.get(month, 0)
        monthly_summary.append({
            "month": month,
            "income": income_amt,
            "expenses": expense_amt,
            "profit": income_amt - expense_amt
        })


    return render_template(
        "dashboard.html",
        total_animals=total_animals,
        total_income=total_income,
        total_expenses=total_expenses,
        net_profit=net_profit,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_summary=monthly_summary
    )

# =========================
# ANIMAL MANAGEMENT
# =========================

@app.route("/animals")
def animals():

    connection = get_db_connection()

    animal_list = connection.execute(
        "SELECT * FROM animals ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "animals.html",
        animals=animal_list
    )


@app.route("/animals/add", methods=["POST"])
def add_animal():

    animal_type = request.form["animal_type"]
    breed = request.form["breed"]
    age = request.form["age"]
    quantity = request.form["quantity"]

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO animals
        (animal_type, breed, age, quantity)
        VALUES (?, ?, ?, ?)
    """, (
        animal_type,
        breed,
        age,
        quantity
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("animals"))


@app.route("/animals/edit/<int:id>", methods=["GET", "POST"])
def edit_animal(id):

    connection = get_db_connection()

    if request.method == "POST":

        animal_type = request.form["animal_type"]
        breed = request.form["breed"]
        age = request.form["age"]
        quantity = request.form["quantity"]

        connection.execute("""
            UPDATE animals
            SET animal_type = ?,
                breed = ?,
                age = ?,
                quantity = ?
            WHERE id = ?
        """, (
            animal_type,
            breed,
            age,
            quantity,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("animals"))

    animal = connection.execute(
        "SELECT * FROM animals WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit_animal.html",
        animal=animal
    )


@app.route("/animals/delete/<int:id>", methods=["POST"])
def delete_animal(id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM animals WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("animals"))


# =========================
# INCOME MANAGEMENT
# =========================

@app.route("/income")
def income():

    connection = get_db_connection()

    records = connection.execute(
        "SELECT * FROM income ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "income.html",
        records=records
    )


@app.route("/income/add", methods=["POST"])
def add_income():

    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    description = request.form.get("description", "")

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO income
        (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (
        category,
        amount,
        date,
        description
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("income"))


@app.route("/income/edit/<int:id>", methods=["GET", "POST"])
def edit_income(id):

    connection = get_db_connection()

    if request.method == "POST":

        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form.get("description", "")

        connection.execute("""
            UPDATE income
            SET category = ?,
                amount = ?,
                date = ?,
                description = ?
            WHERE id = ?
        """, (
            category,
            amount,
            date,
            description,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("income"))

    record = connection.execute(
        "SELECT * FROM income WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit_income.html",
        record=record
    )


@app.route("/income/delete/<int:id>", methods=["GET", "POST"])
def delete_income(id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM income WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("income"))


# =========================
# EXPENSE MANAGEMENT
# =========================

@app.route("/expenses")
def expenses():

    connection = get_db_connection()

    expense_list = connection.execute(
        "SELECT * FROM expenses ORDER BY date DESC, id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "expenses.html",
        expenses=expense_list
    )


@app.route("/expenses/add", methods=["POST"])
def add_expense():

    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    description = request.form.get("description", "")

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO expenses
        (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (
        category,
        amount,
        date,
        description
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("expenses"))


@app.route("/expenses/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    connection = get_db_connection()

    if request.method == "POST":

        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form.get("description", "")

        connection.execute("""
            UPDATE expenses
            SET category = ?,
                amount = ?,
                date = ?,
                description = ?
            WHERE id = ?
        """, (
            category,
            amount,
            date,
            description,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("expenses"))

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit_expense.html",
        expense=expense
    )


@app.route("/expenses/delete/<int:id>", methods=["GET", "POST"])
def delete_expense(id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("expenses"))


# =========================
# REPORTS
# =========================

@app.route("/reports")
def reports():

    connection = get_db_connection()

    # Monthly income totals.
    income_rows = connection.execute("""
        SELECT substr(date, 1, 7) AS month, SUM(amount) AS total
        FROM income
        GROUP BY substr(date, 1, 7)
        ORDER BY month
    """).fetchall()

    # Monthly expense totals.
    expense_rows = connection.execute("""
        SELECT substr(date, 1, 7) AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY substr(date, 1, 7)
        ORDER BY month
    """).fetchall()

    # Category-wise summaries for both modules.
    income_categories = connection.execute("""
        SELECT category, SUM(amount) AS total
        FROM income
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    expense_categories = connection.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    connection.close()

    income_data = {row["month"]: row["total"] for row in income_rows}
    expense_data = {row["month"]: row["total"] for row in expense_rows}
    months = sorted(set(income_data) | set(expense_data))

    monthly_reports = []
    for month in months:
        month_income = income_data.get(month, 0) or 0
        month_expenses = expense_data.get(month, 0) or 0
        monthly_reports.append({
            "month": month,
            "income": month_income,
            "expenses": month_expenses,
            "profit_loss": month_income - month_expenses
        })

    total_income = sum(income_data.values())
    total_expenses = sum(expense_data.values())
    net_profit = total_income - total_expenses

    return render_template(
        "reports.html",
        monthly_reports=monthly_reports,
        total_income=total_income,
        total_expenses=total_expenses,
        net_profit=net_profit,
        income_categories=income_categories,
        expense_categories=expense_categories
    )

# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)