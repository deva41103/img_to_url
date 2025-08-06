from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from uuid import uuid4
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load .env variables (only needed for local dev)
load_dotenv()

app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            # Create a secure and unique filename
            ext = os.path.splitext(image.filename)[1]
            filename = secure_filename(f"{uuid4().hex}{ext}")

            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(image, public_id=filename)

            # Get the URL of the uploaded image
            image_url = upload_result.get("secure_url")

            return render_template('index.html', image_url=image_url)
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
