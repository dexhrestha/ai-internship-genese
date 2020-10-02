from flask import Flask,render_template,redirect,request,url_for
from werkzeug.utils import secure_filename
from utils import *
from flask import jsonify
import json

from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def hello():
     return render_template('index.html')

@app.route('/search_url',methods = ['POST'])
def search_url():

    if request.method == 'POST':
        
        img_url = request.form.get('url')
        filename = get_file_name(img_url)
        message=None
        if not allowed_file(filename):
            return render_template('index.html',message="Not a valid image")  
        content = generate_content(img_url)
          
        if len(content['FaceDetails'])  == 0:
                message = "not a person"
        return render_template('index.html',img_url=img_url,content=content,message=message)
    return redirect('/')

@app.route('/search_upload',methods=['POST'])
def search_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html',message="No file key in request.files") 

        file = request.files['file']
        message = None
        if file.filename == '':
            return render_template('index.html',message="Please select a file") 
        if not allowed_file(file.filename):
            return render_template('index.html',message="Not a valid image file") 

        if file and allowed_file(file.filename):

            file.filename = secure_filename(file.filename)
            img_url = upload_file_to_s3(file,'imagetest-dee',get_url=True)                    
            content = generate_content(img_url)
            
            if len(content['FaceDetails'])  == 0:
                print('here')
                message = "not a person"
            return render_template('index.html',img_url=img_url,content=content,message=message)


        return redirect('/')

@app.route('/api/search_url',methods=['GET','POST'])
def search_url_api():
    if request.is_json:
        data = request.get_json()
        url = data['url']
        filename = get_file_name(url)
        response = {'content':{'FaceDetails':[]}}
        if not allowed_file(filename):
            response['message']="Not a valid image" 
            return (jsonify(response))
        response['content'] = generate_content(url)

        return (jsonify(response))


if __name__ == '__main__':
    app.run(port=8080,debug=True)
    

