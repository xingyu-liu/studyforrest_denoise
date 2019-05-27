# Register volume data with 'fsaverage' surface template

# original sm5 fMRI data
preproc-sess -sf Sesslist -fsd "sm5_original" -surface fsaverage lhrh -fwhm 0 -per-run -nostc -noinorm -nomc

# denoised sm5 fMRI data
preproc-sess -sf Sesslist -fsd "sm5_denoised" -surface fsaverage lhrh -fwhm 0 -per-run -nostc -noinorm -nomc

# original unsmth fMRI data
preproc-sess -sf Sesslist -fsd "unsmth_original" -surface fsaverage lhrh -fwhm 0 -per-run -nostc -noinorm -nomc

# denoised unsmth fMRI data
preproc-sess -sf Sesslist -fsd "unsmth_denoised" -surface fsaverage lhrh -fwhm 0 -per-run -nostc -noinorm -nomc




