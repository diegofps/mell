
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

    logic_program = unindent(8, """
        def logic(args, meta):
            for user in meta.users:
                user.email = user.name.value.lower() + "@company.com"
        """)

    p = MellHelper('logic')
    p.create_project()
    p.create_metadata('users', '{"users": [{"name":"Diego"},{"name":"Quelle"}]}')
    p.create_logic('create_user', logic_program)
    
    status, stdout, stderr = p.exec(f'--root {p.root_path} --show-metadata users')

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output
