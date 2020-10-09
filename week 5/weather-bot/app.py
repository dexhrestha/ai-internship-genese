from flask import Flask,jsonify,request
from utils import get_current_weather
app  = Flask(__name__)

@app.route('/api')
def home():
    content = {'content':[],
        'message':'Hello'}
    return jsonify(content)

@app.route('/api/get-weather',methods=['POST'])
def get_weather():
    content = {'content':{},'message':''}
    if request.is_json:
        content = request.json
        location=content.get('location')
        content=get_current_weather(location)
    return content
    
if __name__ == '__main__':
    app.run(port=8080,debug=True)
