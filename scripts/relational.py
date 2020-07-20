#!/usr/bin/env python3
"""
Receives a Dockerfile, and adds relevant information to the relations.yaml file including:
    1) The parent image
    2) The child image string for the parent image
    3) Any information found about images downstream to this image
"""

import os
import sys
import re
import yaml

RELATION_FILENAME = "relations.yaml"

def check_parents():
    """
    Verifies that the parent images seen are the ones expected.
    """
    listed_parents = ORIDATA['images'][DOCKER_IMAGE][IMAGE_VERSION]['parents']
    found_parents = []
    with open(DOCKERFILE_PATH, "r") as dockerfile:
        for line in dockerfile:
            if 'FROM ' in line:
                found_parents += [line.split()[1].split('/')[-1]]
    for parent in found_parents:
        print("Verifying parent: " + parent)
        if not parent in listed_parents:
            sys.exit("Warning, Dockerfile lists " + parent + " as a parent image, but this is not listed in the YAML file.\nPlease re-version this image appropriately, as changes in parents may cause unforseen functionality changes.")
        else:
            print("Parent images validated, no changes made to relations.yaml") 

def update_table(mod_image, mod_version, parent_images, child_images):
    """
    Updates any changes to the image passed to it with the information passed to it
    :param mod_image: str image name to be modified
    :param IMAGE_VERSION: str image version to be modified
    :param parent_images: str[] list of images that should be input as the parent images
    :param child images: str[] list of images that should be input as the child images
    """
    new_image = {
        mod_image: {
            mod_version: {
                'parents': parent_images,
                'children': child_images
            }
        }
    }
    NEWDATA['images'].append(new_image)

def update_ancestry(parent):
    """
    Finds the parent images to the called image, and updates their child field to include the new\
        image
    :param parent: str the parent image ID to be updated
    :param IMAGE_VERSION: str the parent image version number to be checked
    """
    parent_image = parent.split(':')[0]
    parent_version = parent.split(':')[1]
    new_child_image = DOCKER_IMAGE + ':' + IMAGE_VERSION
    new_child = ''
    if parent_image in ORIDATA['images']:
        new_child = ORIDATA['images'][parent_image][parent_version]['children']
        if new_child == 'none':
            new_child = [new_child_image]
        else:
            new_child += [new_child_image]
    update_table(parent_image, parent_version, \
        ORIDATA['images'][parent_image][parent_version]['parents'], new_child)

def update_parent():
    """
    Finds the information regarding the parents entry for the new image
    :param DOCKERFILE_PATH: str path to the Dockerfile to be searched
    :param IMAGE_VERSION: str image version number to be checked, used as sub-entry to main image
    """
    parents = []
    with open(DOCKERFILE_PATH, "r") as dockerfile:
        for line in dockerfile:
            if 'FROM ' in line:
                parents += [line.split()[1].split('/')[-1]]
    for parent in parents:
        update_ancestry(parent)
    return parents

#Reads the Dockerfile to find the parent image, if there is any, and puts that information into
#the yaml file.    It assumes no child images, since this is a new image.
def build_entry(child_images):
    """
    Reads the Dockerfile to find the parent image, if any.
    :param DOCKERFILE_PATH: str path to the Dockerfile to be read
    :param IMAGE_VERSION: str image version to be used for the new entry
    :param child_images: str list of all child images to be added
    """
    parent = update_parent()
    update_table(DOCKER_IMAGE, IMAGE_VERSION, parent, child_images)

def write_new_yaml():
    """
    Overwrites the existing relations.yaml, should only be called once
    """
    yaml_file = open(RELATION_FILENAME, "w")
    yaml.safe_dump(NEWDATA, yaml_file)
    yaml_file.close()

def check_image_exists():
    """
    Finds any existing images for the Dockerfile.    If an image is found with the name provided,\
    it validates the information.    Otherwise, it creates a new table entry in the yaml.
    :param DOCKERFILE_PATH: str path to the Dockerfile to be entered
    :param IMAGE_VERSION: str image version for the associated Dockerfile
    """
    if DOCKER_IMAGE in ORIDATA['images']:
        print("Existing image found, verifying version information")
        if not IMAGE_VERSION in ORIDATA['images'][DOCKER_IMAGE]:
            print("This appears to be an update to an existing image, running updater.")
            build_entry("none")
            write_new_yaml()
        else:
            print("This image and version already appear in relations.yaml, verifying information.")
            check_parents()
    else:
        print("New image detected, building parent-child tree.")
        build_entry("none")
        write_new_yaml()

def main():
    """
    Main method
    """
    global DOCKER_IMAGE
    global ORIDATA
    global NEWDATA
    global DOCKERFILE_PATH
    global IMAGE_VERSION
    if len(sys.argv) < 1:
        print("Usage python3 scripts/relational.py <DOCKERFILE_PATH>")
        sys.exit(1)
    else:
        DOCKERFILE_PATH = os.path.abspath(sys.argv[1])
        DOCKER_IMAGE = re.split('/', DOCKERFILE_PATH)[-3]
        IMAGE_VERSION = re.split('/', DOCKERFILE_PATH)[-2]
        with open(RELATION_FILENAME) as yaml_file:
            ORIDATA = yaml.safe_load(yaml_file)
        yaml_file.close()
        with open(RELATION_FILENAME) as yaml_file:                                                                                                     NEWDATA = yaml.safe_load(yaml_file)
        yaml_file.close()
        check_image_exists()

if __name__ == "__main__":
    main()
