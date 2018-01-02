########### Python 2.7 #############
import requests, json

data_file = open("data.txt","r")

url = 'https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
payload = {
    # Request parameters
    "documents": [
    {
      "id": "string",
      "text": "Hello from the other side. I must have called a thousand times."
    }
  ]
}
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd80ae700fdba4e839e7b209bb82ec100',
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.text
    print(data)
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))