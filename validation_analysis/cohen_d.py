#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculate the cohen's d effect size for tSNR or ISC 
between the pre- and post-denoising fMRI data

@author: liuxingyu
"""

import nibabel as nib
import os
import numpy as np

sessidlist = ["sub001", "sub002", "sub003", "sub004", "sub005", \
              "sub006", "sub009", "sub010", "sub014", "sub015", \
              "sub016", "sub017", "sub018", "sub019", "sub020"]

runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]

smth_cdt = 'unsmth'
hemi = 'lh'
measurement = 'ISC_temporal'
analysis_dir = ('/nfs/s2/userhome/liuxingyu/workingdir/event_cognition/'
                'studyforrest/result/{0}/surface'.format(measurement))   
vertex_number = 163842

def cohen_d(pre,post):
    """alculate the cohen's d effect size of pre- and post-denoising fMRI data 
    Parameters
    ----------         
        pre: value of a certain measurement of pre-denoising fMRI data, 
            shape = [n_vertice, ].
 
        post: value of a certain measurement of post-denoising fMRI data, 
            shape = [n_vertice, ].
   
    Returns
    -------
        d: the cohen's d of pre and post, 
            shape = [n_vertice, ].
   
    Notes
    -----
        Cohen's d was calculated as the mean difference 
        between the pre- and post-denoising fMRI data divided by the pooled SD
    """
    npre = np.shape(pre)[-1]
    npost = np.shape(post)[-1]
    dof = npost + npre - 2
    d =  ((post.mean(-1) - pre.mean(-1)) / 
          np.sqrt(((npost-1)*np.var(post, axis=-1, ddof=1) + 
                   (npre-1)*np.var(pre, axis=-1, ddof=1)) / dof))
    d = np.nan_to_num(d)
    
    return d


if measurement == 'ISC_temporal':
    corr_allrun = np.zeros([vertex_number,len(runidlist),2])
    for runid in runidlist: 
        after_name = '{0}_run{1}_denoised_{2}.nii.gz'.format(
                smth_cdt, runid, hemi)
        after = nib.load(os.path.join(analysis_dir, 
                                      after_name)).get_data()[:,0,0]
        # fisher z transformation for pearson r value
        after_z = np.arctanh(after)
        
        before_name = '{0}_run{1}_{2}.nii.gz'.format(smth_cdt, runid, hemi)
        before = nib.load(os.path.join(analysis_dir, 
                                       before_name)).get_data()[:,0,0]
        before_z = np.arctanh(before)
        
        corr_allrun[:,int(runid)-1,0] = before_z
        corr_allrun[:,int(runid)-1,1] = after_z
        

if measurement == 'tSNR':
    corr_allrun = np.zeros([vertex_number,len(sessidlist),2])
    count = 0
    
    for subid in sessidlist: 
        after_name = '{0}_{1}_fsaverage_denoised_{2}.nii.gz'.format(
                smth_cdt, subid, hemi)
        after = nib.load(os.path.join(analysis_dir, 
                                      after_name)).get_data()[:,0,0]
        
        before_name = '{0}_{1}_fsaverage_{2}.nii.gz'.format(
                smth_cdt, subid, hemi)
        before = nib.load(os.path.join(analysis_dir, 
                                       before_name)).get_data()[:,0,0]
        corr_allrun[:,count,0] = before
        corr_allrun[:,count,1] = after
        count += 1
    
print("Done")

cohen_d = cohen_d(corr_allrun[:,:,0],corr_allrun[:,:,1])

# save cohen's d image
img = nib.Nifti1Image(cohen_d.reshape([vertex_number,1,1]), None)       
result_name= '{0}_cohend_{1}.nii.gz'.format(smth_cdt, hemi)
save_path = os.path.join(analysis_dir, result_name)
nib.save(img, save_path)
print("Saving %s" % save_path)  