# @file tips.py
# @brief some practice code
def test1():
    import json

    #with open('include/usage.json' , 'r') as json_file:
    #    data = json.load(json_file)
    #    print(json.dumps(data))
    
    data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

    json1 = json.dumps(data)
    print(json1)
    
    #jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'

    #text = json.loads(jsonData)
    #print(text)