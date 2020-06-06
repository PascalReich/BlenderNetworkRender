import bpy
import sys
import subprocess


def install(package):
    subprocess.check_call(sys.executable, "-m", "pip", "install", package)


try:
    from flask import Flask, request, render_template
except ImportError:
    install("flask")
    from flask import Flask, request, render_template

from werkzeug.utils import secure_filename

try:
    import eventlet
except ImportError:
    install("eventlet")
    import eventlet

from eventlet import wsgi

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    f = request.files['file']
    filepath = 'tmp/' + secure_filename(f.filename)
    f.save(filepath)
    render(filepath)
    return "<img src='/static/" + name_from_file(filepath) + ".png'>"


def render(filepath="tmp/alley.blend"):
    bpy.ops.wm.open_mainfile(filepath=filepath)
    # print("yay")
    bpy.context.scene.cycles.device = 'GPU'
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "C:/Users/foggy/OneDrive/Documents/BlenderNetworkRender/static/" + name_from_file(
        filepath) + ".png"
    print(bpy.ops.render.render(write_still=1))


def name_from_file(filename):
    return filename.split("/").pop().split(".")[0]


# render()
# app.run("0.0.0.0", 5000)
wsgi.server(eventlet.listen(('', 8000)), app)
