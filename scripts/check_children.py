#!/usr/bin/env python3
"""
Checks a relations.yaml file for any child images, and returns the list of child images if any found
"""

# Imports
import os
import sys
import re
import yaml
import numpy as np
from update_relations import load_yaml

# Global variables
RELATION_FILENAME = "relations.yaml"


# Methods
def get_update_type(image_version, prev_version):
    # Split the version numbering to find what type of update was performed
    prev_version_major = int(prev_version.split(sep=".")[0])
    prev_version_minor = int(prev_version.split(sep=".")[1])
    prev_version_patch = int(prev_version.split(sep=".")[2])
    curr_version_major = int(image_version.split(sep=".")[0])
    curr_version_minor = int(image_version.split(sep=".")[1])
    curr_version_patch = int(image_version.split(sep=".")[2])
    # Ensure that the new major version is not less than the old major version
    if (curr_version_major < prev_version_major):
        print("ERROR: New major version number {} is less than the previous major version number {}, this is not allowed!\
            \nPlease re-version your Docker image.".format(curr_version_major, prev_version_major))
        exit(1)
    elif(curr_version_major > prev_version_major):
        print("New major version number detected, re-versioning and creating new child image paths.")
        return 'major'
    else:
        # Do the same with the minor version
        if (curr_version_minor < prev_version_minor):
            print("ERROR: New minor version number {} is less than the previous minor version number {} under the same major version {}, this is not allowed!\
                \nPlease re-version your Docker image.".format(curr_version_minor, prev_version_minor, prev_version_major))
            exit(1)
        elif(curr_version_minor > prev_version_minor):
            print(
                "New minor version number detected, re-versioning and creating new child image paths.")
            return 'minor'
        else:
            # Finally check the patch version, and default to this
            if(curr_version_patch < prev_version_patch):
                print("ERROR: New patch version number {} is less than the previous patch version number {} under the same major-minor version {}.{}, this is not allowed!\
                    \nPlease re-version your Docker image.".format(curr_version_patch, prev_version_patch, curr_version_major, curr_version_minor))
                exit(1)
            else:
                print("Patch detected, creating new child image paths.")
                return 'patch'


def update_children(child_list, update_type):
    """
    Takes the image name and version, increments it, and returns an updated child image name
    :param image_name: str : Name of the Docker image to be incrimented
    :param image_version: str : Version number to incriment
    """
    for child in child_list:
        child_image = re.split(':', child)[0]
        child_version = re.split(':', child)[1]
        # Ensure that the image is not in the terminated list
        if (is_terminated(child_image)):
            print(
                "This image has been flagged as not to be automatically updated, skipping.")
            continue
        else:
            # Get the versioning information from the previous entry
            child_major = int(child_version.split(sep=".")[0])
            child_minor = int(child_version.split(sep=".")[1])
            child_patch = int(child_version.split(sep=".")[2])
            # Re-set the version number to match the change from the previous image to the new image
            if(update_type == 'major'):
                child_major += 1
                child_minor = 0
                child_patch = 0
            elif(update_type == 'minor'):
                child_minor += 1
                child_patch = 0
            else:
                child_patch += 1
            new_child_version = "{}.{}.{}".format(
                child_major, child_minor, child_patch)
            position = child_list.index(child)
            new_child = "{}:{}".format(child_image, new_child_version)
            child_list[position] = new_child
            print("Found child image that will require updating: Update {} to {}".format(
                child, new_child))
    return child_list


def is_terminated(image_name):
    """
    Takes an image and checks to see if it has been marked as terminated, returns true if the image has been designated as not to be updated, false otherwise.
    :param image_name: str : Name of the Docker image to be checked for termination
    """
    if image_name in ORIDATA['terminated']:
        return True
    else:
        return False


def get_children(image_name, image_version):
    """
    Finds any children image in the relations.yaml file
    :param image_name: str : Docker image to get the child images from
    :param image_version: str : Specific version of the image to get the child images from
    """
    if image_name in ORIDATA['images']:
        if image_version in ORIDATA['images'][image_name]:
            return ORIDATA['images'][image_name][image_version]['children']
        else:
            versions = np.array(list(ORIDATA['images'][image_name]))
            prev_version = np.array(versions)[-1]
            update_type = get_update_type(image_version, prev_version)
            update_children(ORIDATA['images'][image_name]
                            [prev_version]['children'], update_type)
            return [None]

    else:
        return [None]


def main():
    """
    Main method
    """
    if len(sys.argv) < 1:
        print("Usage python3 scripts/check_children.py <DOCKERFILE PATH>")
        sys.exit(1)
    else:
        global ORIDATA
        global DOCKERFILE_PATH
        # Setup the global variables
        DOCKERFILE_PATH = os.path.abspath(sys.argv[1])
        ORIDATA = load_yaml()
        image_name = re.split('/|\\\\', DOCKERFILE_PATH)[-3]
        image_version = re.split('/|\\\\', DOCKERFILE_PATH)[-2]
        get_children(image_name, image_version)


if __name__ == "__main__":
    main()
