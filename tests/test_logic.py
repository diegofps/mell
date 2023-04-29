
from utils import MellHelper, unindent


def test_logic():

    expected_output = unindent(8, """
        Metadata:
        {
          "users": [
            {
              "name": "Diego",
              "email": "diego@company.com"
            },
            {
              "name": "Quelle",
              "email": "quelle@company.com"
            }
          ]
        }
        """)

    logic_name = 'add_email'
    logic_program = unindent(8, """
        def logic(args, meta):
            for user in meta.users:
                user.email = user.name.value.lower() + "@company.com"
        """)

    meta_name = 'users'
    meta_data = unindent(8, """
        {
          "users": [
            {
              "name":"Diego"
            },
            {
              "name":"Quelle"
            }
          ]
        }
        """)

    p = MellHelper('logic')
    p.create_project()
    p.create_metadata(meta_name, meta_data)
    p.create_logic(logic_name, logic_program)

    status, stdout, stderr = p.exec(f'--root {p.root_path} --show-metadata users')

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output
