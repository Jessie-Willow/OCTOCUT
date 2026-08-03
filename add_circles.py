import matplotlib.pyplot as plt
import matplotlib.image as mpimage
from matplotlib.lines import Line2D
import matplotlib.patches as mppatches
from PIL import Image
from sdss import Region
from dl import queryClient as qc
import pandas as pd
from io import StringIO
import numpy as np
def region(ra, dec, size):
    deg=size/60
    ra_min=ra-deg
    ra_max=ra+deg
    dec_min=dec-deg
    dec_max=dec+deg
    return ra_min, ra_max, dec_min, dec_max
def convert_xy(table,centre,size,pixels):
    degrees=size/60
    table["x_pos"]=np.zeros(len(table))
    table["y_pos"]=np.zeros(len(table))
    table["x_pos"]=(((centre[0]-table["ra"])/degrees)*pixels*np.cos(table["dec"]*2*np.pi/360))+(pixels/2)
    table["y_pos"]=(((centre[1]-table["dec"])/degrees)*pixels)+(pixels/2)
    return(table)
def SDSS_circles(ra,dec,pos_err,ra2,dec2,pos_err2,size,pixels,img,image_path):
    print("Plotting circles")
    degrees=size/60
    print(ra,dec,ra2,dec2)
    radius_pixels= pos_err*pixels/(size*60)
    radius_pixels2= (pos_err2*pixels/(size*60))*np.cos(dec2*2*np.pi/360)
    centre=(pixels/2,pixels/2)
    fig= plt.figure(figsize=(10,10),dpi=pixels/10)
    ax= plt.Axes(fig, [0, 0, 1, 1])
    fig.add_axes(ax)
    ax.imshow(img, aspect= 'equal')
    ax.set_axis_off()
    rosat_centre=(round(((ra-ra2)/(degrees))*pixels*np.cos(dec2*2*np.pi/360))+(pixels/2),round(((dec-dec2)/(degrees))*pixels)+(pixels/2))
    print(rosat_centre)
    p = mppatches.Circle(
        rosat_centre,radius= radius_pixels2,linestyle= ":",ec= "red",linewidth= 2,fc= 'none')
    ax.add_patch(p)
    q = mppatches.Circle(
        (round(centre[0], 0), round(centre[1], 0)),radius= radius_pixels,linestyle= ":",ec= "green",linewidth= 5,fc= 'none')
    ax.add_patch(q)
    reg = Region(ra, dec, fov=degrees)
    df_obj = reg.nearest_objects()
    df_obj=convert_xy(df_obj,(ra,dec),size,pixels)
    for index,row in df_obj.iterrows():
        p = mppatches.Circle((round(row["x_pos"]), round(row["y_pos"])),radius=10,ec= "tab:blue",linewidth= 2,fc= 'none')
        ax.add_patch(p) 
    plt.savefig(image_path)
    plt.close(fig)
def DES_circles(ra,dec,pos_err,size,pixels,img,image_path):
    print("Plotting circles")

    radius_pixels= pos_err*pixels/(size*60)
    center=(pixels/2,pixels/2)
    fig= plt.figure(figsize=(10,10),dpi=pixels/10)

    ax= plt.Axes(fig, [0, 0, 1, 1])
    fig.add_axes(ax)
    ax.imshow(img, aspect= 'equal')
    ax.set_axis_off()
  
    p = mppatches.Circle(
        (round(center[0], 0), round(center[1], 0)),radius= radius_pixels,linestyle= ":",ec= "green",linewidth= 5,fc= 'none')
    ax.add_patch(p)
    ra_min,ra_max,dec_min,dec_max=region(ra,dec,size)
    result=qc.query(sql=f'SELECT ra,dec from des_dr2.main where ra between {ra_min} and {ra_max} and dec between {dec_min} and {dec_max}', database='des_dr1')
    csv_file_like = StringIO(result)

    df_obj = pd.read_csv(csv_file_like)
    df_obj=convert_xy(df_obj,(ra,dec),size,pixels)
    for index,row in df_obj.iterrows():
        p = mppatches.Circle((round(row["x_pos"]), round(row["y_pos"])),radius=10,ec= "tab:blue",linewidth= 2,fc= 'none')
        ax.add_patch(p)  
    plt.savefig(image_path)
    plt.close(fig)