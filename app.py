
from flask import Flask, render_template, request, render_template_string, redirect
from pyopenms import MSExperiment, MzXMLFile
import io, os, string, re
import xml.etree.ElementTree as ET
import xml.dom.minidom
from properties import *
import pyopenms as oms

app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
    # if request.method == 'POST':
    #     mzxml_file = "test.mzxml"
        # if mzxml_file and mzxml_file.filename.endswith('.mzxml'):
          

        # def remove_namespace(tag):
        #     return tag.split('}')[-1]

        # def mzxml_to_xml(mzxml_file, xml_file):
        #     # Parse the mzXML file
        #     tree = ET.parse(mzxml_file)
        #     root = tree.getroot()

        #     # Create a new XML root element
        #     new_root = ET.Element(remove_namespace(root.tag))

        #     # Iterate through the mzXML elements and copy them to the new XML file
        #     for element in root:
        #         new_element = ET.SubElement(new_root, remove_namespace(element.tag))

        #         for attr_key, attr_value in element.attrib.items():
        #             new_element.set(attr_key, attr_value)

        #         for child in element:
        #             new_child = ET.SubElement(new_element, remove_namespace(child.tag))

        #             for child_attr_key, child_attr_value in child.attrib.items():
        #                 new_child.set(child_attr_key, child_attr_value)

        #     # Write the new XML file
        #     new_tree = ET.ElementTree(new_root)
        #     new_tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        #     # dom = xml.dom.minidom.parse(xml_file) # or xml.dom.minidom.parseString(xml_string)
        #     # pretty_xml_as_string = dom.toprettyxml()

        # # Example usage
        # mzxml_file = "test.mzxml"
        # xml_file = "output.xml"
        # mzxml_to_xml(mzxml_file, xml_file)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Main Flask App
@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/info", methods = ["GET", "POST"])
def info():
     # Check if a file is present in the request
    if 'fileUpload' not in request.files:
        #flash('No file found')
        return redirect(request.url)

    file = request.files['fileUpload']

    # If the file is empty or has an invalid extension, show an error message
    if file.filename == '' or not allowed_file(file.filename):
        #flash('Invalid file')
        return redirect(request.url)

    # Save the file to the upload folder and parse it
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        #flash('File uploaded and parsed successfully') 
        mzxml_file = filename
        header = create_header(mzxml_file)
        body = list(create_body(mzxml_file))
        meta = parse_ms_instrument(mzxml_file)
        scanCount = extract_scan_count(mzxml_file)
        possibleCombo = findCombo(500)

        return render_template("table.html", header=header, body = body, meta = meta, scanCount = scanCount, possibleCombo = possibleCombo, mzxml_file = mzxml_file)


@app.route("/peaks/<mzxml_file>/<int:value>", methods = ["GET", "POST"])
def peaks(mzxml_file, value):
    if (request.method == "GET"):
        peaks = detect_peaks(mzxml_file, value)
        return render_template("peaks.html", peaks = peaks)
    else:
        peaks = detect_peaks(mzxml_file, value)
        return render_template("peaks.html", peaks = peaks)

if __name__ == '__main__':
    app.run(debug=True)
