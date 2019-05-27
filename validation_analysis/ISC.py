#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculate the leave one out temporal ISC for pre- and post-denoising fMRI data
@author: liuxingyu
"""

import nibabel as nib
import os
import numpy as np
import scipy.stats as stats

sessidlist = ["sub001", "sub002", "sub003", "sub004", "sub005", \
              "sub006", "sub009", "sub010", "sub014", "sub015", \
              "sub016", "sub017", "sub018", "sub019", "sub020"]

runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]


#-----generate leave-subi-out image-----

smth_cdt = 'unsmth'
hemi = 'rh'
noise_cdt = '_denoised'
projectdir = "/nfs/e5/studyforrest"
funcname = "audiovisual3T_fslpreproc2surface_{0}{1}".format(
        smth_cdt, noise_cdt)   
file_name = 'fmcpr.sm0.fsaverage.{0}.nii.gz'.format(hemi)
leave_one_out_dir = ('/nfs/e5/studyforrest/data_lxy/{0}/'
                'leave_one_out_average_surface{1}').format(
                        smth_cdt, noise_cdt)
vertexamount = 163842

for runid in runidlist:
    pair_number=len(sessidlist)
    example_path = os.path.join(projectdir, sessidlist[0], funcname, 
                                  runid, file_name)
    example_data = nib.load(example_path)
    example_image = example_data.get_data()[0, 0, 0,:]
    timepoint_amount = np.size(example_image)

    pair_order = 0
    
    sum_all_sub = np.zeros([vertexamount, timepoint_amount])  
    
    # calculate the sum of all subs
    for subid in sessidlist:
        result_path = os.path.join(projectdir, subid, funcname, runid, file_name)
        data = nib.load(result_path).get_data()[:, 0, 0,:]      
        data = np.nan_to_num(stats.zscore(data,axis=-1))
        sum_all_sub = sum_all_sub + data
        print("adding {0}".format(subid))
    
    sum_all_sub = sum_all_sub.reshape([vertexamount,1,1,timepoint_amount])
    img = nib.Nifti1Image(sum_all_sub, None, example_data.get_header())
    save_path = os.path.join(leave_one_out_dir, '{0}'.format(runid), 
                             'all_sub_sum_{0}.nii.gz'.format(hemi))
    nib.save(img, save_path)
    print("===" * 5,'done sum',"===" * 5)
    
    sum_all_sub = sum_all_sub[:,0,0,:]
    
    # calculate leave-subi-out data by 
    # 1.substract subi from the sum of all subs 
    # 2. average the remaining part
    for subid in sessidlist:
        result_path = os.path.join(projectdir, subid, funcname, 
                                   runid, file_name)
        data = nib.load(result_path).get_data()[:, 0, 0,:]
        data = np.nan_to_num(stats.zscore(data,axis=-1))
        leave_one_out_avg = (sum_all_sub - data)/(len(sessidlist) - 1)            
        
        leave_one_out_avg = leave_one_out_avg.reshape(
                [vertexamount,1,1,timepoint_amount])
        img = nib.Nifti1Image(leave_one_out_avg, None, 
                              example_data.get_header())            
        result_name = "leave_{0}_out_average_{1}.nii.gz".format(subid,hemi)
        save_path = os.path.join(leave_one_out_dir, '{0}'.format(runid), 
                                 result_name)
        nib.save(img, save_path)
        print("Saving {0} data".format(subid))
        
    print("===" * 5,'done runn{0}'.format(runid),"===" * 5)


#-----calculate ISC with leave one out method-----

result_dir = ('/nfs/e5/studyforrest/data_lxy/result/'
                'isc_temporal/surface') 

def isc(data1, data2):

    """calculate inter-subject correlation along the determined axis.
    
    Parameters
    ----------          
 
        data1: used to calculate functional connectivity, 
            shape = [n_samples, n_features].
        data2: used to calculate functional connectivity, 
            shape = [n_samples, n_features].
    
    Returns
    -------
        isc: point-to-point functional connectivity list of 
            data1 and data2, shape = [n_samples, ].
   
    Notes
    -----
        1. data1 and data2 should both be 2-dimensional.
        2. [n_samples, n_features] should be the same in data1 and data2.
        
    """
   
    data1 = np.nan_to_num(data1)
    data2 = np.nan_to_num(data2)
  
    z_data1 = np.nan_to_num(stats.zscore(data1,axis=-1))
    z_data2 = np.nan_to_num(stats.zscore(data2,axis=-1))
    corr = np.sum(z_data1*z_data2,axis=-1)/(np.size(data1,-1))
    
    return corr


for runid in runidlist: 
    result = []
    
    for subid in sessidlist:
        result_path1 = os.path.join(projectdir, subid, funcname, 
                                    runid, file_name)
        data1_info = nib.load(result_path1)
        data1 = data1_info.get_data()
        data1 = np.nan_to_num(stats.zscore(data1,axis=-1))
        print("===" * 10)
        print("loading %s" % result_path1)

        result_path2 = os.path.join(leave_one_out_dir, runid,
                                    'leave_{0}_out_average_{1}.nii.gz'
                                    .format(subid,hemi))
        data2 = nib.load(result_path2).get_data()
        print("loading %s" % result_path2)
        
        corr_d = isc(data1, data2)
        result.append(corr_d)

    print(np.shape(result))
    
    #--------save pair corr results------------
    result = np.asarray(result)
    result = np.swapaxes(result, 0 ,1)
    result = np.swapaxes(result, 1 ,2)
    result = np.swapaxes(result, 2 ,3)
    print(np.shape(result))

    #----------save ISC image-------------     
    avg_corr = np.mean(result, axis=-1)
   
    img = nib.nifti1image(avg_corr, None, data1_info.get_header())       
    result_name= '{0}_run{1}{2}_{3}.nii.gz'.format(smth_cdt, runid, noise_cdt, 
                  hemi)
    save_path = os.path.join(result_dir, result_name)
    nib.save(img, save_path)
    print("saving %s" % save_path)            

print("done")







