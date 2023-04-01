import re

# Table Header Function
def create_header(mzxml_file):
    with open(mzxml_file) as f:
        for line in f:
            if ("<scan") in line:
                input_text = line

                # Locate the start and end positions of the properties
                start_position = input_text.find("scan") + len("scan")
                end_position = input_text.find(">")

                # Extract the properties substring from input_text
                properties_substring = input_text[start_position:end_position].strip()

                # Split properties_substring into individual properties
                properties_list = properties_substring.split(" ")

                # Extract the headers (keys) from the properties
                headers = []
                for prop in properties_list:
                    key, _ = prop.split('=', 1)
                    headers.append(key)
    return headers

# Extract and Create Table Body Function
def create_body(mzxml_file):
    scan_list = []
    with open(mzxml_file) as f:
        for line in f:
            if ("<scan") in line:
                input_text = line

                # Locate the start and end positions of the properties
                start_position = input_text.find("scan") + len("scan")
                end_position = input_text.find(">")

                # Extract the properties substring from input_text
                properties_substring = input_text[start_position:end_position].strip()

                # Split properties_substring into individual properties
                properties_list = properties_substring.split(" ")

                # Parse the properties into a dictionary
                properties_dict = {}
                for prop in properties_list:
                    key, value = prop.split('=', 1)
                    properties_dict[key] = value.strip('"')
                    
                # Append properties_dict to the scan_list
                scan_list.append(properties_dict)
    return scan_list

# Metadata

def parse_attribute(tag_string):
    attribs = {}
    tag_parts = re.findall(r'(\S+)=("[^"]*"|\'[^\']*\')', tag_string)
    for name, value in tag_parts:
        value = value.strip('"').strip("'")
        attribs[name] = value
    return attribs

def parse_ms_instrument(xml_file):
    with open(xml_file, 'r') as file:
        content = file.read()

    start_ms_instrument = content.find('<msInstrument>') + len('<msInstrument>')
    end_ms_instrument = content.find('</msInstrument>')
    ms_instrument_content = content[start_ms_instrument:end_ms_instrument]

    lst = []
    ms_instrument = {}
    while True:
        start_tag = ms_instrument_content.find('<') + 1
        end_tag = ms_instrument_content.find('>')
        if start_tag == 0 or end_tag == -1:
            break

        open_tag = ms_instrument_content[start_tag:end_tag]
        if ' ' not in open_tag:
            # Empty tag, skip
            ms_instrument_content = ms_instrument_content[end_tag + 1:]
            continue

        close_tag = open_tag.split()[0]
        start_close_tag = ms_instrument_content.find('</' + close_tag + '>') + len('</' + close_tag + '>')
        ms_instrument_content = ms_instrument_content[start_close_tag:]

        attribs = parse_attribute(open_tag)
        ms_instrument[close_tag] = attribs
    return ms_instrument

#Scan Count
def extract_scan_count(mzxml_file):
    with open(mzxml_file, 'r') as file:
        for line in file:
            if 'scanCount' in line:
                start = line.index('scanCount=') + 11
                end = line.index('"', start)
                return int(line[start:end])
    return None


