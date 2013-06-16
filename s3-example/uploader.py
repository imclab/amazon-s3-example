from flask import Flask, render_template, request, redirect, url_for
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from localsettings import AWS_KEY, AWS_SECRET_KEY, BUCKET

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		image = request.files['file']
		url = upload(image)
		return redirect(url)
	return render_template('index.html')

def upload(image):
	conn = S3Connection(AWS_KEY, AWS_SECRET_KEY)
	bucket = conn.get_bucket(BUCKET)
	k = Key(bucket)
	k.key = image.filename
	k.set_contents_from_file(image)
	return conn.generate_url(60, 'GET', bucket=BUCKET, key=image.filename, force_http=True)

if __name__ == "__main__":
    app.run(debug=True)
