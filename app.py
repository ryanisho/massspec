
from flask import Flask, render_template, request, render_template_string
from pyopenms import MSExperiment, MzXMLFile
import io, os, string, re
import xml.etree.ElementTree as ET
import xml.dom.minidom
from properties import create_header, create_body, parse_ms_instrument, extract_scan_count
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



def detect_peaks(file_path):
    lst = []
    # Load the mzXML file
    exp = oms.MSExperiment()
    oms.MzXMLFile().load(file_path, exp)

    # Initialize the peak picker
    picker = oms.PeakPickerHiRes()

    # Perform peak picking
    picked_exp = oms.MSExperiment()
    picker.pickExperiment(exp, picked_exp)

    # Print the detected peaks
    for spectrum in picked_exp:
        scan_num = spectrum.getNativeID()

        for peak in spectrum:
            mz = peak.getMZ()
            intensity = peak.getIntensity()
            lst.append({scan_num : [mz, intensity]})
    return lst

mzxml_file = "test1.mzxml"

#Main Flask App
@app.route("/", methods = ["GET", "POST"])
def index():
    header = create_header(mzxml_file)
    body = list(create_body(mzxml_file))
    meta = parse_ms_instrument(mzxml_file)
    scanCount = extract_scan_count(mzxml_file)
    return render_template("index.html", header=header, body = body, meta = meta, scanCount = scanCount)

@app.route("/peaks", methods = ["GET"])
def peaks():
    peaks = detect_peaks(mzxml_file)
    val = peaks
    return render_template("peaks.html", peaks = peaks)

if __name__ == '__main__':
    app.run(debug=True)
