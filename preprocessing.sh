# Preproccess functional MRI data with FSL feat
# Example: sub-01, run-01
# The preprocessing of the functional images was performed using FEAT 
# (FMRIB Expert Analysis Tool version 6.00) including motion correction, 
# slice timing correction, brain extraction and high-pass temporal 
# filtering (200 s cutoff)22. Notably, we preporcessed the fMRI data 
# with two spatical smoothing settings: unsmoothing and 
# smoothing (Gaussian kernel; FWHM = 5 mm).

# spatial smoothing with 5mm FWHM 
feat preprocessing_design_sm5.fsf

# non spatial smoothing
feat preprocessing_design_unsm.fsf
