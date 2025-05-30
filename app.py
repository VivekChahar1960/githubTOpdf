from flask import Flask, Response, request
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "PDF Proxy API is running locally!"

@app.route('/api/pdf')
def get_pdf():
    file_url = request.args.get('url')
    if not file_url:
        return "Missing 'url' parameter", 400

    try:
        r = requests.get(file_url, stream=True)
        r.raise_for_status()
        return Response(
            r.iter_content(chunk_size=4096),
            content_type='application/pdf',
            headers={"Content-Disposition": "inline; filename=document.pdf"}
        )
    except requests.RequestException as e:
        print(f"Error: {e}")
        return "Failed to fetch PDF", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
