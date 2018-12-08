import requests
import json
import os
from setToken import setToken

setToken()
GRAPH_URL = "https://graph.facebook.com/v3.2"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "text": text
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_image_message(id, url_img):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "image",
                "payload":{
                    "url": url_img
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)

def send_button_message(id, url): 
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN) 
    """
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "template",
                "payload":{
                    "template_type": "button",
                    "text": "what",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "visit Messenger",
                            "payload": "no"
                        },
                        {
                            "type": "postback",
                            "title": "visi Messenger",
                            "payload": "no"
                        }
                    ]
                }
            }
        }
    }
    """
    payload = {
        "recipient": {"id": id},
        "message": {"text": "https://www.telegraph.co.uk/news/picturegalleries/picturesoftheday/12198377/Pictures-of-the-day-19th-March-2016.html"}
    }
    response = requests.post(url, json = payload)

    if response.status_code != 200:
        print("\n<error> unable to send message: ", response.text, "\n")

    return response

def newButtonTest(id):
    print("00000000000000000000000000000000000000000000000000000000000000000000")
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN) 
    payload = {
        "recipient":{
            "id": id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Try the postback button!",
                    "buttons":[
                        {
                            "type":"postback",
                            "title":"Postback Button",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            }
        } 
    }
    response = requests.post(url, json = payload)

    if response.status_code != 200:
        print("\n<error> unable to send message: ", response.text, "\n")

    return response


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
