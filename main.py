#this python file is the main file for the project
#it will be used to run over all the files that are present in the directory 

import os
import sys
import time
import json
from src.rocrate import rocrate

#main function
def main():
    print("Welcome to the project")
    #make the rocrate class object
    rocrate_extra_metadata = ""
    if len(sys.argv) > 1:
        rocrate_extra_metadata = sys.argv[1]
    ROCrateObj = rocrate(rocrate_extra_metadata)
    
if __name__ == "__main__":
    main()