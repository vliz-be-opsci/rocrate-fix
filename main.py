# this python file is the main file for the project
# it will be used to run over all the files that are present in the directory

import sys
from src.rocrate import rocrate


# main function
def main():
    rocrate_extra_metadata = ""
    if len(sys.argv) > 1:
        rocrate_extra_metadata = sys.argv[1]
    rocrate(rocrate_extra_metadata)


if __name__ == "__main__":
    main()
