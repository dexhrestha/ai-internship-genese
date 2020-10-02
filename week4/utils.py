import logging

import requests
from urllib import parse
from PIL import Image
import io
import boto3 

client = boto3.client('rekognition') 
s3 = boto3.client(
   "s3"
)
def is_url(path):
    """
    Checks if given path is a URL

    Args:
        path (str): input path

    Returns:
        bool : True if URL else False 
    """
    return parse.urlparse(path).scheme in ['http','https','ftp']

def get_file_name(url):

    """
    Returns filename from given URL
    
    Args:
        url (str): input url
    
    Returns
        str: filename
    """
    slug = url.split('/')[-1]
    try:
        slug = slug.split('?')[0]
        return slug
    except:
        return slug
    

def allowed_file(filename):
    """
    Check whether given file is allowed
    Args:
        filename (str): input filename
    Returns:
        bool: True if file is images else False
    """
    try:
        format = filename.split('.')[-1]
    except:
        format = None
    if format in ['jpg','png','jpeg']:
        return True 
    return False
    
def upload_file_to_s3(file, bucket_name,get_url=False, acl="public-read"):
    """
    Uploads file to given s3 bucket

    Args:
        file (obj): File object to be uploaded
        bucket_name (str): Name of destination bucket
        get_url (bool): True if user wants url after uploading
        acl (str):Access control list
    Returns:
        bool/str: url if get_url is True else True if successfully uploaded else False
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        object_name = file.filename
        url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        logging.error("Something Happened: ", e)
        return False
    return url if get_url else True


def get_facial_features(client,path=None):
    """
    Get facial feautre from AWS Rekognition
    Args:
        client (obj): boto client object
        path (str): path of file
    Returns:
        dict/None: Response from AWS Rekognition if exceuted successfully else None
    """
    if path is None:
        return None
    if is_url(path):
        image = requests.get(path,stream=True).raw
    else:
        image = open(path,'rb')
        
    if image is not None:
        try:
            response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
            return response
        except Exception as e :
            logging.error(e)
            
            return None

    

def get_emotion(emotions):
    confidence_list = list(map(lambda x:x['Confidence'],emotions))
    emotion_list = list(map(lambda x:x['Type'],emotions))
    #find index of confidence with max confidence
    idx = confidence_list.index(max(confidence_list))
    return emotion_list[idx]
    
def get_gender(gender):
    return gender['Value'],gender['Confidence']

def get_age_range(ageRange):
    return f"{ageRange['Low']} to {ageRange['High']} years"

def get_sunglasses(sunglasses):
    return f"has sunglasses" if sunglasses['Value']  else f"has no sunglasses"

def get_eyeglasses(eyeglasses):
    return f"has eyeglasses" if eyeglasses['Value']  else f"has no eyeglasses"

def get_mustache(mustache):
    return f"has mustache" if mustache['Value']  else f"has no mustache"

def get_beard(beard):
    return f"has beard" if beard['Value']  else f"has no beard"

def generate_content(img_url):
    """
    Generate meaningful summary
    Args:
        img_url (str): URL of target image

    Returns:
        dict: meaningful summary of image
    """
    response = get_facial_features(client,path=img_url)
    content = {'FaceDetails':[]}
    try:
        for image in response['FaceDetails']:
            content['FaceDetails'].append({'Emotion':get_emotion(image['Emotions']),
                                            'Gender':get_gender(image['Gender']),
                                            'AgeRange':get_age_range(image['AgeRange']),
                                            'Sunglasses':get_sunglasses(image['Sunglasses']),
                                            'Eyeglasses':get_eyeglasses(image['Eyeglasses']),
                                            'Mustache':get_mustache(image['Mustache']),
                                            'Beard':get_beard(image['Beard']),
                                            })
        return content
    except:
        return "An error occured at server. Please try again later"

