from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        greek_file = request.files['greek']
        cowper_file = request.files['cowper']
        greek_filename = secure_filename(greek_file.filename)
        cowper_filename = secure_filename(cowper_file.filename)
        greek_file.save(os.path.join(app.config['UPLOAD_FOLDER'], greek_filename))
        cowper_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cowper_filename))
        return redirect('/display?greek=' + greek_filename + '&cowper=' + cowper_filename)
    return '''
    <!doctype html>
    <title>Upload new Files</title>
    <h1>Upload new Files</h1>
    <form method=post enctype=multipart/form-data>
      Greek HTML: <input type=file name=greek><br>
      Cowper HTML: <input type=file name=cowper><br>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/display')
def display_files():
    greek_filename = request.args.get('greek')
    cowper_filename = request.args.get('cowper')
    with open(os.path.join(app.config['UPLOAD_FOLDER'], greek_filename)) as f:
        greek_content = f.read()
    with open(os.path.join(app.config['UPLOAD_FOLDER'], cowper_filename)) as f:
        cowper_content = f.read()
    return render_template('display.html', greek_content=greek_content, cowper_content=cowper_content)


if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')
    app.run(debug=True)
