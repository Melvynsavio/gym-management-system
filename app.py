from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def connect_db():
    return sqlite3.connect("gym.db")


# ---------------------------
# LOGIN PAGE
# ---------------------------
@app.route('/')
def login():
    return render_template('login.html')


# ---------------------------
# HANDLE LOGIN (TEMP)
# ---------------------------
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        return redirect('/dashboard')
    else:
        return "Invalid Credentials"


# ---------------------------
# DASHBOARD
# ---------------------------
@app.route('/dashboard')
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()

    # Total Members
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    # Total Plans
    cursor.execute("SELECT COUNT(*) FROM plans")
    total_plans = cursor.fetchone()[0]

    # Total Revenue
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM payments")
    total_revenue = cursor.fetchone()[0]

    # Today's Attendance
    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE date = DATE('now')
    """)
    today_attendance = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        total_members=total_members,
        total_plans=total_plans,
        total_revenue=total_revenue,
        today_attendance=today_attendance
    )


# ---------------------------
# MEMBERS MODULE
# ---------------------------

# View Members
@app.route('/members')
def members():
    conn = connect_db()
    cursor = conn.cursor()

    # Members + Plan Name
    cursor.execute("""
        SELECT members.id, members.name, members.age, members.phone, plans.name
        FROM members
        LEFT JOIN plans ON members.plan_id = plans.id
    """)
    members = cursor.fetchall()

    # All Plans (for dropdown)
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()

    conn.close()

    return render_template('members.html', members=members, plans=plans)


# Add Member
@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form.get('name')
    age = request.form.get('age')
    phone = request.form.get('phone')
    plan_id = request.form.get('plan_id')   # SAFE VERSION

    if not plan_id:
        return "Error: Plan not selected"

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO members (name, age, phone, plan_id) VALUES (?, ?, ?, ?)",
        (name, age, phone, plan_id)
    )

    conn.commit()
    conn.close()

    return redirect('/members')


# Edit Member
@app.route('/edit_member/<int:id>')
def edit_member(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members WHERE id=?", (id,))
    member = cursor.fetchone()

    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()

    conn.close()

    return render_template('edit_member.html', member=member, plans=plans)


# Update Member
@app.route('/update_member/<int:id>', methods=['POST'])
def update_member(id):
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    plan_id = request.form['plan_id']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE members
        SET name=?, age=?, phone=?, plan_id=?
        WHERE id=?
    """, (name, age, phone, plan_id, id))

    conn.commit()
    conn.close()

    return redirect('/members')


# Delete Member
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM members WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/members')


# ---------------------------
# PLANS MODULE
# ---------------------------

# View Plans
@app.route('/plans')
def plans():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plans")
    data = cursor.fetchall()

    conn.close()

    return render_template('plans.html', plans=data)


# Add Plan
@app.route('/add_plan', methods=['POST'])
def add_plan():
    name = request.form['name']
    price = request.form['price']
    duration = request.form['duration']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO plans (name, price, duration) VALUES (?, ?, ?)",
        (name, price, duration)
    )

    conn.commit()
    conn.close()

    return redirect('/plans')


# Edit Plan
@app.route('/edit_plan/<int:id>')
def edit_plan(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plans WHERE id=?", (id,))
    plan = cursor.fetchone()

    conn.close()

    return render_template('edit_plan.html', plan=plan)


# Update Plan
@app.route('/update_plan/<int:id>', methods=['POST'])
def update_plan(id):
    name = request.form['name']
    price = request.form['price']
    duration = request.form['duration']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE plans
        SET name=?, price=?, duration=?
        WHERE id=?
    """, (name, price, duration, id))

    conn.commit()
    conn.close()

    return redirect('/plans')


# Delete Plan
@app.route('/delete_plan/<int:id>')
def delete_plan(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM plans WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/plans')


# Attendance and Payments modules would be similar in structure to the above
@app.route('/attendance')
def attendance():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance.id, members.name, attendance.date, attendance.status
        FROM attendance
        JOIN members ON attendance.member_id = members.id
    """)

    data = cursor.fetchall()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    return render_template('attendance.html', attendance=data, members=members)


# Mark Attendance
@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    member_id = request.form['member_id']
    status = request.form['status']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance (member_id, date, status)
        VALUES (?, DATE('now'), ?)
    """, (member_id, status))

    conn.commit()
    conn.close()

    return redirect('/attendance')


# ---------------------------
# VIEW PAYMENTS
# ---------------------------
@app.route('/payments')
def payments():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payments.id, members.name, payments.amount, payments.date
        FROM payments
        JOIN members ON payments.member_id = members.id
    """)

    data = cursor.fetchall()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    return render_template('payments.html', payments=data, members=members)


# Add Payment
@app.route('/add_payment', methods=['POST'])
def add_payment():
    member_id = request.form['member_id']
    amount = request.form['amount']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payments (member_id, amount, date)
        VALUES (?, ?, DATE('now'))
    """, (member_id, amount))

    conn.commit()
    conn.close()

    return redirect('/payments')

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)