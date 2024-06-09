from flask import Flask, request, jsonify
import requests
import subprocess

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check_security():
    data = request.json
    domain = data['domain']

    # SSL/TLS check using sslyze
    ssl_check_result = subprocess.run(['sslyze', domain], capture_output=True, text=True).stdout

    # Security headers check
    headers = requests.get(f'https://{domain}').headers
    security_headers = {
        'Content-Security-Policy': headers.get('Content-Security-Policy'),
        'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
        'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
        'X-Frame-Options': headers.get('X-Frame-Options')
    }

    # Clickjacking protection check
    clickjacking_protection = 'X-Frame-Options' in headers or 'Content-Security-Policy' in headers

    return jsonify({
        'ssl_check_result': ssl_check_result,
        'security_headers': security_headers,
        'clickjacking_protection': clickjacking_protection
    })

if __name__ == '__main__':
    app.run(debug=True)
