import os
import sys
import subprocess
import yaml
import re

RELATION_FILENAME = "relations.yaml"

#Reads the Dockerfile to find the parent image, if there is any, and puts that information into the yaml file.  It assumes no child images, since this is a new image.
def build_entry(docker_image, dockerfile_path):
  parent = ''
  with open(dockerfile_path, "r") as dockerfile:
    for line in dockerfile:
      if ('FROM ' in line):
        #If the parent already has at least one value in it
        if parent != '':
          #if the parent already has more than one value, append with new line
          if parent[0] == '|':
            parent += "\n      " + line.split[1]
          #Else, shift to a multi-line format.
          else:
            parent = "|\n      " + parent + "\n      " + line.split[1]
        #Else, put in the parent with the format "ENTRY"
        else:
          parent = line.split()[1]
  new_image = {
    docker_image: {
      'parents': parent,
      'children': "none"
    }
  }
  f = open (RELATION_FILENAME)
  g = open ("temp.yaml", "w")
  data = yaml.safe_load(f)
  data['images'].update(new_image)
  yaml.safe_dump(data, g)

#Checks to see if there are any existing images with the name provided.  If there are, then it will verify the information.  If not, then it passes the information to build a new entry in the yaml file.
def check_image (docker_image, dockerfile_path):
  with open (RELATION_FILENAME) as f:
    data = yaml.safe_load(f)
    f.close()
    for image in data["images"]:
      if (image == docker_image):
        check_path(docker_image, dockerfile_path)
        break
      else:
        print ("New image detected, building parent-child tree.")
        build_entry(docker_image, dockerfile_path)

def main():
  if len (sys.argv) < 1:
    print ("Usage python3 scripts/relational.py <dockerfile_path>")
    sys.exit(1)
  else:
    dockerfile_path = os.path.abspath(sys.argv[1])
    docker_image = re.split('/',  dockerfile_path)[-3]
    image_stat = check_image(docker_image, dockerfile_path)

if __name__ == "__main__":
  main()
