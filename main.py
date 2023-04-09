import os
import uuid

from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 设置最大请求大小为 16MB

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # 生成随机文件名
    ext = os.path.splitext(file.filename)[1]
    new_filename = uuid.uuid4().hex + ext

    # 保存文件
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

    # 返回文件名和绝对路径
    abs_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return jsonify({
        "data": {'filename': new_filename, 'path': abs_path},
        "statusCode": 200,
    })

@app.route('/images/<path:path>')
def get_image(path):
    try:
        img_path = os.path.abspath(os.path.join('./upload', path))
        response = make_response(send_file(img_path, mimetype='image/jpeg'))
        response.headers.set('Access-Control-Allow-Origin', '*')
        return response
    except FileNotFoundError:
        return "Image not found", 404

if __name__ == '__main__':
    app.run('0.0.0.0')
