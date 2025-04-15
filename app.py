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

@app.route('/login', methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
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
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup_user():
    if request.method == 'POST':
        user_name = request.form['user-name']
        user_email = request.form['user-email']
        user_number = request.form['user-number']
        user_password = request.form['user-password']

        sql = "INSERT INTO users (user_name, user_email,user_number, user_password) VALUES (%s, %s, %s, %s)"
        val = (user_name, user_email, user_number,user_password)
        cursor.execute(sql, val)
        db.commit()

        return redirect(url_for('login_user'))
    elif request.method == 'GET':
        return render_template('signup.html')

@app.route('/bus-route', methods=['GET','POST'])
def bus_route():
    if request.method == 'GET':
        return render_template('bookticket.html')
    elif request.method == 'POST':
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
        print(bus_list)
        return render_template('busroute.html', buses=bus_list)

@app.route('/ticket-confirmation', methods=['GET'])
def ticket_confirmation():
    return render_template('ticket_confirmation.html')

@app.route('/book_ticket/<int:bus_id>', methods=['GET','POST'])
def book_ticket(bus_id):
    if request.method == 'GET':
        sql = "SELECT * FROM bus WHERE bus_id = %s"
        val = (bus_id,)
        cursor.execute(sql, val)
        bus = cursor.fetchone()

        bus_dict = {
            'bus_id': bus[0],
            'bus_name': bus[1],  
            'from_place': bus[2],
            'to_place': bus[3],
            'departure_time': bus[4],
            'arrival_time': bus[5],
            'price': bus[6]
        }
        print(bus_dict)
        return render_template('bookticket.html', bus=bus_dict)
    elif request.method == 'POST':
        bus_id = request.form['bus-id']
        user_name = request.form['user-name']
        user_email = request.form['user-email']
        user_number = request.form['user-number']
        travel_date = request.form['travel-date']
        adult_count = request.form['adult-count']
        child_count = request.form['child-count']
        infant_count = request.form['infant-count']

        sql = "INSERT INTO booking (bus_id, user_name, user_email, user_number, travel_date, adult_count, child_count, infant_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %d)"
        val = (bus_id, user_name, user_email, user_number, travel_date, adult_count, child_count, infant_count)
        cursor.execute(sql, val)
        db.commit()

        return redirect(url_for('ticket_confirmation'))

@app.route('/passanger-info', methods=['GET'])
def passanger_info():
    name = request.form['user-name']
    age = request.form['user-age']
    gender = request.form['user-gender']
    seats = request.form['seat-count']



if __name__ == '__main__':
    app.run(debug=True)
