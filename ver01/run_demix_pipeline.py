# bo.zhang@ki.se
# A simplified version of DeMix data processing workflow.

import sys
import urllib
import subprocess
import tempfile
import argparse
import os

import feature_ms2_clone


apars = argparse.ArgumentParser()

# Set ONE mzML file converted from RAW file, require both MS1 and MS2 in profile mode. 
apars.add_argument('mzml')
# Set path to the reference proteome FASTA file. (require writing permit of the same path)
apars.add_argument('-db', default='HUMAN.fa')
# Set a out put path. (requre writing permit of the path)
apars.add_argument('-out_dir', default='.')
# Set the full width of precursor isolation window
apars.add_argument('-w', default=4.0)


# When not found in system PATH, specify the absolute path of ExecutePipeline.exe. 
apars.add_argument('-exe', default='ExecutePipeline')
# When using user customized TOPP workflow
apars.add_argument('-topp', default=os.path.join(os.path.dirname(sys.argv[0]), 'TOPP_Processing.toppas'))
# When loading a user coustomized TOPP resource file. 
apars.add_argument('-trf', default=tempfile.mktemp('.trf'))

#=======
args = apars.parse_args()
trf = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<PARAMETERS version="1.6.2" xsi:noNamespaceSchemaLocation="http://open-ms.sourceforge.net/schemas/Param_1_6_2.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NODE name="1" description="">
    <ITEMLIST name="url_list" type="string" description="" required="false" advanced="false">
      <LISTITEM value="file:%s"/>
    </ITEMLIST>
  </NODE>
</PARAMETERS>
''' % urllib.pathname2url(args.mzml)
open(args.trf, 'w').write(trf)

# '======= run TOPP workflow for peak picking and feature detection'
cmd = [	args.exe, 
		'-in', args.topp,
	 	'-resource_file', args.trf, 
		'-out_dir', args.out_dir ]
print ' '.join(cmd)
subprocess.call(cmd)

# '======= first pass MS-GF+ database searching '
centroidSpec = os.path.join(args.out_dir,  'TOPPAS_out', '004-PeakPickerHiRes', os.path.basename(args.mzml).replace('.gz', ''))
cmd = [ 'java', '-Xmx8g',
		'-jar', os.path.join(os.path.dirname(args.topp), 'MSGFPlus', 'MSGFPlus.jar'),
		'-mod', os.path.join(os.path.dirname(args.topp), 'MSGFPlus', 'Mods.txt'),
		'-d', args.db,
		'-s', centroidSpec,
		'-o', centroidSpec + '.mzid' ] 
# Q-Exactive, HCD, trypsin, 2 miscleavage, 0/1 13C, 10 ppm precursor tol.
cmd += '-t 10ppm -ti 0,1 -m 3 -inst 3 -minLength 7 -addFeatures 1 -tda 1'.split()
print ' '.join(cmd)
subprocess.call(cmd)


# '======== DeMix '
macc, max_scan = feature_ms2_clone.load_mzid(centroidSpec + '.mzid', qval=0.005)
t = macc.std() * 3
t = t > 10 and 10 or t

demixSpec = centroidSpec + '.demix.mgf'
featureTab = os.path.join(args.out_dir,  'TOPPAS_out', '009-TextExporter',
                          os.path.basename(args.mzml).replace('.gz', '').replace('.mzML', '.csv'))
demixSpec = feature_ms2_clone.spectra_clone(
    featureTab, centroidSpec, macc.mean(), max_scan, float(args.w))


# '======== second pass MS-GF+ dababase search '
cmd = [ 'java', '-Xmx8g',
		'-jar', os.path.join(os.path.dirname(args.topp), 'MSGFPlus', 'MSGFPlus.jar'),
		'-mod', os.path.join(os.path.dirname(args.topp), 'MSGFPlus', 'Mods.txt'),
		'-d', args.db,
		'-s', demixSpec,
		'-o', demixSpec + '.mzid',
		'-t', '%.1fppm' % t] # adaptive mass tolerance
cmd += '-ti 0,1 -m 3 -inst 3 -minLength 7 -addFeatures 1 -tda 1'.split()
print ' '.join(cmd)
subprocess.call(cmd)



