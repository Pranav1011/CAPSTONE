from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime  # For generating timestamps, if needed
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VIT'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)),"Database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Email(db.Model):
    __tablename__ = "user_email"
    email_id = db.Column(db.Text, nullable = False, primary_key = True)
    cus_name = db.Column(db.Text, nullable = False)
    title = db.Column(db.Text, nullable = False)
    email_content = db.Column(db.Text, nullable = False)
    sentiment = db.Column(db.Text)
    category = db.Column(db.Text)
    summary = db.Column(db.Text)
    auto_reply = db.Column(db.Text)
    date = db.Column(db.Text)



emails = []

@app.route('/')
def index():
    emails = Email.query.all()
    return render_template('Main.html', emails = emails)


@app.route('/email/<email_id>')
#@app.route('/email')
def email_detail(email_id):
    '''email = next((email for email in emails if email['id'] == email_id), None)
    if email is not None:
        return render_template('email_detail.html', email=email)
    else:
        return "Email not found", 404
    '''
    emails = Email.query.all()
    for email in emails:
        if email.email_id == email_id:
            return render_template('email_detail.html', email=email)
    else:
        return "Email not found", 404
    
    
@app.route('/add_query', methods=['GET', 'POST'])
def add_query():
    if request.method == 'POST':
        customer_email = request.form['customerEmail']
        customer_name = request.form['customerName']
        email_title = request.form['emailTitle']
        email_content = request.form['emailContent']
        sent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # or use request.form['sentTime'] if provided by user

        # email_id = len(emails)  # Simple ID based on list length
        ''' emails.append({
            'id': email_id,
            'sender_name': customer_name,
            'email_title': email_title,
            'email_content': email_content,
            'timestamp': sent_time
        })
        '''
        new_email = Email(email_id = customer_email,
    cus_name = customer_name,
    title = email_title,
    email_content = email_content,
    date = sent_time)
        db.session.add(new_email)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('add_query.html')
    
@app.route('/delete_email/<email_id>', methods=['POST'])
def delete_email(email_id):
    email_to_delete = Email.query.filter_by(email_id=email_id).first()
    if email_to_delete:
        db.session.delete(email_to_delete)
        db.session.commit()
        flash('Email deleted successfully.')
    else:
        flash('Email not found.')
    return redirect(url_for('index'))

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    email_content = data['email_content']
    API_URL = "https://api-inference.huggingface.co/models/Pranav-10/Sentiment_analysis"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
	
    sentiment_label = model_response['label']  # Adjust based on actual model response structure
    
    # Convert model labels to human-readable sentiment
    if sentiment_label == 'LABEL_1':
        sentiment = 'Positive'
    elif sentiment_label == 'LABEL_0':
        sentiment = 'Negative'
    else:
        sentiment = 'Unknown'
    
    return jsonify({"sentiment": sentiment})
@app.route('/settings')
def settings():
    # Add any necessary data retrieval or processing here if needed
    return render_template('settings.html')



if __name__ == '__main__':
    app.run(debug=True)
