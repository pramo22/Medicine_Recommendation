# 💊 Medicine_Recommendation

This is a web-based drug recommendation system built with **Flask**. It supports user registration and login, and allows users to get drug recommendations based on their health condition using different algorithms:
- Content-Based Filtering
- Collaborative Filtering
- Hybrid Filtering

 ## Features

- 🧑‍💻 User Registration & Login (Flask-Login)
- 🔐 Authentication with user ID, password, email, and security key
- 📄 Drug recommendation form with dynamic input options
- 🤖 Support for multiple recommendation strategies
- 📊 Displays predicted sentiment, scores, and drug info

  ## Tech Stack

- **Backend**: Python, Flask, Flask-Login
- **Frontend**: HTML, Jinja2, Bootstrap 5, tailwind CSS
- **Recommendation Logic**: Python-based (Distil-Roberta /ML models assumed)
- **Storage**: In-memory (can be extended to SQLite)

---

## 📦 Project Structure

project/ │ ├── templates/ │ ├── login.html │ ├── register.html │ └── recommendation_form.html │ ├── static/ │ └── (Bootstrap CDN used for styling) │ ├── app.py └── README.md


## Installed Packages
  - Install Flask
    ```bash
       pip install flask
    
  - Install scikit-learn
    ``` bash
     pip install sklearn
    
  - Install Pandas
    ``` bash
     pip install pandas
    
  - Install Numpy
     ``` bash
     pip install numpy

  - Install Surprise
     ``` bash
     pip install scikit-surprise

## To run this project
   - 
      ``` bash
      py app.py

## Dataset Used
![drug_review_test.csv](https://github.com/pramo22/Medicine_Recommendation/blob/main/data/drug_review_test.csv)
<br>
![drug_review_with_sentiment.csv](https://github.com/pramo22/Medicine_Recommendation/blob/main/data/drug_reviews_with_sentiment.csv)
<br>
![content_scores.csv](https://github.com/pramo22/Medicine_Recommendation/blob/main/data/content_scores.csv)
<br>
![collaborative_scores.csv](https://github.com/pramo22/Medicine_Recommendation/blob/main/data/collaborative_scores.csv)
