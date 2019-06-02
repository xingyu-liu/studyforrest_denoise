# perform ICA with FSL’s MELODIC (version 3.15) on the preprocessed fMRI data
melodic -i func_data -o func_data.ica -v --nobet --bgthreshold=1 --tr=2.000001 -d 0 --mmthresh=0.5 --report --guireport=../../report.html 

