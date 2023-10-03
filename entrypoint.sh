#!/bin/sh -l
pwd
ls -a
cd ../..
ls -a
cd /github/workspace

echo "extra_metadata is" $1

#install pip requirements
pip install -r requirements.txt --no-cache-dir

# copy over the extra metadata file if it exists to the main directory
if [ -f $1 ]; then
    cp $1 /github/workspace/extra_metadata.json
    #run the main python file
    python main.py --extra_metadata extra_metadata.json
else
    #run the main python file
    python main.py
fi