import json

def import_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def convertToHfJson(json_path):
    json_file = import_json(json_path)
    json_data = {}
    json_data['version'] = "v0.1"
    json_data['data'] = []
    for key in json_file['common_examples'].keys():
        row_list = json_file['common_examples'][key]
        for item in row_list:
            row = {"text": item, "intent":key}
            json_data['data'].append(row)
    return json_data

if __name__=="__main__":
    json_data = convertToHfJson('train-data.json')
    save_json(json_data, 'train-data-hf.json')