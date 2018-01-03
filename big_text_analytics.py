import requests, json

with open('data.txt', 'r') as myfile:
    data=myfile.readlines()

print len(data)

for i in range(0,100):
    send_data = data[i]
    url = 'https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
    payload = {
        # Request parameters
        "documents": [
        {
          "id": "string",
          "text": send_data   
        }
      ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'd80ae700fdba4e839e7b209bb82ec100',
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    keyPhrases = response.json()
    #print(keyPhrases)
    if keyPhrases['documents']:
        print(keyPhrases['documents'][0]['keyPhrases'])