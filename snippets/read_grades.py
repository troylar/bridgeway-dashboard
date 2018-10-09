import json
with open('data.json') as f:
    data = json.load(f)
for subject in data:
    print(subject)
    print(data[subject]['grade'])
    print(data[subject]['percentage'])
