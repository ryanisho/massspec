from flask import (
    Flask,
    render_template,
    request,
    render_template_string,
    redirect,
    send_file,
)
from pyopenms import MSExperiment, MzXMLFile
import io, os, string, re
from properties import *
import requests

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Main Flask App
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/info", methods=["GET", "POST"])
def info():
    # Check if a file is present in the request
    if "fileUpload" not in request.files:
        return redirect(request.url)

    file = request.files["fileUpload"]

    # If the file is empty or has an invalid extension, show an error message
    if file.filename == "" or not allowed_file(file.filename):
        return redirect(request.url)

    # Save the file to the upload folder and parse it
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        mzxml_file = filename
        header = create_header(mzxml_file)
        body = list(create_body(mzxml_file))
        meta = parse_ms_instrument(mzxml_file)
        scanCount = extract_scan_count(mzxml_file)

        return render_template(
            "table.html",
            header=header,
            body=body,
            meta=meta,
            scanCount=scanCount,
            mzxml_file=mzxml_file,
        )


@app.route("/peaks/<mzxml_file>/<int:value>", methods=["GET", "POST"])
def peaks(mzxml_file, value):
    if request.method == "GET":
        peaks = detect_peaks(mzxml_file, value)
        peakLen = len(peaks)
        iterator = 0
        index = "scan=" + str(value)

        return render_template(
            "peaks.html", value=value, index=index, peaks=peaks, peakLen=peakLen
        )
    else:
        return render_template("peaks.html", peaks=peaks)


@app.route("/convert/<mzxml_file>", methods=["POST", "GET"])
def convert(mzxml_file):
    xml_file = "output.xml"
    mzxml_to_xml(mzxml_file, xml_file)

    return send_file(xml_file, as_attachment=True)


@app.route("/compound/<value>/<t>/<mz>/<intensity>", methods=["POST", "GET"])
def compound(value, mz, t, intensity):
    if request.method == "GET":
        compoundInfo = findCompound(mz)
        compoundName = defCompound(compoundInfo)
        peakNum = t
        breakdown = composition(compoundInfo)
        return render_template(
            "compound.html",
            breakdown=breakdown,
            intensity=intensity,
            value=value,
            mz=mz,
            compoundInfo=compoundInfo,
            compoundName=compoundName,
            peakNum=peakNum,
        )
    else:
        return render_template("compound.html")


if __name__ == "__main__":
    app.run(debug=True)
