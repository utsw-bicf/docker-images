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
        print(
            "Usage python3 scripts/getLatestPaths.py <docker_owner> <relations.yaml path>")
        sys.exit(1)
    else:
        owner = sys.argv[1]
        relations = load_yaml(os.path.abspath(sys.argv[2]))
        latest_images = relations['latest']
        test_path = os.getcwd()
        print(test_path, file=sys.stderr)
        for image in latest_images:
            tag = latest_images[image]
            image_name = "{}/{}:{}".format(owner, image, tag).replace("+", "_")
            image_path = os.path.abspath(image + "/" + tag + "/unittest.yml")
            if os.system("docker pull " + image_name) != 0:
                print("ERROR: Unable to build " + image_name)
                sys.exit(1)
            if os.system("python3 tests/test_dockerfiles.py \"" +
                      owner + "\" \"" + image_path + "\"") != 0:
                print ("ERROR: Image testing failed for " + image_name)


if __name__ == "__main__":
    main()
