# coding=utf-8
from flask import Flask, render_template, redirect
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
import async_task

FILE_DIR = '/tmp/disqus2lean/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADS_DEFAULT_DEST'] = FILE_DIR

data_set = UploadSet('data', DATA)
configure_uploads(app, data_set)
patch_request_class(app, 1024 * 1024)   # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    APPID = StringField('APPID')
    APPKEY = StringField('APPKEY')
    data = FileField(validators=[FileAllowed(data_set, u'xml only!'), FileRequired(u'File cannot be empty!')])
    submit = SubmitField(u'点击开始')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = data_set.save(form.data.data)
        file_path = FILE_DIR + 'data/' + filename
        appid = form.APPID.data
        appkey = form.APPKEY.data
        t = async_task.ProcessThread(appid, appkey, file_path)
        t.daemon = True
        t.start()
        return redirect("https://panjunwen.com")
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(threaded=True)