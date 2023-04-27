from utils import MellHelper, file_count

def test_new_root():

    p = MellHelper('new_root')
    
    p.delete()

    returncode, _, _ = p.exec(f'--new {p.root_path}')
    
    assert returncode == 0

    assert file_count(p.root_path    ) == 3

    assert file_count(p.style_path   ) == 5
    assert file_count(p.meta_path    ) == 0
    assert file_count(p.generate_path) == 0

    assert file_count(p.template_path) == 0
    assert file_count(p.asset_path   ) == 0
    assert file_count(p.logic_path   ) == 0
    assert file_count(p.plugin_path  ) == 0
    assert file_count(p.static_path  ) == 0

def test_new_plugin():

    p = MellHelper("new_plugin")
    name = 'new_plugin'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--style {p.style_path} --new-plugin {name}')[0] == 0
    assert file_count(p.plugin_path) == 1

def test_new_logic():
    
    p = MellHelper("new_logic")
    name = 'new_logic'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--style {p.style_path} --new-logic {name}')[0] == 0
    assert file_count(p.logic_path) == 1

def test_new_style():

    p = MellHelper("new_style")
    name = 'new_style2'

    p.delete()
    
    assert p.exec(f'--new {p.root_path}')[0] == 0
    assert p.exec(f'--root {p.root_path} --new-style {name}')[0] == 0

    p.set_style(name)
    
    assert file_count(p.root_path    ) == 4

    assert file_count(p.style_path   ) == 5
    assert file_count(p.meta_path    ) == 0
    assert file_count(p.generate_path) == 0

    assert file_count(p.template_path) == 0
    assert file_count(p.asset_path   ) == 0
    assert file_count(p.logic_path   ) == 0
    assert file_count(p.plugin_path  ) == 0
    assert file_count(p.static_path  ) == 0

