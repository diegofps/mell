
from utils import MellHelper

import os

def create_project(name, meta_name):
    
    p = MellHelper('load_metadata')

    p.delete()

    p.exec(f'--new {p.root_path}')

    meta_data     = """{"user": {"name": "Diego Souza","age": 33, "backpack": ["book", "pen", "bottle", "phone", "camera"]}}"""
    meta_filepath = os.path.join(p.meta_path, meta_name + '.json')

    with open(meta_filepath, 'w') as fout:
        fout.write(meta_data)
    
    return p

def test_load_metadata():

    meta_name     = "data"

    p = create_project('load_metadata', meta_name)
    
    status, stdout, stderr = p.exec(f'--root {p.root_path} --show-metadata {meta_name}')

    expected_output = """Metadata:
{
  "user": {
    "name": "Diego Souza",
    "age": 33,
    "backpack": [
      "book",
      "pen",
      "bottle",
      "phone",
      "camera"
    ]
  }
}
"""

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output

def test_metadata_set():

    meta_name = 'data'

    p = create_project('metadata_set', meta_name)

    status, stdout, stderr = p.exec(f'--root {p.root_path} --set "extra" "more" --set user.age 18 --set "user.backpack[1]" "keys" --show-metadata {meta_name}')

    expected_output = """Metadata:
{
  "user": {
    "name": "Diego Souza",
    "age": "18",
    "backpack": [
      "book",
      "keys",
      "bottle",
      "phone",
      "camera"
    ]
  },
  "extra": "more"
}
"""

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output



