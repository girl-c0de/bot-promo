import requests

url = "http://127.0.0.1:8080/message/sendText/pythonbot"

payload = {
    "number": "5521994942511",
    "options": {
        "delay": 123,
        "presence": "composing",
        "linkPreview": True,
        "quoted": {
            "key": {
                "remoteJid": "<string>",
                "fromMe": False,
                "id": "<string>",
                "participant": "<string>"
            },
            "message": { "conversation": "<string>" }
        },
        "mentions": {
            "everyOne": False,
            "mentioned": ["5521994942511"]
        }
    },
    "textMessage": { "text": "te amo meu xuxubirinho!!" }
}
headers = {
    "apikey": "qwefWTz0pXcYJkBkVM4RY7lHAhSRvZzGOBNF6DRVv6ArgSO23eBoj61qf8zvRmWnMuJQ66soKRiZG0NSyzTBWSCVNQGKAp5F2IrhGUE62wEJrNXkhZfgOiNbH6MnzwPIhiuYNqfU3WE3Snzj4lLfIMok3dUH6p57M337lKNmnmATJMsyPC6iXyEu7NW59BX2hHOBbYa8VB2tE3e35hrwfRSWvD4uiDN2C86yg4Ji0d8oR6ka9PPuf8CEQ8QQlKrm",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())