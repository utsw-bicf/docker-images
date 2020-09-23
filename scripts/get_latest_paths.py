#!/usr/bin/env python3
"""
Prints out the paths for the unittest.yml files for all latest images to run their pytests
"""

import os
import sys
import re
import yaml
from check_pre_exist import load_yaml

def main():
    """
    Main method
    
    """
    if len(sys.argv) < 1:
        print("Usage python3 scripts/getLatestPaths.py <relations.yaml path>")
        sys.exit(1)
    else:
        relations = load_yaml(os.path.abspath(sys.argv[1]))
        latest_images = relations['latest']
        print("Loaded yaml:\n" + latest_images)
        for image in latest_images:
            print (image, file = sys.stderr)
            image_path = image + "/" + latest_images[image] + "/unittest.yml"
            print(image_path)
