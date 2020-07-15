import os
import sys
import subprocess
import yaml
import re

RELATION_FILENAME = "relations.yaml"

#Updates any existing entries
def update_table(mod_image, image_version, parent_images, child_images):
  new_image = {
    mod_image: {
      image_version: {
        'parents': parent_images,
        'children': child_images
      }
    }
  }
  print(new_image)
  NEWDATA['images'].update(new_image)

#Updates the child relationship for an existing entry to include the new entry
def update_ancestry(parent, image_version):
  parent_image = parent.split(':')[0]
  parent_version = parent.split(':')[1]
  new_child_image = DOCKER_IMAGE + ':' + image_version
  new_child = ''
  for image in ORIDATA["images"]:
    if (image == parent_image):
      new_child = ORIDATA["images"][parent_image][parent_version]['children']
      if (new_child == 'none'):
        new_child = [new_child_image]
      else:
        new_child += [new_child_image]
  update_table(parent_image, parent_version, ORIDATA["images"][parent_image][parent_version]['parents'], new_child)

#Update the parent information from the Dockerfile
def update_parent(dockerfile_path, image_version):
  parents = []
  with open(dockerfile_path, "r") as dockerfile:
    for line in dockerfile:
      if ('FROM ' in line):
        parents += [line.split()[1].split('/')[-1]]
  for parent in parents:
    update_ancestry(parent, image_version)
  return parent

#Reads the Dockerfile to find the parent image, if there is any, and puts that information into the yaml file.  It assumes no child images, since this is a new image.
def build_entry(dockerfile_path, image_version, child_images):
  parent = update_parent(dockerfile_path, image_version)
  update_table(DOCKER_IMAGE, image_version, parent, child_images)
  write_new_yaml(new_image)

#Overwrite the existing relations.yaml with the new information
def write_new_yaml(new_image):
  f = open (RELATION_FILENAME, "w")
  yaml.safe_dump(NEWDATA, f)
  f.close()
  #Checks to see if there are any existing images with the name provided.  If there are, then it will verify the information.  If not, then it passes the information to build a new entry in the yaml file.
def check_image (dockerfile_path, image_version):
  for image in ORIDATA['images']:
    if (image == DOCKER_IMAGE):
      check_path(dockerfile_path)
      break
    else:
      child_images = "none"
      print ("New image detected, building parent-child tree.")
      build_entry(dockerfile_path, image_version, child_images)

def main():
  global DOCKER_IMAGE
  global ORIDATA
  global NEWDATA 
  if len (sys.argv) < 1:
    print ("Usage python3 scripts/relational.py <dockerfile_path>")
    sys.exit(1)
  else:
    dockerfile_path = os.path.abspath(sys.argv[1])
    DOCKER_IMAGE = re.split('/',  dockerfile_path)[-3]
    image_version = re.split('/',  dockerfile_path)[-2]
    with open (RELATION_FILENAME) as f:
      ORIDATA = yaml.safe_load(f)
      NEWDATA = yaml.safe_load(f)
    f.close()
    image_stat = check_image(dockerfile_path, image_version)
    write_new_yaml()

if __name__ == "__main__":
  main()
