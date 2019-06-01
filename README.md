# studyforrest_denoise

Scripts here are related to fMRI dataset 
'studyforrest_movie_denoised'(https://openneuro.org/datasets/ds001769).

# Denoise procedure
In the 'studyforrest_movie_denoised', we denoised the studyforrest 
audio-visual movie fMRI data(https://openneuro.org/datasets/ds000113) 
following a four-step procedure including 1.preprocessing, 
2.ICA decomposition, 3.IC classification and 4.artifacts removal.

1. Preprocessing  
Discription: performed using feat (FMRIB Expert Analysis Tool 
version 6.00, part of FMRIB's Software Library [www.fmrib.ox.ac.uk/fsl])  
Code: /preprocessing.sh

2. ICA decomposition  
Discription: performed with a probabilistic ICA algorithm implemented 
in the FSL’s MELODIC version 3.15  
Code: /MELODIC_ICA.sh

3. IC classification  
Discription: Classification of ICs was done manually using Melview
(http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Melview).

4. Artifacts removal  
Discription: performed with FSL’s MELODIC version 3.15  
Code: /artifact-IC_removal.sh

# Technical validation
Additionally, the technical quality of the datasets was validated in
two aspects, temporal signal-to-noise ratio (tSNR) and 
inter-subject correlation (ISC)

1. Register fMRI volume data on 'fsaverage' surface template
using FreeSurfer version 6.0.0 (https://surfer.nmr.mgh.harvard.edu)  
Code: /validation_analysis/preprocessing_fsaverage.sh

2. Calculate tSNR and ISC for pre- and post-denoising fMRI data  
Code: /validation_analysis/tSNR.py  
/validation_analysis/ISC.py

3. Calculate the cohen's d effect size for tSNR and ISC between 
pre- and post-denoising fMRI data  
Code: /validation_analysis/cohen_d.py

4. Generate visualization of the cohen's d of tSNR and ISC  
Code: /validation_analysis/results_visualization.py
