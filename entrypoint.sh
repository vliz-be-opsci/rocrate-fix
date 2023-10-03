#!/bin/sh -l
pwd
ls -a
cd ../..
echo "extra_metadata is" $1
#install pip requirements
pip install -r requirements.txt --no-cache-dir

#copy over main.py and /src/rocrate.py to the github workspace
cp main.py github/workspace
cp src/rocrate.py github/workspace

cd github/workspace
ls -al
# copy over the extra metadata file if it exists to the main directory
if [ -f $1 ]; then
    cp $1 extra_metadata.json
    #run the main python file
    python main.py --extra_metadata extra_metadata.json
else
    #run the main python file
    python main.py
fi