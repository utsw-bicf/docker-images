#!/usr/bin/env python3
"""
Receives a relations file and a docker image:version combination, and verifies that this image does not already exist in the master branch.
If it exists in master, as these images are meant to be locked down and final, it errors out and tells the user to try another image version.  Otherwise, it allows procedure as normal.
After this, it should build the image, push to DockerHub, and continue as normal.
"""

import os
import sys
import re
import yaml

def check_version_info(master_version, image_version):
     if re.match("[0-9]+\.[0-9]+\.[0-9]+"):
         if image_version.split(sep=".")[0] < master_version.split(sep=".")[0]:
                print("Error: Proposed version number is less than the current master version.\nPlease incriment the version for this image correctly.")
                return False
         elif master_version.split(sep=".")[0] == image_version.split(sep=".")[0]:
                if image_version.split(sep=".")[1] < master_version.split(sep=".")[1]:
                     print("Error: Proposed version number is less than the current master version.\nPlease incriment the version for this image correctly.")
                     return False
                elif  image_version.split(sep=".")[1] == master_version.split(sep=".")[1]:
                     if  image_version.split(sep=".")[2] <= master_version.split(sep=".")[2]:
                          print("Error: Proposed version number is less than or equal the current master version.\nPlease incriment the version for this image correctly.")
                          return False
                     else:
                          print("Versioning appears to have incrimented, proceeding with build.")
                          return True
     else:
          print("Error: the version number does not match our default pattern: '0.0.0'.\nPlease re-name the directory to match this structure.")
          return False

def check_exists(master_yaml, image_name, image_version):
     """
     Checks to see if an image exists as an entry in a yaml file
     :param master_yaml: the yaml file to check for the entry
     :param image_name: the name of the Docker image to search for
     :param image_version: the version of said Docker image to search for
     """
     if image_name in master_yaml['images']:
          print("Found an image with the same name, checking for versions.")
          if image_version in master_yaml['images'][image_name]:
                print ("Error: Found duplicated image and version already present in Master\n\
                     Cannot proceed, please change the image version to avoide overwritting a locked image.")
                return False
          else:
                print ("New version of this image found, verifying that this is an updated version number")
                return check_version_info(master_yaml['images'][image_name][-1], image_version)
     else:
          print("New image found, proceeding with build/push, and updating relations.yaml.")
          return True

def load_yaml(yaml_file):
     """
     Loads a yaml file and returns a python yaml object
     :param yaml_file: the yaml file to open and read
     """
     with open(yaml_file) as yf:
          yaml_data = yaml.safe_load(yf)
     yf.close()
     return yaml_data

def main():
     """
     Main method
     """
     
     if len(sys.argv) < 2:
          print("Usage python3 scripts/check_pre-exist.py <master relations.yaml> <Dockerfile path>")
          sys.exit(1)
     else:
          master_yaml = load_yaml(sys.argv[0])
          image_name = re.split('/', sys.argv[1])[-3]
          image_version = re.split('/', sys.argv[1])[-2]
          if check_exists(master_yaml, image_name, image_version):
                print ("New image found, proceeding to build, push to DockerHub, and add it to the 'relations.yaml' file.")
          else:
                sys.exit(1)

if __name__ == "__main__":
     main()