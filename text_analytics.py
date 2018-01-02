########### Python 2.7 #############
import requests, json

data_file = open("data.txt","r")

url = 'https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
payload = {
    # Request parameters
    "documents": [
    {
      "id": "string",
      "text": "Many Deep Learning hardware startup ventures will begin to finally deliver their silicon in 2018. These will all be mostly busts because they will forget to deliver good software to support their new solutions. These firms have as their DNA, hardware. Unfortunately, in the DL space, software is just as important. Most of these startups don’t understand software and don’t understand the cost of developing software. These firms may deliver silicon, but nothing will ever run on them!"
    }
  ]
}
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd80ae700fdba4e839e7b209bb82ec100',
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.json()['documents'][0]['keyPhrases']
    print(data)
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))