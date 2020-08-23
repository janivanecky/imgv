from flask import Flask
from flask import render_template, send_from_directory
import os

app = Flask(__name__)

# Serve at most 100 images to keep things sane.
MAX_IMG_LIMIT = 100

@app.route('/imgs/<path:img>')
def get_img(img):
    # The GET parameter doesn't contain the initial slash, so we have to re-add it.
    img = '/' + img
    return send_from_directory(os.path.dirname(img), os.path.basename(img))

@app.route('/', defaults={'next_dir': os.path.expanduser('~')})
@app.route('/<path:next_dir>')
def main(next_dir):
    # The GET parameter doesn't contain the initial slash, so we have to re-add it.
    current_dir = '/' + next_dir

    #
    files = os.listdir(current_dir)
    
    # Create a list of sub-directories.
    dirs = [f for f in files if os.path.isdir(os.path.join(current_dir, f))]
    dirs = sorted(dirs)
    # Make into tuples of (dir_name, dir_path).
    # Note that we're stripping first slash from the path so it can be used as a GET parameter.
    dirs = [(d, os.path.join(current_dir, d).lstrip('/')) for d in dirs]
    # Add "go up" option.
    dirs = [("..", os.path.dirname(current_dir).lstrip('/'))] + dirs

    # Create a list of images to display.
    imgs = [f for f in files if any([f.endswith(ext) for ext in ['png', 'jpg', 'jpeg']])]
    # Make into tuples of (img_name, img_path).
    # Note that we're stripping first slash from the path so it can be used as a GET parameter.
    imgs = [(i, os.path.join(current_dir, i).lstrip('/')) for i in imgs]
    imgs = imgs[:MAX_IMG_LIMIT]

    # Serve.
    return render_template('index.html', imgs=imgs, dirs=dirs)