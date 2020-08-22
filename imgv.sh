#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
FLASK_APP=$DIRECTORY/imgv.py FLASK_DEBUG=1 IMG_VIEWER_DIR=$1 flask run -h 0.0.0.0 -p 6003