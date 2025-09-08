from flask import render_template, request, redirect, url_for, flash, session, abort
from vpa import app, login_manager
from vpa.models import  User, db, Parking_Lot, Parking_Spot, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, date, timedelta
from functools import wraps
import requests
from sqlalchemy import cast, String, func, or_

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


login_manager.login_view = 'login_view'  # Where to redirect users who aren't logged in


# Load user function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def is_admin():
    return current_user.is_authenticated and current_user.is_admin


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return redirect(url_for('login_view'))


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if both username and password are provided
        if not username or not password:
            flash('Please fill out all the mandatory fields', 'warning')
            return redirect(url_for('login_view'))
        
        # Fetch the user from the database by username
        user = User.query.filter_by(username=username).first()

        
        # Check if user exists
        if not user:
            flash('The username provided is not registered with us.', 'danger')
            return redirect(url_for('login_view'))
        
        # Check if the password is correct
        if not check_password_hash(user.passhash, password):
            flash('Incorrect password.', 'danger')
            return redirect(url_for('login_view'))

        # Log in the user with Flask-Login
        login_user(user)
        flash('Login successful', "success")

        if user.is_admin == 1:
            return redirect(url_for('admin_dash'))
        else:
            return redirect(url_for('user_dash', id=user.id))

    # Render the login template if it's a GET request
    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()     #logs out the user
    return redirect(url_for('login_view'))    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        # Convert string to date object
    
        # Validate inputs
        if not all([username, password, fullname, email]):
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email Address is already registered.', 'danger')
            return redirect(url_for('register'))

        # Hash password and create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            passhash=password_hash,
            fullname=fullname,
            email=email
        )

        db.session.add(new_user)
        try:
           db.session.commit()
           flash('Registration successful! Please log in.', 'success')
           return redirect(url_for('login_view'))
        except Exception as e:
           db.session.rollback()
           flash("An error occurred while saving the user. Please try again.")
           print(f"Database error: {e}")
        return redirect(url_for('login_view'))
    

    return render_template('auth/register.html')


##############admin methods###########################################################################################

@app.route('/admin/dashboard', methods = ['GET', 'POST'])
@login_required
@admin_required
def admin_dash():
    if request.method == 'GET':
        lots = Parking_Lot.query.all()
        
        return render_template('admin_dash.html', lots=lots)
    

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required  
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # check if the user has existing reservations which are occupied
    if user.reservation:
        for reservation in user.reservation:
            if reservation.leaving_timestamp is None:
                # If the reservation is still active, do not allow deletion     
               flash(f"Cannot delete user '{user.username}' as they have existing active reservations.", "danger")
               return redirect(url_for('admin_dash'))  

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' has been deleted.", "success")
    return redirect(url_for('admin_dash'))  # Change as per your layout


#############Get parking history for all reservations##########################################################
@app.route('/parking/summary', methods=['GET']) 
@login_required 
@admin_required
def parking_history():  
    # Get all reservations with valid leaving timestamps
    reservations = Reservation.query.filter(Reservation.leaving_timestamp.isnot(None)).order_by(Reservation.parking_timestamp).all()

    if not reservations:
        labels = ["No History"]
        durations = [0]
    else:
        labels = [f"#{r.id}" for r in reservations]
        durations = [
            round((r.leaving_timestamp - r.parking_timestamp).total_seconds() / 60, 2)  # in minutes
            for r in reservations
        ]

    chart = create_bar_chart(
        labels,
        durations,
        title="Parking Duration per Reservation",
        xlabel="Reservation",
        ylabel="Duration (minutes)"
    )

    return render_template("parking_history.html", chart=chart, reservations=reservations)



