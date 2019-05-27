# To denoise the fMRI data, Artifact-ICs were removed by regressing out its corresponding timeseries from the original data
fsl_regfilt -i func_data -o func_data_denoised -d func_data.ica/melodic_mix -f "1, 2, 3"  # where comma-separated list of component numbers should be ICs identified as artifacts
