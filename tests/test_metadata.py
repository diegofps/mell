
from utils import MellHelper, unindent

def test_load_metadata():

    expected_output = unindent(8, """
        Metadata:
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
        """)

    meta_name = "data"

    p = MellHelper('load_metadata')
    p.create_project()
    p.create_metadata(meta_name, '{"user": {"name": "Diego Souza","age": 33, "backpack": ["book", "pen", "bottle", "phone", "camera"]}}')
    
    status, stdout, stderr = p.exec(f'--root {p.root_path} --show-metadata {meta_name}')

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output

def test_metadata_set():

    expected_output = unindent(8, """
        Metadata:
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
        """)

    meta_name = 'data'

    p = MellHelper('metadata_set')
    p.create_project()
    p.create_metadata(meta_name, '{"user": {"name": "Diego Souza","age": 33, "backpack": ["book", "pen", "bottle", "phone", "camera"]}}')
    
    status, stdout, stderr = p.exec(f'--root {p.root_path} --set "extra" "more" --set user.age 18 --set "user.backpack[1]" "keys" --show-metadata {meta_name}')

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output