@app.route('/add/lot', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_lot():
    if request.method == 'POST':

        prime_location_name = request.form.get('prime_location_name')
        price = request.form.get('price')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        maximum_number_of_spots = request.form.get('maximum_number_of_spots')


        new_lot = Parking_Lot(prime_location_name=prime_location_name, price=price, address=address, pin_code=pin_code, maximum_number_of_spots=maximum_number_of_spots)
        db.session.add(new_lot)
        db.session.commit()

        flash("Parking Lot added successfully!", "success")

        for spot in range(int(maximum_number_of_spots)):
            new_spot = Parking_Spot(lot_id=new_lot.id, status='A')
            db.session.add(new_spot)
        db.session.commit()

        return redirect(url_for('admin_dash'))
    

@app.route('/edit/lot/<int:id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_lot(id):
    if request.method == 'POST':
        url = f'http://localhost:5000/lots/{id}'

        prime_location_name = request.form.get('prime_location_name')
        price = request.form.get('price')
        address = request.form.get('address')       
        pin_code = request.form.get('pin_code')
        maximum_number_of_spots = request.form.get('maximum_number_of_spots')
        # Check if any field is provided
        if not (prime_location_name or price or address or pin_code or maximum_number_of_spots):
            flash("No changes were submitted.", 'info') 
            return redirect(url_for('admin_dash'))
        # Prepare data for update
         

        data = {}
        if prime_location_name:
            data['prime_location_name'] = prime_location_name
        if price:
            data['price'] = price
        if address: 
            data['address'] = address
        if pin_code:
            data['pin_code'] = pin_code
        if maximum_number_of_spots:
            data['maximum_number_of_spots'] = maximum_number_of_spots
        
        # Ensure data is not empty      
        if not data:
            flash("No changes were submitted.", 'info') 
            return redirect(url_for('admin_dash'))
        

        response = requests.put(url, json=data)
        
        try:
            result = response.json()
            flash(result.get('message', 'Parking Lot Details are Updated.'), "success")
            return redirect(url_for('admin_dash'))
        except requests.exceptions.JSONDecodeError:
            flash("Failed to update lot: No response from server.", "danger")
            return redirect(url_for('admin_dash'))

    lot = Parking_Lot.query.get(id)    
    return render_template('edit_lot.html', lot=lot)


@app.route('/remove/lot/<int:id>', methods = ['POST'])
@login_required
@admin_required
def delete_lot(id):
    if request.method == 'POST':
        url = f'http://localhost:5000/lots/{id}'

    try:
        response = requests.delete(url)
        result = response.json()
        
        if response.status_code == 200:
            flash(result.get('message', 'Parking Lot deleted successfully.'), 'success')
        else:
            flash(result.get('message', 'Failed to delete Parking Lot.'), 'danger')

    except requests.exceptions.RequestException as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"API error: {e}")

    return redirect(url_for('admin_dash'))

    

@app.route('/add/spot', methods = ['POST'])
@login_required
@admin_required
def add_spot():
    if request.method == 'POST':
        lot_id = request.form.get('lot_id')

        lot = Parking_Lot.query.get(lot_id)

        status = 'A'  #  'A' means available , O means occupied

        print(len(lot.spots), lot.maximum_number_of_spots)

        if not lot:
            flash("Parking Lot not found.", "danger")
            return redirect(url_for('admin_dash'))
        
        # Check if the maximum number of spots has been reached
        if len(lot.spots) >= lot.maximum_number_of_spots:
            
            flash("Maximum number of spots reached for this lot.", "danger")
            return redirect(url_for('admin_dash'))
        # Create a new parking spot

        data = {
            'lot_id': lot_id,
            'status': status
        }
        
         
        url = 'http://localhost:5000/spots'

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

            flash("spot added successfully!", "success")
            return redirect(url_for('admin_dash'))

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            flash("Failed to connect to API.", "danger")
        except ValueError:
            flash("Invalid response from server.", "danger")
        except Exception as e:
            flash(f"Unexpected error: {e}", "danger")
            

        return redirect(url_for('admin_dash'))

    
@app.route('/edit/spot/<int:spot_id>', methods=['POST'])
@login_required
@admin_required
def edit_spot(spot_id):
    spot = Parking_Spot.query.get(spot_id)

    if not spot:
        flash("spot not found.", "danger")
        return redirect(url_for('admin_dash'))


    status = 'O' if spot.status == 'A' else 'A' # Toggle status between 'A' (available) and 'O' (occupied)

    if request.method == 'POST':

      
        url = f'http://localhost:5000/spots/{spot_id}'

        try:
            response = requests.patch(url, json={'status': status})
            response.raise_for_status()  # Raise an error for bad responses
            response_data = response.json()

            if response.status_code == 200:
                flash("spot updated successfully!", "success")
            else:
                flash(response_data.get("message", "Update failed."), "danger")
        except Exception as e:
            flash("Error communicating with API.", "danger")
            print(f"API error: {e}")

        return redirect(url_for('admin_dash'))


@app.route('/remove/spot/<int:spot_id>', methods = ['POST'])
@login_required
@admin_required
def delete_spot(spot_id):
    if request.method == 'POST':
        url = f'http://localhost:5000/spots/{spot_id}'

    try:
        response = requests.delete(url)
        result = response.json()
        
        if response.status_code == 200:
            flash(result.get('message', 'spot deleted successfully.'), 'success')
        else:
            flash(result.get('message', 'Failed to delete spot.'), 'danger')

    except requests.exceptions.RequestException as e:

        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"API error: {e}")

    return redirect(url_for('admin_dash'))


