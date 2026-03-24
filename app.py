# Imports
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database import db, init_db, User
from forms import RegistrationForm, LoginForm
from security import hash_password, verify_password, add_security_headers
from datetime import datetime, timedelta

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data
        
        # Duplicate check
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('register.html', form=form)
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use another or login.', 'danger')
            return render_template('register.html', form=form)
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            failed_login_attempts=0,
            locked_until=None,
            created_at=datetime.utcnow(),
            last_login=None
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('✅ Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Registration failed: {type(e).__name__}")
            flash('An error occurred during registration. Please try again later.', 'danger')
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            username_or_email = form.username.data.strip()
            password = form.password.data
            
            # User lookup
            user = User.query.filter(
                (User.username == username_or_email) | 
                (User.email == username_or_email.lower())
            ).first()
            
            # Lockout check
            if user and user.is_locked():
                remaining_time = (user.locked_until - datetime.utcnow()).total_seconds()
                remaining_minutes = int(remaining_time / 60) + 1
                print(f"⚠️ Locked account: {username_or_email} (unlocks in {int(remaining_time)}s)")
                flash(f'🔒 Too many login attempts detected. Please try again after {remaining_minutes} minutes.', 'danger')
                return render_template('login.html', form=form)
            
            # Password verification
            password_valid = False
            if user:
                password_valid = verify_password(user.password_hash, password)
            else:
                verify_password('pbkdf2:sha256:600000$dummy$hash', password)
                password_valid = False
            
            if user and password_valid:
                # Success
                user.failed_login_attempts = 0
                user.locked_until = None
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Create session
                session['user_id'] = user.id
                session['username'] = user.username
                session.permanent = True
                
                flash(f'✅ Welcome back, {user.username}!', 'success')
                print(f"✅ Successful login: {user.username} from {request.remote_addr}")
                return redirect(url_for('dashboard'))
            else:
                # Failure
                if user:
                    user.failed_login_attempts += 1
                    max_attempts = app.config.get('MAX_LOGIN_ATTEMPTS', 5)
                    
                    if user.failed_login_attempts >= max_attempts:
                        lockout_duration = app.config.get('LOCKOUT_DURATION', 15)
                        user.locked_until = datetime.utcnow() + timedelta(minutes=lockout_duration)
                        print(f"🔒 Account locked: {user.username} ({user.failed_login_attempts} attempts)")
                        flash(f'🔒 Too many login attempts detected. Account locked for {lockout_duration} minutes.', 'danger')
                    else:
                        remaining = max_attempts - user.failed_login_attempts
                        print(f"⚠️ Failed login {user.failed_login_attempts}/{max_attempts} for {user.username}")
                        flash('Invalid username or password. Please try again.', 'danger')
                    
                    db.session.commit()
                else:
                    print(f"⚠️ Login for non-existent user: {username_or_email}")
                    flash('Invalid username or password. Please try again.', 'danger')
                
                return render_template('login.html', form=form)
        
        return render_template('login.html', form=form)
    except Exception as e:
        print(f"[ERROR] Login error: {type(e).__name__}")
        try:
            db.session.rollback()
        except:
            pass
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return render_template('login.html', form=LoginForm())


# Dashboard
@app.route('/dashboard')
def dashboard():
    try:
        if 'user_id' not in session:
            flash('Please login to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        
        if not user:
            session.clear()
            flash('Session expired. Please login again.', 'warning')
            return redirect(url_for('login'))
        
        return render_template('dashboard.html',
                             username=user.username,
                             email=user.email,
                             created_at=user.created_at.strftime('%B %d, %Y'))
    except Exception as e:
        print(f"[ERROR] Dashboard error: {type(e).__name__}")
        try:
            session.clear()
        except:
            pass
        flash('An error occurred. Please login again.', 'danger')
        return redirect(url_for('login'))


# Logout
@app.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'✅ You have been logged out successfully, {username}!', 'success')
    return redirect(url_for('login'))


# Security headers
@app.after_request
def apply_security_headers(response):
    return add_security_headers(response)

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
