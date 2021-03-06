DeMix: maximizing peptide identification from cofragmentation
=====

##### Dependent packages:  

Python 2.7  
numpy  
pandas  
lxml  
pymzml http://pymzml.github.io/  
pyteomics http://pythonhosted.org//pyteomics/  
msconvert (ProteoWizard) http://proteowizard.sourceforge.net/index.shtml  
MS-GF+ http://omics.pnl.gov/software/ms-gf  
Java runtime environment  

##### Procedures:

1. msconvert, RAW to mzML.gz, with filter "zeroSample removeExtra 1-2"  ** Note:** do not use "peakPicking" option in msconvert.
2. run_demix_pipeline to execute pipeline under command line (also execute MS-GF+ database searching)

* Note: the default setting of OpenMS parameters are optimized for Thermo Orbitrap Q-Exactive mass spectrometer (**high-resolution**: 70,000 MS1 and 17,500 MS2). Change parameters in OpenMS/TOPP if using data from different instrumental settings.
* Note: the pipeline works with spectra in **profile** mode (both MS1 and MS2), and does peak picking. Modify the TOPP pipeline, if using spectra in centroid mode or mixed.
* Note: change the modification file under the path of MSGFPlus if searching for different PTMs.  
* Caution: many bug reports related to the database searching with MS-GF+. If program fails while calling the subprocess of MS-GF+, please check the Java setting in your system evrionment, and manually excute the command for MS-GF+ generated from the script.

##### Example:
* Windows Command Prompt   
> python C:\GitHub\DeMix\run_demix_pipeline.py -exe "c:\Program Files\OpenMS-1.11\bin\ExecutePipeline.exe" -db c:\DATA\HUMAN.fa -w 4.0 C:\GitHub\DeMix\Example\20131106_Q2_SDC_120MIN_HELA1.mzML.gz

* Linux or OSX Terminal    
> python /home/GitHub/DeMix/run_demix_pipeline.py /home/GitHub/DeMix/Example/20131106_Q2_SDC_120MIN_HELA1.mzML.gz -db /Data/HUMAN.fa -w 4.0 -out_dir DeMixResult

Parameters:
*   -db : Fasta file of proteome sequences (might require writing permit on the path for MS-GF+ indexing)  
*   -w : full width of precursor isolation window, default 4.0   
*   -out_dir : root path for outputs, default: current working path "."   ** Note**: spectra and identification result will be put in: out_dir/TOPPAS_out/004-PeakPickerHiRes/  

* Set these options only for debug purpose:   
-exe : when "ExecutePipeline" is not found in system environment PATH.  
-topp : when the default TOPPAS workflow is not working.  
-trf : when failed generating temporary resource file.  

##### Reference
Zhang, B., Pirmoradian, M., Chernobrovkin, A., & Zubarev, R. A. (2014). DeMix Workflow for Efficient Identification of Co-fragmented Peptides in High Resolution Data-dependent Tandem Mass Spectrometry. Molecular & Cellular Proteomics : MCP. doi:10.1074/mcp.O114.038877
http://www.ncbi.nlm.nih.gov/pubmed/25100859
