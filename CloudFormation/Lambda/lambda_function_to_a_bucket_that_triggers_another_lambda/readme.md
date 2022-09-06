# LAMBDA Function with source code loaded into the function with a ZIP file.

## Steps
- Create a bucket called "col-code-repo-for-lambda". Note the name of the bucket as you will refer to this in the cloud formation template.
- ZIP all the items under the "src" folder and create a zip file called "my_code.zip". Note this name as the template will require the name.


## Things to consider
- The source must be called index.js in the "src" folder.
- You can add more files and directories to the src folder to include node packages.
- All items that is needed to deploy is in the "template" folder.
