#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate visualization of cohen's d of ISC or tSNR 

@author: liuxingyu
"""

import os
import nibabel as nib
from surfer import Brain

mearsurement = 'ISC_temporal'
smth_cdt = 'unsmth'
analysis_dir_parent = ('/nfs/s2/userhome/liuxingyu/workingdir/'
                       'event_cognition/studyforrest')
analysis_dir = os.path.join(analysis_dir_parent, 'result/{0}/surface'
                .format(mearsurement))

cohen_d_lh = nib.load(os.path.join(analysis_dir, '{0}_cohend_lh.nii.gz'
                      .format(smth_cdt))).get_data()[:,0,0]   
cohen_d_rh = nib.load(os.path.join(analysis_dir, '{0}_cohend_rh.nii.gz'
                      .format(smth_cdt))).get_data()[:,0,0]
#------visualization--------
# parameters: tSNR -> max=2, colormap='autumn'
# parameters: SC -> min=-3, max=3, colormap='coolwarm'
brain = Brain('fsaverage','lh','inflated', background='w', offscreen=True)
brain.add_data(cohen_d_lh, min=-3, max=3, colormap='coolwarm')
brain.save_imageset('/nfs/s2/userhome/liuxingyu/Desktop/{0}_{1}_cohend_lh'
                    .format(mearsurement, smth_cdt), ['l','m','v'])
brain.close()

brain = Brain('fsaverage','rh','inflated', background='w', offscreen=True)
brain.add_data(cohen_d_rh, min=-3, max=3, colormap='coolwarm')
brain.save_imageset('/nfs/s2/userhome/liuxingyu/Desktop/{0}_{1}_cohend_rh'
                    .format(mearsurement, smth_cdt), ['l','m','v'])
brain.close()
