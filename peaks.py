import re
from pyopenms import MSExperiment, MzXMLFile
import pyopenms as oms

def detect_peaks(file_path, scan_num):
    lst = []
    # Load the mzXML file
    exp = oms.MSExperiment()
    oms.MzXMLFile().load(file_path, exp)

    # Initialize the peak picker
    picker = oms.PeakPickerHiRes()

    # Perform peak picking
    picked_exp = oms.MSExperiment()
    picker.pickExperiment(MSExperiment(exp), MSExperiment(picked_exp))

    # Print the detected peaks
    for spectrum in picked_exp:
      current_scan_num = spectrum.getNativeID()
      if current_scan_num == scan_num:
         for peak in spectrum:
            mz = peak.getMZ()
            intensity = peak.getIntensity()
            lst.append({current_scan_num : [mz, intensity]})
    return lst