from cStringIO import StringIO
import requests, json
import bs4
import sys
import nltk.data
from gtts import gTTS
import os
import sys, getopt
import re
import numpy as np
import imageio
from moviepy.editor import *
from gtts import gTTS
import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
import string
import gensim
from gensim import corpora
import shutil
reload(sys)
sys.setdefaultencoding('utf8')

_FPS=24

def getimage(query):
    url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
    headers = {
        'Ocp-Apim-Subscription-Key': '60fc159801924ff89e38e80ebd688e26'
    }
    try:
        response = requests.get(url+"?q=" + query+"&count=1", headers=headers)
        data = response.json()
        if data['value']:
            content_url =  data['value'][0]['contentUrl']
            print(content_url)
            return content_url
        else:
            return ""
    except Exception as e:
        print(e)
        return ""

def format_text(string): #break in to lines to fit the screen
    words=string.split()
    output=''
    buffer_string=''
    for w in words:
        if(len(buffer_string)<50):
            buffer_string+=w+' '
        else:
            output+=buffer_string+'\n'
            buffer_string=w+' '
    output+=buffer_string   
    return output

print("Retrieving page...")
res = requests.get(sys.argv[1])
print("Page retrieved")
res.raise_for_status()
print(res.text)
noStarchSoup = bs4.BeautifulSoup(res.text,"html")
data = noStarchSoup.select('.postArticle-content > section > .section-content > div')[0]
data= data.getText()
print(data)
'''data = [s.strip() for s in data.splitlines()]
print(data)'''
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
data = tokenizer.tokenize(data)
print(data)

my_list = []

globalkeyphrases = []

for i in range(0,min(len(data),100)):
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
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        keyPhrases = response.json()
        try:
            print(keyPhrases)
            j=0
            phrase = keyPhrases['documents'][0]['keyPhrases'][j]
            while phrase in globalkeyphrases:
                j=j+1
                phrase = keyPhrases['documents'][0]['keyPhrases'][j]
                print('lol ' + str(j) )
            print('finally')
            my_list.append(getimage(phrase))
            globalkeyphrases.append(phrase)
        except:
            my_list.append("")
    except Exception as e:
        print(e)

print(my_list)
print(data)



for i in range(0,len(my_list)):
    print("Downloading image number" + str(i) )
    f = open(str(i)+'.jpg','wb')
    f.write(requests.get(my_list[i]).content)
    f.close()


for i in range(0,len(data)):
    tts = gTTS(text=data[i], lang='en', slow=False)
    tts.save(str(i)+'.mp3')
    print '\n',data[i],'\n'
    print "created "+ str(i)+ " audio file"

count_lines = 1

text_clip_list=[]
audio_clip_list=[]
file_names_list = []

silence = AudioFileClip('silence.mp3').subclip(0,0.1)
audio_clip_list.append(silence)
for i in range(0,len(data)):

    sent_audio_clip=AudioFileClip(str(i)+'.mp3')
    print "length of audio: "+str(i)+" = ",sent_audio_clip.duration
    audio_clip_list.append(sent_audio_clip)

    sent_txt_clip = TextClip(format_text(data[i]),font='Montserrat',fontsize=100,color='white',bg_color='black',stroke_width=20).set_pos('bottom').set_duration(sent_audio_clip.duration).resize(width=750)
    text_clip_list.append(sent_txt_clip)

    file_names_list.append(str(i)+'.jpg')

audio_clip=concatenate_audioclips(audio_clip_list)

print(file_names_list)
number_of_images = len(file_names_list)

video_clip_list=[]


black_clip=ImageClip('black.jpg').set_duration(0.1).set_fps(_FPS)
video_clip_list.append(black_clip)
black = 'black.jpg'

if number_of_images > 0:
    for i in range(0,number_of_images):
        temp_clip=ImageClip(str(i)+'.jpg').set_duration(audio_clip.duration/number_of_images).set_position('top').set_fps(_FPS).crossfadein(0.5)
        video_clip_list.append(temp_clip)
        print 'temp_clip width: ',temp_clip.size
else:
    temp_clip=ImageClip(black).set_duration(audio_clip.duration).set_fps(_FPS)
    video_clip_list.append(temp_clip)

video_clip = concatenate_videoclips(video_clip_list).set_position('center')


txt_clip=concatenate_videoclips(text_clip_list).set_position('bottom')

result=CompositeVideoClip([video_clip,txt_clip])

print "Composite video clip size: ",result.size

result_with_audio=result.set_audio(audio_clip)


print "audio duration: "+str(audio_clip.duration)
print "result duration: "+str(result.duration)
print "result audio duration: "+str(result_with_audio.duration)



result_with_audio.write_videofile(str(count_lines)+'.mp4',codec='libx264',fps=_FPS)
