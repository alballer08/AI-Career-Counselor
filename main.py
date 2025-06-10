import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in the .env file.")

genai.configure(api_key=API_KEY)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Store conversations in memory (in production, use a database)
conversations = {}

# Career counselor system prompt
CAREER_COUNSELOR_PROMPT = """
You are a professional AI Career Counselor called Star with expertise in:
- Career guidance and planning
- Resume and interview advice
- Industry trends and job market insights
- Skills development recommendations
- Career transition strategies
- Professional networking guidance
- Salary negotiation tips
- Work-life balance advice

Always provide helpful, supportive, and actionable career advice. Ask clarifying questions to better understand the user's situation, goals, and background. Be encouraging while remaining realistic about career prospects and challenges.

Start conversations by introducing yourself and asking how you can help with their career journey today.
"""

def get_or_create_conversation(session_id):
    """Get existing conversation or create a new one"""
    if session_id not in conversations:
        conversation = model.start_chat()
        # Initialize with career counselor prompt
        conversation.send_message(CAREER_COUNSELOR_PROMPT)
        conversations[session_id] = {
            'chat': conversation,
            'messages': [],
            'created_at': datetime.now()
        }
    return conversations[session_id]

@app.route('/')
def index():
    """Main page"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create conversation
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(uuid.uuid4())
            session_id = session['session_id']
        
        conversation_data = get_or_create_conversation(session_id)
        conversation = conversation_data['chat']
        
        # Send message and get response
        response = conversation.send_message(user_message)
        ai_response = response.text
        
        # Store messages
        conversation_data['messages'].append({
            'user': user_message,
            'ai': ai_response,
            'timestamp': datetime.now()
        })
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/history')
def get_history():
    """Get chat history for current session"""
    session_id = session.get('session_id')
    if session_id and session_id in conversations:
        messages = conversations[session_id]['messages']
        return jsonify({
            'messages': [
                {
                    'user': msg['user'],
                    'ai': msg['ai'],
                    'timestamp': msg['timestamp'].isoformat()
                } for msg in messages
            ]
        })
    return jsonify({'messages': []})

@app.route('/api/clear')
def clear_chat():
    """Clear current chat session"""
    session_id = session.get('session_id')
    if session_id and session_id in conversations:
        del conversations[session_id]
    return jsonify({'status': 'cleared'})


if __name__ == "__main__":
    print("🎯 Starting AI Career Counselor...")
    print("📝 Make sure to set your API_KEY in the .env file")
    print("🌐 Visit http://localhost:3000 to start counseling!")
    app.run(debug=True, host='0.0.0.0', port=3000)