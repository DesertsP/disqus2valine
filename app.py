# coding=utf-8
from flask import Flask, render_template, redirect, request
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
import utils.async_task as async_task
import re


FILE_DIR = '/tmp/disqus2lean/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADS_DEFAULT_DEST'] = FILE_DIR

data_set = UploadSet('data', DATA)
configure_uploads(app, data_set)
patch_request_class(app, 10 * 1024 * 1024)   # set maximum file size, default is 16MB


class UploadForm(FlaskForm):
    APPID = StringField('APPID')
    APPKEY = StringField('APPKEY')
    email = StringField('email')
    data = FileField(validators=[FileAllowed(data_set, u'xml only!'), FileRequired(u'File cannot be empty!')])
    submit = SubmitField(u'点击开始')


@app.route('/lean-engine', methods=['GET'])
def add_cron_task():
    url = request.args.get('url')
    urls = re.findall("[\w\d]+", url)
    if len(urls) == 1:
        with open("/var/spool/cron/crontabs/root", 'a+') as fp:
            task = "*/50 6-23 * * * curl https://" + urls[0] + ".leanapp.cn\n"
            if task in fp.read():
                return render_template('leanengine.html', status=0)
            else:
                fp.write(task)
                return render_template('leanengine.html', status=1)
    else:
        return render_template('leanengine.html', status=0)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = data_set.save(form.data.data)
        file_path = FILE_DIR + 'data/' + filename
        appid = form.APPID.data
        appkey = form.APPKEY.data
        email = form.email.data
        t = async_task.ProcessThread(appid, appkey, email, file_path)
        t.daemon = True
        t.start()
        return redirect("https://deserts.io")
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(threaded=True)