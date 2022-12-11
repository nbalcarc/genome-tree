import os
import shutil
import tempfile
from zipfile import ZipFile


def preprocess(file_dir: str) -> str:
    '''Removes all irrelevant information from the given genome file'''
    
    with open(file_dir, 'r') as file:
        with open(file_dir + ".copy", 'w') as file1:
            for line in file.readlines():
                if not line.startswith('>'): #all irrelevant lines start with >
                    file1.write(line)
    return file_dir + ".copy"


def main():
    '''Entry point for program'''
    
    basedir = os.getcwd() + "/"
    genomes_dir = basedir + "genomes"
    genomes_raw_dir = basedir + "genomes_raw"
   
    # notify user if no genomes_raw folder
    if not os.path.isdir(genomes_raw_dir):
        print("ERROR: The genomes_raw folder does not exist!")
        return
    
    # reset the genomes folder
    if os.path.isdir(genomes_dir):
        shutil.rmtree(genomes_dir)
     
    os.makedirs(basedir + "genomes") #create the genomes folder
    zipdir = tempfile.mkdtemp() #create a temporary folder to unzip our genomes
    
    # iterate through all files in the folder
    for file in os.listdir(genomes_raw_dir):
        file_clipped = file[:-4]
        
        # unzip the folder
        with ZipFile(genomes_raw_dir + "/" + file, 'r') as zipfile:
            os.makedirs(genomes_dir + "/" + file_clipped)
            zipfile.extractall(zipdir + "/" + file) #ensure no two unzipped folders overlap
        
        # iterate through all files in the extracted location (the file ends with .fna but the name could be anything)
        genome_location = zipdir + f"/{file}/ncbi_dataset/data/{file_clipped}/"
        for tfile in os.listdir(genome_location):
            
            # if this isn't the file we're looking for, skip
            if tfile[tfile.rfind('.'):] != ".fna":
                continue
            
            genome_file = preprocess(genome_location + tfile) #preprocess the file before copying
            shutil.copyfile(genome_file, genomes_dir + "/" + file_clipped + "/" + tfile) #copy the file into the output
    

if __name__ == "__main__":
    main()
