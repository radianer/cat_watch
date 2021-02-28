"""
@author Radianer
"""
from flask import Flask, Response, render_template

class CamCatServer:

    def __init__(self, cat_watcher):
        self.cat_watcher = cat_watcher
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            return render_template("index.html")
    
        @self.app.route("/video_feed")
        def video_feed():
            return Response(self.cat_watcher.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def run(self):
        self.app.run(debug=True)