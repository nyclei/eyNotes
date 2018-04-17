#!/usr/bin/env python

import urllib
import json
from distutils.version import LooseVersion
from string import Template
import argparse
import sys
import os

""" constants
"""
REGISTRY_BASE_V2_URL = "https://awssandbox.registry.rccl.com/v2"
CATALOG_URL = REGISTRY_BASE_V2_URL + "/_catalog"
DELETE_TEMPLATE = Template("delete_docker_registry_image.py --image $image:$version")
DRYRUN_FLAG = " --dry-run"


""" function : lessThan
"""
greaterThan = lambda x, y: LooseVersion(x).__cmp__(y)


""" function : greaterThan
"""
def lessThan(x, y):
    return -greaterThan(x, y)


""" function : get sorted removable command
"""
def getRemovableImageTags(imageName, numberToKeep, dryRun=True):
    tagListUrl = REGISTRY_BASE_V2_URL + "/" + imageName + "/tags/list"
    response = urllib.urlopen(tagListUrl)
    j_data = json.loads(response.read())
    versions = [] 
    for tag in j_data['tags']:
        versions.append(str(tag))

    versions.sort(lessThan)

    for tag in versions[0:numberToKeep]:
        deleteCmd = DELETE_TEMPLATE.substitute(image=imageName, version=tag)
        if(dryRun):
            deleteCmd += DRYRUN_FLAG
        print ("#[KEEP] > " + deleteCmd)

    for tag in versions[numberToKeep:]:
        deleteCmd = DELETE_TEMPLATE.substitute(image=imageName, version=tag)
        if(dryRun):
            deleteCmd += DRYRUN_FLAG
        print ("#[DELETE] > " + deleteCmd)
        os.system(deleteCmd)
        os.system("sleep 2")


""" parsing v2 catalog
"""
def probeCatalog(numberToKeep):
    CATALOG_URL = REGISTRY_BASE_V2_URL + "/_catalog"
    response = urllib.urlopen(CATALOG_URL)
    j_data = json.loads(response.read())
    for imageName in j_data['repositories']:
        getRemovableImageTags(imageName, numberToKeep, False)


""" Validate docker registry path
"""
def validateRegistryDataPath():
    if not 'REGISTRY_DATA_DIR' in os.environ:
        print "The environment setting of 'REGISTRY_DATA_DIR' is not set yet"
        print "Set it with '. ./setRegDataPath.sh' "
        sys.exit(1)

    regDataDir = os.environ['REGISTRY_DATA_DIR']
    print "Path to registry data is set to: \"" + regDataDir +"\""

    if not(os.path.isdir(regDataDir + "/blobs") and os.path.isdir(regDataDir + "/repositories" )):
        print "The environment setting of 'REGISTRY_DATA_DIR' misses subfolders 'blogs' or 'repositories'. Exit"
        sys.exit(1)

def main():

    if os.geteuid() != 0:
        print "You need to have root privileges to run this script."
        sys.exit(0)
    validateRegistryDataPath()

    parser = argparse.ArgumentParser(description="Cleanup docker registry")
    parser.add_argument("-d", "--registry_data_dir",
                        dest="dir",
                        required=False,
                        help="Path to registry data")
    parser.add_argument("-n", "--number_of_images_to_keep",
                        dest = "numberToKeep",
                        required = True,
                        help="Number of TAGs for each image to keep")
    args = parser.parse_args()
    keep = int(args.numberToKeep)

    if(keep <= 0):
        probeCatalog(1)
    else:
        probeCatalog(int(args.numberToKeep))





""" Main Entry
"""
if __name__ == "__main__":
    main()

