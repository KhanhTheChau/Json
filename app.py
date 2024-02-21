import json
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# Hàm để điền các giá trị rỗng khi cần thiết
def fill_missing_values(data):
    default_values = {
        "id": None,
        "user": "",
        "password": "",
        "info": {
            "ho": "",
            "ten": "",
            "email": "",
            "sdt": "",
            "img": ""
        }
    }
    id_counter = 1
    for item in data:
        item["id"] = id_counter
        id_counter += 1
        for key, value in default_values.items():
            if key not in item:
                item[key] = value
            elif isinstance(item[key], dict):
                for subkey, subvalue in value.items():
                    if subkey not in item[key]:
                        item[key][subkey] = subvalue
    return data

@app.route('/save', methods=['POST'])
def save_json():
    data = request.json
    data = fill_missing_values(data)
    with open('user.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({'message': 'Data saved successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
