from flask import Flask, request
from flask_cors import CORS
from predict import *
from utils.class_fetch import get_class_name
from utils.wiki_fetch import get_wiki_data
import utils.mongo_db_provider as db

app = Flask(__name__)
CORS(app)


@app.route('/recognize', methods=['POST'])
def recognize_handler():
    uploaded_image_path = '/home/zhaoxue/uploaded/'

    print(request.content_type)
    image = request.files['file']
    form = request.form
    timestamp = form["timestamp"]
    device_number = form["device_number"]
    local_id = form["local_id"]
    global_id = device_number+'_'+local_id
    print('Record received:\n'+str(timestamp)+'\n'+global_id)
    # Image received
    if image:
        # Get image file type
        name_splited = image.filename.split('.')
        file_type = name_splited[len(name_splited)-1]
        # Save to server with uploaded info
        saved_path = uploaded_image_path + global_id + '.' + file_type
        image.save(saved_path)
        # Load model
        model = load_model()
        # Predict: prediction result is the class with the highest possibility
        result = model_predict(model, image)
        max_match = result[0][result.argmax()].item()
        print('Max match value: ', max_match)

        # If no match (subject to threshold)
        if max_match < 14:
            return 'invalid image'

        # Get class name
        class_id = result.argmax().item()+1
        class_name = get_class_name(class_id)

        # Create a record in MongoDB
        record = {
            "record_id": global_id,
            "timestamp": timestamp,
            "image_path": saved_path,
            "result": class_name,
        }
        db.insert(record)

        # Return class name
        return class_name
    else:
        return 'error'


@app.route('/wiki', methods=['POST'])
def wiki_handler():
    print(request.content_type)
    print('Fetching wiki data...')
    request_json = request.json

    if request_json:
        class_name = request_json['class_name']
        summary, order_name, family_name, genus_name, species_name, page_url, image_url = get_wiki_data(class_name)
        return {
            'class_name': class_name,
            'taxonomy': {
                'order_name': order_name,
                'family_name': family_name,
                'genus_name': genus_name,
                'species_name': species_name,
            },
            'page_url': page_url,
            'image_url': image_url,
            'summary': summary
        }
    else:
        return 'error'


@app.route('/update_location', methods=['POST'])
def update_record_location():
    print(request.content_type)
    request_json = request.json
    if request_json:
        record_id = request_json['record_id']
        location = {
            'latitude': request_json['location']['latitude'],
            'longitude': request_json['location']['longitude']
        }
        rec = {
            'record_id': record_id,
            'location': location
        }
        db.update(rec)
        return 'updated'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
