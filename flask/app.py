from flask import Flask, request, jsonify, redirect, url_for, session
import time
import requests
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "your-secret-key"  # 세션 암호화를 위한 고유한 키로 변경 필요
request_history = {}
session_store = {}
RECAPTCHA_SECRET = "your-recaptcha-secret-key"  # Google reCAPTCHA Secret Key로 교체

@app.route('/memberships', methods=['GET'])
def check_membership():
    result = {}
    headless_score = 0

    # 탐지 로직
    user_agent = request.headers.get('User-Agent')
    if user_agent and 'HeadlessChrome' in user_agent: 
        headless_score += 30
    if request.args.get('webdriver', 'false').lower() == 'true': 
        headless_score += 20
    if not request.args.get('canvasFingerprint'): 
        headless_score += 15
    outer_height = request.args.get('outerHeight', type=int)
    outer_width = request.args.get('outerWidth', type=int)
    if outer_height == 0 or outer_width == 0: 
        headless_score += 15
    webgl_info = request.args.get('webglInfo')
    if not webgl_info or 'undefined' in webgl_info or 'null' in webgl_info: 
        headless_score += 15
    timing_start = request.args.get('timingNavigationStart', type=int)
    timing_end = request.args.get('timingResponseEnd', type=int)
    if timing_start and timing_end and (timing_end - timing_start < 10): 
        headless_score += 10
    if request.args.get('userInteraction', 'false').lower() != 'true': 
        headless_score += 20

    session_token = str(uuid4())
    current_time = time.time() * 1000
    if session_token in request_history and (current_time - request_history[session_token] < 50): 
        headless_score += 10
    request_history[session_token] = current_time

    # 최종 판단
    result['headless_score'] = headless_score
    if headless_score > 50:
        session_store[session_token] = '/memberships'
        return jsonify({
            'redirect': f'/captcha?session_token={session_token}',
            'requires_captcha': True,
            'recaptcha_site_key': 'your-recaptcha-site-key'  # Google reCAPTCHA Site Key로 교체
        })
    else:
        return jsonify({'message': 'you are human', 'requires_captcha': False})

@app.route('/captcha', methods=['GET'])
def show_captcha():
    session_token = request.args.get('session_token')
    if session_token in session_store:
        return jsonify({
            'session_token': session_token,
            'recaptcha_site_key': 'your-recaptcha-site-key'
        })
    return jsonify({'error': 'Invalid session token'}), 400

@app.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    session_token = request.form.get('session_token')
    recaptcha_response = request.form.get('recaptcha_response')

    verification = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': RECAPTCHA_SECRET, 'response': recaptcha_response}
    ).json()

    if verification['success'] and session_token in session_store:
        original_url = session_store.pop(session_token)
        return jsonify({'message': 'you are human', 'redirect': original_url})
    return jsonify({'message': 'Failed: Likely Bot'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
  
