from flask import Flask, request, flash, render_template, redirect, url_for, session
from models.content_based import recommend_with_positive_sentiment  # your recommendation logic
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from model import db, Users
from flask_bcrypt import Bcrypt
import os  # Import os to handle file operations
import pandas as pd  # Import pandas to handle DataFrames
from models.collaborative_based import recommend_svd,hybrid_model_recommendation

app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Required to use sessions

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_users(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('recommend'))

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            flash("Password do not match", "danger")
            return render_template('register.html')
        
        user_id=data['user_id']
        existing_user = Users.query.filter_by(user_id=user_id).first()

        if existing_user:
            flash("An account with this name already exists.", "danger")
            return render_template('register.html')
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = Users(user_id=data['user_id'],username=data['username'],email=data['email'], password=hashed_password, security_answer=data['security_answer'])
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can log in now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        user = Users.query.filter_by(user_id=data['user_id']).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username and password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out sucessfully", "success")
    return redirect('login')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # Ensure that the user is authenticated before accessing their user_id
    if current_user.is_authenticated:
        user_id = current_user.user_id  # Automatically get the logged-in user's user_id
    else:
        flash("You need to be logged in to make recommendations.", "danger")
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in
    
    if request.method == 'POST':
        # Collect form input
        method = request.form.get('method')
        condition = request.form.get('condition')
        review_text = request.form.get('review_text')

        if not user_id:
            return "User ID is required!", 400

        recommendations = []

        # Handle content-based recommendation method
        if method == "content":
            if not condition or not review_text:
                return "Condition and Review Text are required!", 400
            results_df = recommend_with_positive_sentiment(condition, review_text, user_id)
            results_df['review'] = results_df['review'].fillna("No review available").astype(str)
            recommendations = results_df.to_dict(orient="records")
        
        elif method == "collaborative":
            if not condition:
                return "Condition is required for collaborative filtering!", 400

            results_df = recommend_svd(user_id, condition, review_text)

            if results_df.empty:
                return "⚠️ No collaborative recommendations found. Try a different user or condition.", 404
            
            recommendations = results_df.to_dict(orient="records")

        elif method == "hybrid":
            if not condition or not review_text:
                return "Both Condition and Review Text are required for hybrid filtering!", 400

            # Step 1: Generate content-based scores and save to content_scores.csv
            content_results_df = recommend_with_positive_sentiment(condition, review_text, user_id)
            content_results_df.to_csv("data\\content_scores.csv", index=False)  # Save content scores
     
            # Step 2: Generate collaborative scores and save to collaborative_scores.csv
            collab_results_df = recommend_svd(user_id, condition, review_text)
            collab_results_df.to_csv("data\\collaborative_scores.csv", index=False)  # Save collaborative scores

            # Step 3: Generate hybrid recommendations using these saved scores
            results_df = hybrid_model_recommendation(user_id, condition)
            results_df['review'] = results_df['review'].fillna("No review available").astype(str)

            if results_df.empty:
                return "No hybrid recommendations found.", 404
            
     
            recommendations = results_df.to_dict(orient="records")
           

        # Save form data and recommendations to session
        session['form_data'] = {
            'recommendations': recommendations,
            'user_id': user_id,
            'method': method,
            'condition': condition,
            'review_text': review_text
        }

        # Redirect to GET route (avoids refresh warning)
        return redirect(url_for('recommend'))

    # Handle GET request (after redirect or page refresh)
    form_data = session.pop('form_data', None)  # Clear data after showing once

    if form_data:
        # Show recommendation results
        return render_template(
            "recommend_form.html",
            recommendations=form_data['recommendations'],
            user_id=form_data['user_id'],
            method=form_data['method'],
            condition=form_data['condition'],
            review_text=form_data['review_text']
        )
    else:
        # Show fresh form
        return render_template(
            "recommend_form.html",
            recommendations=[],
            user_id=user_id,
            method='',
            condition='',
            review_text=''
        )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
