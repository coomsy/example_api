from flask import Flask, request, Response
from base64 import b64decode
import json
from time import time
import string

app = Flask(__name__)

_token_value = "You'reInItToWinIt"

@app.route('/')
def hello_world():
    return open('pages/index.html').read()

# START Authorization methods
@app.route('/auth', methods = ['POST'])
def auth():
    print(request.headers)
    #if creds := request.headers.get('Authorization'): just wanted to flex with walrus
    creds = request.headers.get('Authorization')
    if creds:
        creds = b64decode(creds.split(' ')[-1]).decode().split(':',1)
        if creds[0] == 'wayne' and creds[1] == 'Youre10PlyBud!':
            return Response(response=json.dumps({
                                'Message': 'Good Job there bud',
                                'Token': _token_value
                            }), 
                            status=200,
                            headers={'Token': _token_value}) 
    
    return Response(response='{"error": "ooo, yah thats not how you do that"}', status=400)
        
# START Data Structures
## easy
@app.route('/alcohol')
def alcohol():
    if _token_value != request.headers.get('Token'):
        return Response(response='{"error":"Wheres my Token mf"}', status=400)
    return Response(response=open('data/alcohol.json', 'r').read(), status=200) 


# START validating exercise
@app.route('/alcohol/activity/<num>', methods = ['POST'])
def check_their_work(num):
    print(f'Got request for activity[{num}]')
    if _token_value != request.headers.get('Token'):
        return Response(response='{"error":"Wheres my Token mf"}', status=400)
    data = json.loads(open('data/alcohol.json', 'r').read())
    
    try:
        learner_answer = json.loads(request.data.decode())
    except Exception as ex:
        print(repr(ex))
        # no idea what error is, just tell em they didn't format correctly
        return Response(response='{"error": "What did you just send me?... this aint json?"}', 
                        status=400)
    
    if not learner_answer.get('answer'):
        return Response(response='{"error": "Could not find key \"answer\"... see / page"}', 
                        status=400)

    learner_answer = learner_answer['answer']

    # !!! IMPORTANT !!!
    #! no this isn't how I write stuff, this app is for fun. So I try to do one liners 
    #! + keep the learners from trying to cheat. Cuz aint no way they doing these
    # !!! IMPORTANT !!!
    answer = ''
    # Most expensive item (name)
    if num == '1':
        #str
        answer = list(max([ item for _, item in data.items() ], key=lambda x: list(x.values())[0]))[0]
    # Least expensive item (name)
    elif num == '2':
        #str
        answer = list(min([ item for _, item in data.items() ], key=lambda x: list(x.values())[0]))[0]
    # Top 10% Most Expensive (names)
    elif num == '3':
        # [ {str,float},... ]
        answer = list(sorted([ item for _, item in data.items() ], key=lambda x: list(x.values())[0], reverse=True))[:int(len(data) * .1 )]
    # Removing all special chars, in names
    elif num == '4':
        answer = []
        for _, item in data.items():
            for char in string.punctuation:
                item = { key.replace(char, ''):value for key,value in item.items() }
            answer.append(item)

    if isinstance(answer, str):
        if answer == learner_answer:
            return Response(response='{"Message": "Nice Going bud. On to the next.. Pitter patter"}', status=200)
        else:
            return Response(response='{"error": "Was the answer correct? In the words of the late E40, NOPE."}', status=400)
    elif isinstance(answer, list):
        # ducttape fix
        if sorted(answer, key=lambda x: list(x.values())[-1] ) == sorted(learner_answer, key=lambda x: list(x.values())[-1] ):
            return Response(response='{"Message": "Nice Going bud. On to the next.. Pitter patter"}', status=200)
        else:
            return Response(response='{"error": "Was the answer correct? In the words of the late E40, NOPE."}', status=400)




if __name__ == '__main__':
    #app.run(use_reloader=True)
    app.run()
