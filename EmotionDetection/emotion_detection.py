import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    
    if requests is None:
        # fallback to urllib if requests is not available
        from urllib import request as _request, parse as _parse
        data = json.dumps(myobj).encode('utf-8')
        req = _request.Request(url, data=data, headers={
            'Content-Type': 'application/json',
            **header
        })
        try:
            with _request.urlopen(req) as resp:
                resp_text = resp.read().decode('utf-8')
                status_code = resp.getcode()
        except Exception:
            status_code = 400
            resp_text = ''
        response_text = resp_text
    else:
        response = requests.post(url, json=myobj, headers=header)
        response_text = response.text
        status_code = response.status_code

    if status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
        
    formatted_response = json.loads(response_text)
    
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    dominant_emotion = max(emotions, key=emotions.get)
    
    return {
        'anger': emotions['anger'],
        'disgust': emotions['disgust'],
        'fear': emotions['fear'],
        'joy': emotions['joy'],
        'sadness': emotions['sadness'],
        'dominant_emotion': dominant_emotion
    }