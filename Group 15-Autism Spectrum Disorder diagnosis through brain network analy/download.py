import pandas as pd
import os
from tqdm import tqdm
# import wget
import requests



# base_str = https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/[pipeline]/[strategy]/[derivative]/[file identifier]_[derivative].[ext]


# https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/cpac/filt_global/rois_aal/KKI_0050822_rois_aal.1D
base_str = "https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/[pipeline]/[filt]/[roi]/[file identifier]_[roi].1D"

# https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/cpac/func_minimal/OHSU_0050147_func_minimal.nii.gz

roi_str = "https://s3.amazonaws.com/fcp-indi/data/Projects/ABIDE_Initiative/Outputs/[pipeline]/filt_global/[derivative]/[file identifier]_[derivative].1D"


def create_url(pipe, roi, fg):
    url = base_str.replace("[pipeline]", pipe)
    url = url.replace("[filt]", fg)
    url = url.replace("[roi]", roi)
    return url

# Function to download a file from a given URL
def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_abide1_roi(pheno_file, out_dir, pipe, roi, fg):
    df = pd.read_csv(pheno_file)

    # url = create_url(pipe, roi, fg)

    # create out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for i, row in tqdm(df.iterrows(), total=len(df)):
        sub_id = row["SUB_ID"]
        # site = row["SITE_ID"]
        site = row['FILE_ID']
        if site == 'no_filename':
            continue

        url = create_url(pipe, roi, fg)
        url = url.replace("[file identifier]", site)
        
        out_file = f"{out_dir}/{site}_{roi}.1D"
        try:
            # wget.download(url, out_file)
            # print(url)
            download_file(url, out_file)
        except Exception as e:
            print(e)
            print(f"Failed to download {url} to {out_file}")


def download_abide1_pcp(pheno_file, out_dir):
    df = pd.read_csv(pheno_file)

    # create out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for i, row in tqdm(df.iterrows(), total=len(df)):
        sub_id = row["SUB_ID"]
        site = row["SITE_ID"]
        url = base_str.replace("[file identifier]", site + "_00" + str(sub_id))
        out_file = f"{out_dir}/{site}_{sub_id}_func_preproc.nii.gz"
        # try:
        #     # wget.download(url, out_file)
        # except Exception as e:
        #     print(e)
        #     print(f"Failed to download {url} to {out_file}")


if __name__ == "__main__":
    # argument parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pheno_file", type=str)
    parser.add_argument("out_dir", type=str)
    parser.add_argument("--pipe", type=str, default="dparsf")
    parser.add_argument("--roi", type=str, default="rois_cc200")
    parser.add_argument("--fg", type=str, default="filt_noglobal")
    args = parser.parse_args()

    download_abide1_roi(
        args.pheno_file,
        args.out_dir,
        args.pipe,
        args.roi,
        args.fg)
