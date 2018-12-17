import requests
import json
import os
#from setToken import setToken

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

def send_video_message(id, url_video):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "template",
                "payload":{
                    "template_type": "open_graph",
                    "elements":[
                        {
                            "url": url_video
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)

def send_button_message(id): 
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN) 
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type": "template",
                "payload":{
                    "template_type": "button",
                    "text": "*command button*",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "任務",
                            "payload": "yes"
                        },
                        {
                            "type": "postback",
                            "title": "本周任務",
                            "payload": "yes"
                        },
                        {
                            "type": "postback",
                            "title": "魔物",
                            "payload": "yes"
                        },
                    ]
                }
            }
        }
    }
    response = requests.post(url, json = payload)

    if response.status_code != 200:
        print("\n<error> unable to send message: ", response.text, "\n")

    return response

def newButtonTest(id):
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
