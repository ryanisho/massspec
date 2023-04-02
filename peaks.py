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
            compound = findCombo(mz)
            lst.append({current_scan_num : [mz, intensity]})
    return lst
 
def findCombo(molarMass):
  carbonMass = 12.01
  hydrogenMass = 1.008
  oxygenMass = 16.00
  tolerance = 0.1

  c, h, o = 0

  while c <= int(molarMass/carbonMass):
    while h <= int(molarMass/hydrogenMass):
      while o <= int(molarMass/oxygenMass):
        currentMolarMass = c * carbonMass + h * hydrogenMass + o * oxygenMass;
        
        if abs(currentMolarMass - molarMass) < tolerance:
          print(f"Possible Compound: C{c}H{h}O{o}")
          break
      o = 0
    h = 0