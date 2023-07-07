import requests

def lineNotifyMessage(token, image_path):
    with open("output.txt",'r' ,encoding='utf-8') as file:
        msg = file.read()

    headers = { "Authorization": "Bearer " + token }
    data = { 'message': msg }

    image = open(image_path, 'rb')
    files = { 'imageFile': image }

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify",
        headers = headers, data = data, files = files)