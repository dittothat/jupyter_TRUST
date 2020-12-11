Organization is BIDS-like (https://bids-specification.readthedocs.io/en/stable/) if additional info about the thinking behind this structure is needed.
 
Use dcm2niix to make the dcm -> nii.gz conversion, as it will generate the most of the json sidecars automatically:
dcm2niix -z y -b y -m o -f sub-<number>_ses-<##>_%s_%d_%c -o <temp output location> <dicom input location>
example: dcm2niix -z y -b y -m o -f sub-scd04_ses-01_%s_%d_%c -o ./nifti_files/ ./dicoms/
 
Then organize the files into a tree like this:
 
/data/sub-scd04
└── ses-01
    ├── anat
    │   ├── sub-scd04_ses-01_T1w.json (this is the MEMPRAGE or equivalent)
    │   └── sub-scd04_ses-01_T1w.nii.gz
    │   ├── sub-scd04_ses-01_T2w.json (if the axial T2 exists)
    │   └── sub-scd04_ses-01_T2w.nii.gz
            sub-scd04_ses-01_acq_sag_T2w.json
            sub-scd04_ses-01_acq_sag_T2w.nii.gz
    ├── flow
    │   ├── sub-scd04_ses-01_rec-MIP_COR_tof.json (rec stands for "reconstruction", of the Time Of Flight data)
    │   ├── sub-scd04_ses-01_rec-MIP_COR_tof.nii.gz
    │   ├── sub-scd04_ses-01_rec-MIP_SAG_tof.json
    │   ├── sub-scd04_ses-01_rec-MIP_SAG_tof.nii.gz
    │   ├── sub-scd04_ses-01_rec-MIP_TRA_tof.json
    │   ├── sub-scd04_ses-01_rec-MIP_TRA_tof.nii.gz
    │   ├── sub-scd04_ses-01_run-1_rec-gre_flow.json (the PC-MRI data)
    │   ├── sub-scd04_ses-01_run-1_rec-gre_flow.nii.gz
    │   ├── sub-scd04_ses-01_run-1_rec-mag_flow.json
    │   ├── sub-scd04_ses-01_run-1_rec-mag_flow.nii.gz
    │   ├── sub-scd04_ses-01_run-1_rec-ph_flow.json (this *json, must include the fields given below)
    │   ├── sub-scd04_ses-01_run-1_rec-ph_flow.nii.gz
    │   ├── sub-scd04_ses-01_run-2_rec-gre_flow.json (if there are multiple runs these can be designated like this)
    │   ├── sub-scd04_ses-01_run-2_rec-gre_flow.nii.gz
    │   ├── sub-scd04_ses-01_run-2_rec-mag_flow.json
    │   ├── sub-scd04_ses-01_run-2_rec-mag_flow.nii.gz
    │   ├── sub-scd04_ses-01_run-2_rec-ph_flow.json (this *json, must include the fields given below)
    │   ├── sub-scd04_ses-01_run-2_rec-ph_flow.nii.gz
    │   ├── sub-scd04_ses-01_tof.json
    │   └── sub-scd04_ses-01_tof.nii.gz
    └── trust
        ├── sub-scd04_ses-01_acq-prep0_run-1_trust.json (this *json, must include the fields given below)
        ├── sub-scd04_ses-01_acq-prep0_run-1_trust.nii.gz
        ├── sub-scd04_ses-01_acq-prep1_run-1_trust.json (this *json, must include the fields given below)
        ├── sub-scd04_ses-01_acq-prep1_run-1_trust.nii.gz
        ├── sub-scd04_ses-01_acq-prep2_run-1_trust.json (this *json, must include the fields given below)
        ├── sub-scd04_ses-01_acq-prep2_run-1_trust.nii.gz
        ├── sub-scd04_ses-01_acq-prep2_run-1_trust.json (this *json, must include the fields given below)
        ├── sub-scd04_ses-01_acq-prep2_run-1_trust.nii.gz
        ├── sub-scd04_ses-01_acq-prep4_run-1_trust.json (this *json, must include the fields given below)
        ├── sub-scd04_ses-01_acq-prep4_run-1_trust.nii.gz
        ├── sub-scd04_ses-01_acq-prep8_run-1_trust.json (this *json, must include the fields given below)
        └── sub-scd04_ses-01_acq-prep8_run-1_trust.nii.gz
└── ses-02 (each subject should have at least two sessions)
...
 
 
Original source data should go in a parallel similarly structured tree:
/sourcedata/sub-scd04
└── ses-01
    └── dicoms
    └── raw
 
The pc-mri rec-ph (phase) *.json must include these fields:
    "VENC": 100, (cm/s, this is often given in the sequence name, but should be crossed checked in every case with the sAngio.sFlowArray.asElm[0].nVelocity in the Siemen's ascii dicom header. Run $ mri_probedicom --i <file.dcm> > ~prob.dat, then open up ~/probe.dat and search for "velocity")
    "RawData": true, (this indicates whether a raw file exists in the sourcedata tree for the corresponding dcm series)
    "RawFileName": "<filename>.DAT", (If the previous field is true, then include this please)
    "Vessels": ["RICA", "LICA", "BA", "other"] (this list can be modified to reflect the acquisition, sometimes we get the BA and ICAs in separate acquisitions. Most often it should be ["RICA", "LICA", "BA"])
 
The trust *.json must each include this field:
    "Hct": 0.34 (the hematocrit from blood test closest to the scan session without a transfusion in between)
 
Please observe that there must be a comma after each entry in the json file, but then no comma following the last field before the final }.
 
Please include a participants.tsv file of the following format in the root directory:
participant_id age sex group
sub-scd04 14 F HIE
 
Any issues in the conversion and sorting can be noted in a README file in the root directory.