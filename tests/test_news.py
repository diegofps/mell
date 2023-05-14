from utils import MellHelper, file_count


def test_new_root():

    p = MellHelper('new_root')
    
    p.delete()

    returncode, _, _ = p.exec(f'--new {p.root_path}')
    
    assert returncode == 0

    assert file_count(p.root_path    ) == 3

    assert file_count(p.style_path   ) == 5
    assert file_count(p.meta_path    ) == 0
    assert file_count(p.output_path) == 0

    assert file_count(p.templates_path) == 0
    assert file_count(p.assets_path   ) == 0
    assert file_count(p.migrations_path   ) == 0
    assert file_count(p.generators_path  ) == 0
    assert file_count(p.statics_path  ) == 0

def test_new_generator():

    p = MellHelper("new_generator")
    name = 'new_generator'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--style {p.style_path} --new-generator {name}')[0] == 0
    assert file_count(p.generators_path) == 1

def test_new_migration():
    
    p = MellHelper("new_migration")
    name = 'new_migration'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--style {p.style_path} --new-migration {name}')[0] == 0
    assert file_count(p.migrations_path) == 1

def test_new_style():

    p = MellHelper("new_style")
    name = 'new_style2'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--root {p.root_path} --new-style {name}')[0] == 0

    p.set_style(name)
    
    assert file_count(p.root_path) == 4

    assert file_count(p.style_path ) == 5
    assert file_count(p.meta_path  ) == 0
    assert file_count(p.output_path) == 0

    assert file_count(p.templates_path ) == 0
    assert file_count(p.assets_path    ) == 0
    assert file_count(p.migrations_path) == 0
    assert file_count(p.generators_path) == 0
    assert file_count(p.statics_path   ) == 0

