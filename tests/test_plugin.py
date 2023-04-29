from utils import MellHelper, unindent

def test_plugin():

    metaname = 'data'

    metadata = unindent(8, """
        {
            "projects":[
                {
                    "name": "Thoculi",
                    "cost_in_usd": "1000000.00",
                    "duration_in_months": 3
                },
                {
                    "name": "Catalina",
                    "cost_in_usd": "30000000.00",
                    "duration_in_months": 24
                },
                {
                    "name": "Gold",
                    "cost_in_usd": "2000000.00",
                    "duration_in_months": 2
                }
            ]
        }
        """)
    
    asset_template = unindent(8, """
        Project '|= meta.name =|' will last |= meta.duration_in_months =| month(s) and cost USD |= meta.cost_in_usd =|.
        """)
    
    plugin_program = unindent(8, """
        def plugin(args, meta, inflater):
            for i, project in enumerate(meta.projects):
                inflater.inflate('project.txt', project, to_file=f'project_{i}.txt')
        """)

    project_0 = unindent(8, """
        Project 'Thoculi' will last 3 month(s) and cost USD 1000000.00.""")

    project_1 = unindent(8, """
        Project 'Catalina' will last 24 month(s) and cost USD 30000000.00.""")

    project_2 = unindent(8, """
        Project 'Gold' will last 2 month(s) and cost USD 2000000.00.""")

    p = MellHelper("plugin")
    p.create_project()
    p.create_metadata(metaname, metadata)
    p.create_plugin('projects', plugin_program)
    p.create_asset('project.txt', asset_template)
    status, stdout, stderr = p.exec(f'--root {p.root_path} {metaname}')

    assert status == 0
    assert stderr == ''
    assert stdout == ''

    assert p.read_generated_file('project_0.txt') == project_0
    assert p.read_generated_file('project_1.txt') == project_1
    assert p.read_generated_file('project_2.txt') == project_2
