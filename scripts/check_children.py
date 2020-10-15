#!/usr/bin/env python3
"""
Checks a relations.yaml file for any child images, and returns the list of child images if any found
"""

# Imports
import os
import sys
import re
import yaml
from update_relations import load_yaml

# Global variables
RELATION_FILENAME = "relations.yaml"


# Methods
def update_children(image_name, image_version):
    """
    Takes the image name and version, increments it, and returns an updated child image name
    :param image_name: str : Name of the Docker image to be incrimented
    :param image_version: str : Version number to incriment
    """
    print("Child image:\t{}\nChild version:\t{}\n".format(
        image_name, image_version))


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
        print(DOCKERFILE_PATH)
        image_name = re.split('/|\\\\', DOCKERFILE_PATH)[-3]
        image_version = re.split('/|\\\\', DOCKERFILE_PATH)[-2]
        children = get_children(image_name, image_version)
        print(children)
        for child in children:
            print(child)
            if child is None:
                continue
            else:
                child_image = re.split(':', child)[0]
                print(child_image)
                child_version = re.split(':', child)[1]
                if (is_terminated(child_image)):
                    print(
                        "This image has been flagged as not to be automatically updated, skipping.")
                    exit()
                else:
                    update_children(child_image, child_version)


if __name__ == "__main__":
    main()
