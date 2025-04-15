from flask import Flask, request, render_template, redirect, url_for,flash
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host="127.0.0.1",       
    user="root",
    password="root",
    database="bus_booking"  
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/login', methods=['POST'])
def login_user():
    user_email = request.form['user-email']
    user_password = request.form['user-password']
    sql = "SELECT * FROM users WHERE user_email = %s AND user_password = %s"
    val = (user_email, user_password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        return redirect(url_for('home'))
    else:
        return "Invalid credentials"
    
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_user():
    user_name = request.form['user-name']
    user_email = request.form['user-email']
    user_number = request.form['user-number']
    user_password = request.form['user-password']

    sql = "INSERT INTO users (user_name, user_email,user_number, user_password) VALUES (%s, %s, %s, %s)"
    val = (user_name, user_email, user_number,user_password)
    cursor.execute(sql, val)
    db.commit()

    return redirect(url_for('login_page'))

@app.route('/bus-list', methods=['POST'])
def bus_route():
    bus_from = request.form['from-station']
    bus_to = request.form['to-station']
    travel_date = request.form['travel-date']


    sql = """
            SELECT b.bus_id, b.bus_name, b.from_place, b.to_place, b.departure_time, b.arrival_time, bf.fare_amount
            FROM bus b
            join bus_fare bf on b.bus_id = bf.bus_id
            WHERE b.from_place = %s AND b.to_place = %s AND b.travel_date = %s;
            """

    val = (bus_from, bus_to, travel_date)
    cursor.execute(sql, val)
    buses = cursor.fetchall()

    bus_list = []
    for bus in buses:
        bus_list.append({
            'id': bus[0],
            'name': bus[1],
            'from': bus[2],
            'to': bus[3],
            'departure_time': bus[4],
            'arrival_time': bus[5],
            'price': bus[6]
        })
    print(bus_list[0])

    return render_template('busroute.html', buses=bus_list)


@app.route('/book_ticket/<int:bus_id>', methods=['GET', 'POST'])
def book_ticket(bus_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        seats = request.form['seats']

        sql= "INSERT INTO tickets (bus_id, name, age, gender, seats) VALUES (%s, %s, %s, %s, %s)"
        val= (bus_id, name, age, gender, seats)
        cursor.execute(sql, val)
        db.commit()

        flash("Ticket booked successfully!", "success")
        return redirect(url_for('home'))

    return render_template('book_ticket.html', bus_id=bus_id)


if __name__ == '__main__':
    app.run(debug=True)
