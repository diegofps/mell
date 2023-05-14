
from utils import MellHelper, unindent


def test_migrations():

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

    migration_name = 'add_email'
    migration_script = unindent(8, """
        def migrate(args, meta):
            for user in meta.users:
                user.email = user.name.lower() + "@company.com"
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

    p = MellHelper('migrations')
    p.create_project()
    p.create_metadata(meta_name, meta_data)
    p.create_migration(migration_name, migration_script)

    status, stdout, stderr = p.exec(f'--root {p.root_path} --show-metadata users')

    assert status == 0
    assert stderr == ''
    assert stdout == expected_output
