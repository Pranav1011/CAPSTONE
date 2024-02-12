from flask import Flask, render_template, request, redirect, url_for, request, jsonify
import datetime  # For generating timestamps, if needed

app = Flask(__name__)

# Example email data store - this could be replaced with a database
emails = []

@app.route('/')
def index():
    return render_template('Main.html', emails=emails)

@app.route('/email/<int:email_id>')
def email_detail(email_id):
    email = next((email for email in emails if email['id'] == email_id), None)
    if email is not None:
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

        email_id = len(emails)  # Simple ID based on list length
        emails.append({
            'id': email_id,
            'sender_name': customer_name,
            'email_title': email_title,
            'email_content': email_content,
            'timestamp': sent_time
        })

        return redirect(url_for('index'))
    else:
        return render_template('add_query.html')
    
@app.route('/delete_email/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    print(f"Attempting to delete email with ID: {email_id}")  # Debugging line
    global emails
    emails = [email for email in emails if email['id'] != email_id]
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

if __name__ == '__main__':
    app.run(debug=True)
