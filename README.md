# rocrate-fix
A gh-action that will add missing files to a rocrate and will add metadata to a rocrate.

## Usage

## what to write in the extra metadata file

The extra metadata file is a json file

each key of the json file can be used as the follwoing:

* start with '_:' : this will be used as a blank node
    * example: "_:blanknode1": {"@type": "dcat:Distribution", "dcat:accessURL": "https://example.com"}
    * This can be used to update or add a node to the @graph
* start with ./ : this will be used as a file path
    * example: "./file1.json": {"@type": "dcat:Distribution", "dcat:accessURL": "https://example.com"}
    * This can be used to update an existing file. If the file does not exist it won't be added to the @graph
* regex expression: this will be used to match a file path
    * example: "(.*)\\.txt$": {"@id": "_:test"}
    * In the example above all files that end with .txt will be matched and the @id will be added to the @graph of all the matched files
    * This can be used to update any existing file or blank node. (useful for large rocrates)


