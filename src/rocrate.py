#this file wil lcontain the class that will be used to manipulate the rocrate

import os
import sys
import time
import json
import validators
import regex as re

class rocrate():
    def __init__(self,extra_metadata):
        self.extra_metadata_file = extra_metadata
        self.rocrate_json = {}
        print("rocrate class created")
        self.load_rocrate()
        self.complete_metadata_crate()
        self.load_rocrate()
        print(self.extra_metadata_file)
        if self.extra_metadata_file != "" and self.extra_metadata_file != "--extra_metadata":
            self.extra_metadata_json()
            self.add_extra_metadata()
            self.save_rocrate()
        
    def extra_metadata_json(self):
        '''
        description: this function will be used to display json representation of the extra metadata file
        input: self.extra_metadata_file
        output: self.extra_metadata_file_json
        '''
        #load in the extra_metadata_file with is a file
        with open(os.path.join(os.getcwd(),self.extra_metadata_file), "r") as extra_metadata_file:
            self.extra_metadata_file_raw = extra_metadata_file.read()
        self.extra_metadata_file_json = json.loads(self.extra_metadata_file_raw)
        print(self.extra_metadata_file_json)
    
    def load_rocrate(self):
        '''
        description: this function will be used to load the rocrate file
        input: self.rocrate_json
        output: self.rocrate_json
        '''
        print(os.getcwd())
        #open file os.path.join(os.getcwd(), "ro-crate-metadata.json")
        with open(os.path.join(os.getcwd(), "ro-crate-metadata.json"), "r") as rocrate_file:
            self.rocrate_json = json.load(rocrate_file)
        print(self.rocrate_json)
        
    def add_extra_metadata(self):
        '''
        description: this function will be used to add extra metadata to the rocrate
        input: self.extra_metadata_file_json
        output: self.rocrate_json
        '''
        #go over all the keys in the extra_metadata_file_json and search if the same key is in the self.rocrate_json["@graph"]
        #if yes then add the value of the key to the self.rocrate_json["@graph"]
        #if not check if the key to be added is a blank node or not 
        # if yes then add the key to the self.rocrate_json["@graph"]
        for key, value in self.extra_metadata_file_json.items():
            found = False
            for node in self.rocrate_json["@graph"]:
                print(node)
                if node["@id"] == key:
                    #merge the value of the key with the node
                    node.update(value)
                    found = True
                
                #check the node id as a regex expression of the key
                #check if key doesn't start with ./ or _:
                if key.startswith("./") == False  and key.startswith("_:") == False:
                    regex = re.compile(key)
                    if regex.match(node["@id"]):
                        #merge the value of the key with the node
                        node.update(value)
                        found = True
            
            if not found:
                #add the key to the self.rocrate_json["@graph"] if it is a blank node
                if key.startswith("_:"):
                    toappend = {"@id": key}
                    toappend.update(value)
                    self.rocrate_json["@graph"].append(toappend)
                
        
        print(self.rocrate_json)
    
    def save_rocrate(self):
        '''
        description: this function will be used to save the rocrate file
        input: self.rocrate_json
        output: self.rocrate_json
        '''
        with open(os.path.join(os.getcwd(), "ro-crate-metadata.json"), "w") as rocrate_file:
            json.dump(self.rocrate_json, rocrate_file, indent=4)
            
        print("rocrate saved")
        
    def complete_metadata_crate(self):
        #get the metadata rocrate metadata file
        data = self.rocrate_json

        #make variable for the new metadata file
        try:
            #take the old metadata file that is not @graph and put it in a new variable
            new_data = {}
            for key, value in data.items():
                if key != "@graph":
                    new_data[key] = value
                if key == "@graph":
                    #go over each item in the graph and only append the one where "@id" => "./ro-crate-metadata.json"    
                    for item in value:
                        if item["@id"] == "./ro-crate-metadata.json":
                            new_data["@graph"] = [item]
                            break
            print(new_data)
        except Exception as e:
            print("An error occured while loading the new metadata file")
            print(f"error: {e}")
            print(e)
            return

        #make variables that contain all the nodes from the graph that aren't a file and a variable that contains all the nodes in the graph that are files
        try:
            other_nodes = [node for node in data["@graph"] if node["@type"] != "File"]
            print(other_nodes)
            files_nodes = [node for node in data["@graph"] if node["@type"] == "File"]
            print(files_nodes)
        except Exception as e:
            print("An error occured while trying to get the nodes from the graph")
            print(f"error: {e}")
            print(e)
            return

        #make relations list variabe that is comprised of all parent_folder, relative_path and name of all the files present on the local storage of the user
        try:
            relation = []
            for root, dirs, files in os.walk(os.path.join(os.getcwd()), topdown=False): 
                
                #check if the root path begins with src or venv and if so skip the iteration
                if root.startswith(os.path.join(os.getcwd(), "src")) or root.startswith(os.path.join(os.getcwd(), "venv")):
                    continue
                                
                #make a print that shows the root path but split by the os.getcwd()
                last_part_root = root.split(os.getcwd())[-1]
                current_folder_name = os.path.split(last_part_root)[-1]
                full_relative_folder = last_part_root[1:]
                #replace os.path.sep by "/"
                old_full_relative_folder = full_relative_folder
                full_relative_folder = full_relative_folder.replace(os.path.sep, "/")
                #check if full_relative_folder is empty, if so, set it to ./
                if full_relative_folder == "":
                    print(f"nothing root : {root}")
                    parent = "./"
                    for file in files:
                        # if the path is action.yml | Dockerfile | entrypoint.sh | README.md | requirements.txt | main.py | extra_metadata.json | .gitignore then skip the iteration
                        # if root is cwd and file is mentioned from above then skip the iteration
                        if root == os.getcwd() and (file == "action.yml" or file == "Dockerfile" or file == "entrypoint.sh" or file == "README.md" or file == "requirements.txt" or file == "main.py" or file == "extra_metadata.json" or file == "dev-requirements.txt" or file == ".gitignore" or file == ".env"):
                            continue
                        
                        if " " in file:
                            new_file = file.replace(" ", "_")
                            old_file = os.path.join(root, file)
                            new_file = os.path.join(root, new_file)
                            print(f"old_file: {old_file}")
                            print(f"new_file: {new_file}")
                            os.rename(old_file, new_file)
                            file = new_file
                        #get the relative path of the file , the parent relative direcotry
                        label_file = os.path.join(parent, file)
                        label_file = label_file.replace(" ", "_")
                        label_file = label_file.replace(os.path.sep, "/")
                        print(f"label_file: {label_file}")
                        relation.append({"label":label_file, "parent":parent, "file":file})
                    # go to the next iteration of the loop
                    continue
                
                #check if full_relative_folder does not start with "."
                if full_relative_folder[0] != ".":
                    print(f"no . root : {root}")
                    parent = "./" + full_relative_folder + "/"
                    print(f"full_current_folder: {root}")
                    #check if there are spaces in the lastpart of the root path split by os.path.sep and if so replace them with _
                    if " " in current_folder_name:
                        current_folder_name = current_folder_name.replace(" ", "_")
                        root_without_last_folder = root.split(os.path.sep)[:-1]
                        new_root = os.path.sep.join(root_without_last_folder + [current_folder_name])
                        print(f"new_root: {new_root}")
                        os.rename(root, new_root)
                        root = new_root
                    #go over each file and first check if there are no spaces in the file location 
                    for file in files:
                        if " " in file:
                            new_file = file.replace(" ", "_")
                            old_file = os.path.join(root, file)
                            new_file = os.path.join(root, new_file)
                            print(f"old_file: {old_file}")
                            print(f"new_file: {new_file}")
                            os.rename(old_file, new_file)
                            file = new_file
                        #get the relative path of the file , the parent relative direcotry
                        label_file = os.path.join(parent, file)
                        label_file = label_file.replace(" ", "_")
                        label_file = label_file.replace(os.path.sep, "/")
                        print(f"label_file: {label_file}")
                        relation.append({"label":label_file, "parent":parent, "file":file})
            print(f"relation: {relation}")
        except Exception as e:
            print("An error occured while trying to get the relations list")
            print(f"error: {e}")
            print(e)
            return {"error": "An error occured while trying to fix the rocrate , make sure you don't have the file explorer open of the current rocrate {os.getcwd()}"}
            
        #go over all relations and check if relation["parent"] is in the other_nodes that are of type dataset
        try:
            all_datasets_added = []
            for rel in relation:
                added_via_other_node = False
                parent = rel["parent"]
                if parent in all_datasets_added:
                    continue
                print(f"parent: {parent}")
                for node in other_nodes:
                    if node["@type"] == "Dataset":
                        #chekc first if the id_to_check is not a url
                        if validators.url(node["@id"]):
                            new_data["@graph"].append(node)
                            added_via_other_node = True
                            break
                        if node["@id"] == parent:
                            #TODO discuss with marc if we should use an uuid or not as the id and then the real name as the label?
                            new_data["@graph"].append({"@id":node["@id"], "@type":node["@type"], "label":node["@id"], "hasPart":[]})
                            added_via_other_node = True
                            break   
                
                if not added_via_other_node:
                    new_data["@graph"].append({"@id":parent, "@type":"Dataset", "label":parent, "hasPart":[]})
                all_datasets_added.append(parent)    
        except Exception as e:
            print("An error occured while trying to add the dataset nodes to the new metadata file")
            print(f"error: {e}")
            print(e)
            return

        #go over the relation list again and add the parent to the parent folder of the parent
        try:
            all_parents_added = []
            for rel in relation:
                parent = rel["parent"]
                parent_splitted = parent.split("/")
                parent_of_parent = "/".join(parent_splitted[:-2]) + "/"
                if parent not in all_parents_added:
                    for node in new_data["@graph"]:
                        if node["@id"] == parent_of_parent:
                            node["hasPart"].append({"@id":parent})
                            all_parents_added.append(parent)
                            break
        except Exception as e:
            print("An error occured while trying to add the parent to the parent folder of the parent")
            print(f"error: {e}")
            print(e)
            return

        #go over all the other_nodes and do the same but for the ones that are not a dataset
        try:
            for node in other_nodes:
                if node["@id"] == "./ro-crate-metadata.json":
                    continue
                id_to_check = node["@id"]
                if "label" in node:
                    id_to_check = node["label"]
                if node["@type"] != "Dataset":
                    print(node)
                    if "label" not in node:
                        node["label"] = node["@id"]
                    new_data["@graph"].append(node)
        except Exception as e:
            print("An error occured while trying to add the non dataset nodes to the new metadata file")
            print(f"error: {e}")
            print(e)
            return
        
        #go over all the files_nodes and check in the relation list if the label of the file is in files_nodes["@id"] => if found then add the file from files_nodes to the new_data["@graph"]
        try:
            for rel in relation:
                found = False
                for file_node in files_nodes:
                    if rel["label"] == file_node["@id"]:
                        found = True
                        #check first if ref["@label"] is already in teh graph
                        for node in new_data["@graph"]:
                            if node["@id"] == file_node["@id"]:
                                break
                        if "label" not in file_node:
                            file_node["label"] = file_node["@id"]
                        new_data["@graph"].append(file_node)
                        #add the file to the dataset hasPart
                        for parentnode in new_data["@graph"]:
                            if parentnode["@id"] == rel["parent"]:
                                parentnode["hasPart"].append({"@id":file_node["@id"]})
                                break
                        break
                if not found:
                    if rel["label"] == "./ro-crate-metadata.json":
                        continue
                    new_data["@graph"].append({"@id":rel["label"], "@type":"File", "label":rel["label"]})
                    #add the file to the dataset hasPart
                    for parentnode in new_data["@graph"]:
                        if parentnode["@id"] == rel["parent"]:
                            parentnode["hasPart"].append({"@id":rel["label"]})
                            break
        except Exception as e:
            print("An error occured while trying to add the files nodes to the new metadata file")
            print(f"error: {e}")
            print(e)
            return
        
        # This part will go over the new_data["@graph"] and check if the name starts with ./src or ./venv
        # if the node name is also one of the following then remove it from the new_data["@graph"]
        # ./.env | ./action.yml | ./Dockerfile | ./entrypoint.sh | ./README.md | ./requirements.txt | ./main.py | extra_metadata.json | ./.gitignore
        new_graph_data = []
        for item in new_data["@graph"]:	
            check = True
            #perform @id name check
            if item["@id"].startswith("./src") or item["@id"].startswith("./venv"):
                check = False
            if item["@id"] == "./.env" or item["@id"] == "./action.yml" or item["@id"] == "./Dockerfile" or item["@id"] == "./entrypoint.sh" or item["@id"] == "./README.md" or item["@id"] == "./requirements.txt" or item["@id"] == "./dev-requirements.txt" or item["@id"] == "./main.py" or item["@id"] == "./extra_metadata.json" or item["@id"] == "./.gitignore":
                check = False
            if check:
                new_graph_data.append(item)
        
        new_data["@graph"] = new_graph_data
                        
        #pretty print the new_data with identation of 4
        #print(f"new_data: {json.dumps(new_data, indent=4)}")
        self.rocrate_json = new_data
        self.save_rocrate()