from flask import Flask, render_template, url_for, redirect, request, make_response
import os
import subprocess

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename, extension = os.path.splitext(file.filename)
    file.save('uploads/' + filename + extension)
    subprocess.call(["python3 yolov5/detect.py --weights yolov5/best.pt --source uploads/" + filename + extension + " --save-txt && cp yolov5/runs/detect/exp/" + filename + extension + " static"], shell=True)
    return redirect(url_for("show", filename=filename + extension))



@app.route('/show/<filename>/<extension>')
def show(filename):
    return render_template("success.html", filename=filename)
    

if __name__ == "__main__":
    app.run(debug=True)
