#!/bin/sh -l
pwd
ls -a
cd ../..
echo "extra_metadata is" $1
#install pip requirements
pip install -r requirements.txt --no-cache-dir

#copy over main.py and /src/rocrate.py to the github workspace
cp main.py github/workspace

cd github/workspace
mkdir src
cd ../..
cd src
cp rocrate.py ../github/workspace/src
cd ..
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

#delete main.py and /src/rocrate.py from the github workspace
rm main.py
rm -rf src