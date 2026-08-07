# OCTOCUT
Create and edit optical cutouts for the OCTAVIUS system.
A copy of this code is avilable on the artemis system under /mnt/xmm-xcs/environments/OCTOCUT. Virtual enviroment under .venv

How to make optical images:
Ingredients:
A computer capable of connecting to the Artemis HPC.

Step 1:
Using the terminal, Login to the HPC. you can do that by running
ssh USERNAME@ood.artemis.hrc.sussex.ac.uk.
Replace USERNAME with your sussex username.
This tells the system to connect to the address of artemis using the SSH protocol(secure shell protocol)
You will then be prompted to enter your password. Do it.

Step 2: 
Ensure code is not run on the login node.
You will notice that your shell prompt (the text that appears before you type any commands) contains the word login. This is fine for navigating and finding files, but not for running code, as this can slow down the login node for other users.
To work on a computing node instead, run 
srun --pty bash
This tells Slurm workload manager to allocate a computing node 

Step 3:
Sourcing the virtual environment
To ensure the code continues to work without constant bug fixing, we use a virtual environment which has specific modules and versions loaded. The virtual environment has already been prepared. To find it, we first navigate to directory with all the code we need. To do this, run:
cd /mnt/xmm-xcs/environments/OCTOCUT
Now, you need to actually enter the virtual environment. To do this, run:
source .venv/bin/activate
Your shell prompt now should begin with (DES_Imaging)

Step 4: Running the code
To run python files using bash, we first type python3, this lets bash know that the file we are about to pass it is a python file, which it should run.
The file in question is called OctoCut.py. The simplest thing you can do with this file is run the help command. In this case, type 
python3 OctoCut.py -h
This should now display a list of the arguments that you can pass to OctoCut.py
The three most important are --infile, --outdir, and survey. Infile is the csv file of objects you want to make images of. Outdir is the directory you want to save the images to. A sub directory with the name of the survey will be created in this directory, and the images will be saved there. I strongly recommend using a directory with the same name as your octavius page, under /mnt/xmm-xcs/sussex-octavius. Finally, the survey argument tells the cutout maker which survey to use to make the images. The current allowed ones are DSS,PANSTARR,LEGACY,SDSS,DES. Want something not in this list? Email me at ib317@sussex.ac.uk
So, to use the image maker you need to run the command
python3 OctoCut.py --infile FILEPATH --outdir DIRECTORYPATH --survey SURVEYNAME
The cutout maker will then update you on its progress through the file, including whether each image could be produced and its save location (Double check this is the one you expected!)

