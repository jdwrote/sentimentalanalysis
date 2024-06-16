from flask import Flask, request, jsonify
from application_llm_sentiment import sentimental_analysis_llm
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

application = Flask(__name__)


@application.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    url = None
    if request.is_json:
        data = request.get_json()
        if data:
            url = data['url']
            llm_response = sentimental_analysis_llm(url)
            return llm_response
        else:
            pass
    else:
        if url is None:
            return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    application.run(debug=True)


