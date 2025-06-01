import json
# Firecloud
from google.cloud import firestore
from google.oauth2 import service_account
import base64
from typing import List
import requests


#===========================#
def get_base64_image(user_name:str):
    """
    As an example, here we use a placeholder base64 string for a gray circle
    """
    from PIL import Image, ImageDraw
    import io

    img = Image.new('RGB', (80, 80), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, 80, 80), fill=(150, 150, 150))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


#===========================#
def firebase_init(project:str, collection:str) -> None:
    """
    authenticate and connect Firebase/Firecloud
    """
    with open('firebase.json', 'r') as f:
        key_dict = json.load(f)

    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(
        credentials=creds, 
        project=project
    )
    return db


#===========================#
def request_get(headers, url) -> None:
    """ REQUEST """
    try:
        # GET request to Fitbit API
        response = requests.get(url, headers=headers)
        print(f"Status_code: {response.status_code}")

        if response.status_code == 401:
            # Access token expired
            print("[Access Token Expired]\n")
            return
        
        elif response.status_code == 200:
            # The request was successful
            print("[Request Successful] {} \n".format(url))
            return response.json()
        
        else:
            # Handle other status codes if necessary
            print(f"[Other status code]\n")
            response.raise_for_status()
            return

    except requests.exceptions.RequestException as e:
        print(f"[ERROR]: {e} | response: {response}")
        return


#===========================#
def fetch(firecloudClient, endpoints: List[str]):
    """
    Args:
        _endoints: 
    """
    if len(endpoints) == 2:
        return firecloudClient \
            .collection(endpoints[0]) \
            .document(endpoints[1])


    elif len(endpoints) == 4:
        return firecloudClient \
            .collection(endpoints[0]) \
            .document(endpoints[1]) \
            .collection(endpoints[2]) \
            .document(endpoints[3])
    
    elif len(endpoints) == 6:
        return firecloudClient \
            .collection(endpoints[0]) \
            .document(endpoints[1]) \
            .collection(endpoints[2]) \
            .document(endpoints[3]) \
            .collection(endpoints[4]) \
            .document(endpoints[5])

    else:
        raise ValueError("")






