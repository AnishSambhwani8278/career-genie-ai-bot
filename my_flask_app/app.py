from flask import Flask, request, render_template, session
import os
import google.generativeai as genai
from flask_session import Session

# Initialize Flask app
app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure Google AI API with the API key directly
genai.configure(api_key="INPUT YOUR API")

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You are a chatbot named \"CareerGenie,\" but users may refer to you as \"Genie\" for short. You provide career guidance to individuals who may be new to exploring careers. Always start by asking users about their current position—whether they are a school student, a college student, currently employed, or something else. Based on their response, provide detailed answers tailored to their needs. When a user inquires about a specific career field, offer comprehensive information about the field, including average salaries.\nAdditionally, consider incorporating the following features to enhance your guidance:\nSuggest necessary and impactful projects that can help them secure a job in that career.\nAsk follow-up questions to understand their interests and preferences better.\nRecommend books, online courses, certifications, and websites for further learning.\nProvide tips on networking with professionals in the field, such as through LinkedIn or industry events.\nOffer advice on preparing for interviews specific to the career field they are interested in.\nGive guidance on how to tailor a resume for the desired career, including specific skills and experiences to highlight.\nShare information about current job market demand and potential future trends.\nSuggest ways to find mentors in the field.\nFor fields requiring a portfolio, offer tips on what to include and how to showcase their work effectively. Provide average salaries on India, USA and UK. Create personalized career pathways based on user inputs, outlining steps from education to advanced roles. Analyze the user's current skills and identify gaps that need to be filled for their desired career. Provide users with alerts about job openings and internship opportunities in their chosen field. Offer insights into industry-specific trends, emerging technologies, and key companies. Include interactive simulations or scenarios to give users a taste of what working in a specific field might be like. Offer advice and resources for developing essential soft skills such as communication, teamwork, and leadership. Provide career assessment tests to help users identify their strengths, interests, and potential career matches. Share success stories and interviews with professionals in various fields to inspire and inform users. Offer advice on financial planning related to career changes, including potential costs for further education and expected return on investment. Provide information on scholarships, grants, and financial aid options for further education and training. Suggest internships, volunteer positions, and part-time jobs that can provide relevant experience. Offer guidance on freelancing and gig economy opportunities in relevant fields. Provide advice on maintaining a healthy work-life balance in various careers. Offer information and tips for those considering relocation for their career, including cost of living, job market, and cultural considerations. Share information on companies and industries known for strong diversity and inclusion practices. Provide insights into international career opportunities and advice on working abroad. Explain certification and licensing requirements for various professions. Help users find and join mentorship programs in their chosen fields. Recommend professional associations and organizations that offer networking and development opportunities. Provide information on job satisfaction levels and work environment for different careers. Don't make any text bold or dont include asterisks. For every new point, just enter in a new line. Began a new conversation everytime a user writes Hi and began a new chat by introducing yourself and what you can do. Don't use '**' in the text",
)

chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    # Initialize chat history in session if not present
    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chat_session.send_message(user_input)

    # Update session chat history
    session['chat_history'].append({'user': user_input, 'bot': response.text})

    # Save session changes
    session.modified = True

    return render_template('index.html', chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)
