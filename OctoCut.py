import sys
import pandas as pd
import requests
import os
import numpy as np
import argparse
import add_circles
parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument("--infile",help="The input file of objects you want cutouts of. Must be csv with RA and DEC columns")
parser.add_argument("--outdir",help="File you want to store retrieved images in")
parser.add_argument("--survey",help="keyword of survey you want to access. currently supports DSS,SDSS,LEGACY,PANSTARR,DES")
parser.add_argument("--all",help="Alternative to individually specifying surveys",default="n")
parser.add_argument("--size",help="size of image in arcminutes", default=3)
parser.add_argument("--pixels",help="Number of pixels to use in cutout. Output is always square.", default=512)
parser.add_argument("--circles",help="Whether to add object circles from survey catalogue. only available for SDSS so far. enter y/n", default="n")
args = parser.parse_args()
survey_dict={"DSS":f"CDS%2FP%2FDSS2%2Fcolor","PANSTARR":f"CDS%2FP%2FPanSTARRS%2FDR1%2Fcolor-i-r-g","SDSS":f"CDS%2FP%2FSDSS9%2Fcolor","LEGACY":f"CDS%2FP%2FDESI-Legacy-Surveys%2FDR10%2Fcolor","DES":f"CDS%2FP%2FDES-DR2%2FColorIRG"}
data= pd.read_csv(args.infile)

def retrieve_image(ra, dec,surv, scale= 0.35, width= 512, height= 512):

    image_url= (f"https://alasky.cds.unistra.fr/hips-image-services/hips2fits?hips={surv}&width={width}&height={height}&fov={float(args.size)/60}&projection=SIN&coordsys=icrs&rotation_angle=0.0&ra={ra}&dec={dec}&format=jpg")
    return image_url

def extract_images(surv_name,surv_loc):
    counter= 1
    output_dir= args.outdir+"/"+surv_name
    os.makedirs(output_dir, exist_ok= True)
    for index, row in data.iterrows():     #iteration over the CSV rows
        name= row['XCS_ID']
        ra= row['RA'] 
        dec= row['DEC']
        print(f"Getting image at {ra},{dec}")
        image_url= retrieve_image(ra, dec,surv_loc,width=args.pixels,height=args.pixels)
        response= requests.get(image_url)
        if response.status_code == 200:
            image_path= os.path.join(output_dir, f"{surv_name}_{int(name)}.jpg")
            counter+= 1
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"Saved image for {name} at {image_path}")
            if args.survey=="SDSS" and args.circles=="y":
                add_circles.SDSS_circles(ra,dec,row["POS_ERR"],row["RA_2"],row["DEC_2"],row["POSITIONAL_UNCERTAINTY"],int(args.size),args.pixels,image_path)
            elif args.circles=="y":
                print("Object identification not available for this survey yet.")


        else:
            print(f"Failed to retrieve image for {name} (RA: {ra}, DEC: {dec})")
            
    print("Image retrieval complete!")
if args.all=="y":
    for item in survey_dict:
        extract_images(item,survey_dict[item])
else:
    extract_images(args.survey,survey_dict[args.survey])
    