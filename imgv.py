from flask import Flask
from flask import render_template, send_from_directory
import os

app = Flask(__name__)

# Initialize to home dir.
current_dir = os.path.abspath("")

# Serve at most 100 images to keep things sane.
MAX_IMG_LIMIT = 100

@app.route('/imgs/<filename>')
def get_img(filename):
    return send_from_directory(current_dir, filename)

@app.route('/', defaults={'next_dir': None})
@app.route('/<next_dir>')
def main(next_dir):
    # Good'ol global state.
    global current_dir

    if next_dir:
        # `^` is an URL-representable symbol for going up the directory, so we need to parse it.
        if next_dir == '^':
            next_dir = '..'

        current_dir = os.path.join(current_dir, next_dir)
    else:
        # Reinitialize to home dir.
        current_dir = os.path.abspath("")

    # 
    files = os.listdir(current_dir)
    
    # Create a list of sub-directories.
    dirs = [f for f in files if os.path.isdir(os.path.join(current_dir, f))]
    dirs = sorted(dirs)
    dirs = ["^"] + dirs  # Add "go up" option.

    # Create a list of images to display.
    imgs = [f for f in files if any([f.endswith(ext) for ext in ['png', 'jpg', 'jpeg']])]
    imgs = imgs[:MAX_IMG_LIMIT]

    # Serve.
    return render_template('index.html', imgs=imgs, dirs=dirs)