@app.route('/users')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/collect_payment/<int:spot_id>', methods=['POST'])
@login_required
@admin_required
def collect_payment(spot_id):
    reservations = Parking_Spot.query.get_or_404(spot_id).reservation
    active_reservation = None

    for reservation in reservations:
        if reservation.leaving_timestamp is None:
            # If the reservation is still active, proceed to collect payment
            active_reservation = reservation
            break


    # Calculate leaving timestamp (now)
    leaving_timestamp = datetime.now()

    # Calculate duration in hours
    duration = (leaving_timestamp - active_reservation.parking_timestamp).total_seconds() / 3600

    # Round up and calculate payment (e.g., $10/hour)
    hourly_rate = active_reservation.spot.lot.price  # Assuming price is per hour
    if duration < 1:
        duration = 1

    # Round duration to the nearest hour
    amount_due = round(duration * hourly_rate, 2)

    

    return render_template("collect_payment_admin_modal.html", reservation=active_reservation, leaving_timestamp=leaving_timestamp, amount_due=amount_due)


@app.route('/release/spot/admin/<int:reservation_id>', methods=['POST'])
@login_required
@admin_required
def release_spot_by_admin(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    amount_paid = request.form.get('amount_paid')

    try: 
        if reservation.leaving_timestamp is None:
            reservation.leaving_timestamp = datetime.now()
            reservation.spot.status = 'A'  # Mark the spot as available 
            reservation.amount_paid = amount_paid             
            db.session.commit()
            flash(f"Spot released. ₹{amount_paid} collected.", "success")

    except Exception as e:

        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"API error: {e}")

    return redirect(url_for('admin_dash'))


@app.route('/admin/search')
@admin_required
@login_required
def admin_search():

    filter_by = request.args.get('filter')
    query = request.args.get('query')
     
    # Validate inputs
    if not filter_by or not query:
        flash("Please select a filter and enter a search term.", "warning")
        return redirect(url_for('index'))  # or another fallback page

    results = []

    # Apply filter logic
    if filter_by == 'user':
        results = User.query.filter(User.fullname.ilike(f'%{query}%')).all()

    elif filter_by == 'lot':
       results = Parking_Lot.query.filter(
                        or_(
                            Parking_Lot.pin_code.ilike(f'%{query}%'),
                            Parking_Lot.address.ilike(f'%{query}%'),
                            Parking_Lot.prime_location_name.ilike(f'%{query}%'
                        ))
                    ).all()

    
    else:
        flash("Invalid filter selected.", "danger")
        return redirect(url_for('index'))
     
    return render_template('search_results_admin.html', results=results, filter=filter_by, query=query)


    


###############See user parking history along with status in a table for admin##########################################################
@app.route('/see_user_history/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def see_user_history(user_id):  
        # Get all reservations for the user
        user = User.query.get(user_id)
        print(user.reservation)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('admin_dash'))

        reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp).all()  
        if not reservations:
            flash("No parking history found for this user.", "info")
            return redirect(url_for('user_list'))
        # Prepare data for the table
        history_data = []
        for reservation in reservations:
            duration = None
            if reservation.leaving_timestamp:
                duration = round((reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 60, 2)
            history_data.append({
                'reservation_id': reservation.id,
                'vehicle_number': reservation.vehicle_number,
                'parking_timestamp': reservation.parking_timestamp,
                'leaving_timestamp': reservation.leaving_timestamp,
                'duration': duration,
                'spot_status': reservation.spot.status
            })
        return render_template('user_parking_history_admin.html', user=user, history_data=history_data)   
  
############################################User Methods################################################


@app.route('/user/dashboard/<int:id>', methods=['GET', 'POST'])
@login_required     
@user_required
def user_dash(id):
    if request.method == 'GET':
        user = User.query.get(id)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('home'))

        # Get all reservations for the user
        reservations = Reservation.query.filter_by(user_id=id).all()
        
        # Get all parking spots for the user
        spots = Parking_Spot.query.all()

        return render_template('user_dash.html', user=user, reservations=reservations, spots=spots)


@app.route('/user/search')
@user_required
@login_required
def user_search():

    filter_by = request.args.get('filter')
    query = request.args.get('query')

    # Validate inputs
    if not filter_by or not query:
        flash("Please select a filter and enter a search term.", "warning")
        return redirect(url_for('index'))  # or another fallback page

    results = []

    # Apply filter logic
    if filter_by == 'location':
        results = Parking_Lot.query.filter(
                        or_(
                            Parking_Lot.address.ilike(f'%{query}%'),
                            Parking_Lot.prime_location_name.ilike(f'%{query}%'
                        ))
                    ).all()

    elif filter_by == 'pin_code':
        results = Parking_Lot.query.filter(Parking_Lot.pin_code.ilike(f'%{query}%')).all()

    
    else:
        flash("Invalid filter selected.", "danger")
        return redirect(url_for('index'))
     
    return render_template('search_results.html', results=results, filter=filter_by, query=query)


