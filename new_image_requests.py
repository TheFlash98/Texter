########### Python 2.7 #############
import requests, json

#data_file = open("data.txt","r")
#data = request.data['textcontent']
url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
headers = {
    'Ocp-Apim-Subscription-Key': '60fc159801924ff89e38e80ebd688e26'
}
query = 'cat'
response = requests.get(url+"?q=" + query+"&count=1", headers=headers)
data = response.json()
if data['value']:
    print data['value'][0]['contentUrl']