@app.route('/user/book/<int:lot_id>', methods=['POST'])
@login_required
@user_required
def book_spot(lot_id):
    lot = Parking_Lot.query.get(lot_id)
    if not lot:
        flash("Parking Lot not found.", "danger")
        return redirect(url_for('user_dash', id=current_user.id))

    # Check if the lot has available spots
    available_spots = [spot for spot in lot.spots if spot.status == 'A']
    if not available_spots:
        flash("No available spots in this lot.", "warning")
        return redirect(url_for('user_dash', id=current_user.id))
    
    # Get the first available spot
    spot = available_spots[0]
   
    
    # Check if the vehicle number is provided
    vehicle_number = request.form.get('vehicle_number')
    if not vehicle_number:
        flash("Please provide your vehicle number.", "warning")
        return redirect(url_for('user_dash', id=current_user.id))
    
    # Check if the vehicle number is already booked
    existing_reservation = Reservation.query.filter_by(vehicle_number=vehicle_number).first()
    if existing_reservation:
        if existing_reservation.leaving_timestamp is None:
            # If the vehicle number is already booked and the reservation is still active
            flash("This vehicle number is already booked for another reservation.", "warning")
            return redirect(url_for('user_dash', id=current_user.id))
      


    # Create a new reservation
    reservation = Reservation(
        spot_id=spot.id,
        vehicle_number=request.form.get('vehicle_number'),
        user_id=current_user.id,
        parking_timestamp=datetime.now()
    )

    db.session.add(reservation)
    spot.status = 'O'
    db.session.commit() 
    flash("Spot booked successfully!", "success")

    return redirect(url_for('user_dash', id=current_user.id))


@app.route('/release/spot/<int:reservation_id>', methods=['POST'])
@login_required
@user_required
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != current_user.id:
        abort(403)

    amount_paid = request.form.get('amount_paid')

    try: 
        if reservation.leaving_timestamp is None:
            reservation.leaving_timestamp = datetime.now()
            reservation.spot.status = 'A'  # Mark the spot as available 
            reservation.amount_paid = amount_paid             
            db.session.commit()
            flash(f"Spot released. ₹{amount_paid} collected.", "success")

    except Exception as e:

        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"API error: {e}")



    return redirect(url_for('user_dash', id=current_user.id))


@app.route('/give_payment/<int:reservation_id>', methods=['POST'])
@login_required
@user_required
def give_payment(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    # Calculate leaving timestamp (now)
    leaving_timestamp = datetime.now()

    # Calculate duration in hours
    duration = (leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600

    # Round up and calculate payment (e.g., $10/hour)
    hourly_rate = reservation.spot.lot.price  # Assuming price is per hour
    if duration < 1:
        duration = 1

    # Round duration to the nearest hour
    amount_due = round(duration * hourly_rate, 2)

    

    return render_template("confirm_payment_modal.html", reservation=reservation, leaving_timestamp=leaving_timestamp, amount_due=amount_due)


###############################################Parking History for User Dashboard############################################################

@app.route('/user/parking_history/<int:id>')
@login_required
@user_required
def user_parking_history(id):
    # Get all reservations with valid leaving timestamps
    reservations = Reservation.query.filter_by(user_id=current_user.id).filter(
        Reservation.leaving_timestamp.isnot(None)
    ).order_by(Reservation.parking_timestamp).all()

    if not reservations:
        labels = ["No History"]
        durations = [0]
    else:
        labels = [f"#{r.id}" for r in reservations]
        durations = [
            round((r.leaving_timestamp - r.parking_timestamp).total_seconds() / 60, 2)  # in minutes
            for r in reservations
        ]

    chart = create_bar_chart(
        labels,
        durations,
        title="Parking Duration per Reservation",
        xlabel="Reservation",
        ylabel="Duration (minutes)"
    )

    return render_template("user_parking_history.html", chart=chart, id=id)


###############################################create bar chart for parking history###############################################

def create_bar_chart(labels, values, title, xlabel, ylabel):
    import matplotlib
    matplotlib.use('Agg')  # ensures no Tkinter GUI issues on server
    import matplotlib.pyplot as plt
    import io, base64

    fig, ax = plt.subplots(figsize=(8, 4))  # optional: adjust size

    ax.bar(labels, values, color='skyblue', edgecolor='black', width = 0.2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)  # optional: y starts at 0

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)

    return f"data:image/png;base64,{encoded}"

