
import shutil
import glob
import os


class MellProject:

    def __init__(self, root_name):
        
        self.cmd = os.path.join('.', 'mell', 'main.py')
        self.root_path = os.path.join('tmp', root_name)

        self.set_style('style')
    
    def set_style(self, name):

        self.style_path = os.path.join(self.root_path, name)
        self.meta_path = os.path.join(self.root_path, 'meta')
        self.generate_path = os.path.join(self.root_path, 'generate')

        self.template_path = os.path.join(self.style_path, 'template')
        self.asset_path = os.path.join(self.style_path, 'asset')
        self.logic_path = os.path.join(self.style_path, 'logic')
        self.plugin_path = os.path.join(self.style_path, 'plugin')
        self.static_path = os.path.join(self.style_path, 'static')
    
    def delete(self):

        if os.path.exists(self.root_path) and os.path.isdir(self.root_path):
            shutil.rmtree(self.root_path)
        

def file_count(folderpath):

    filepaths = glob.glob(os.path.join(folderpath, '*'))
    return len(filepaths)

def test_new_root():

    p = MellProject('new_root')
    
    p.delete()
    
    os.system(f'{p.cmd} --new {p.root_path}')

    assert file_count(p.root_path) == 3

    assert file_count(p.style_path) == 5
    assert file_count(p.meta_path) == 0
    assert file_count(p.generate_path) == 0

    assert file_count(p.template_path) == 0
    assert file_count(p.asset_path) == 0
    assert file_count(p.logic_path) == 0
    assert file_count(p.plugin_path) == 0
    assert file_count(p.static_path) == 0

def test_new_plugin():

    p = MellProject("new_plugin")
    name = 'new_plugin'

    p.delete()
    
    os.system(f'{p.cmd} --new {p.root_path}')
    os.system(f'{p.cmd} --style {p.style_path} --new-plugin {name}')
    
    assert file_count(p.plugin_path) == 1

def test_new_logic():
    
    p = MellProject("new_logic")
    name = 'new_logic'

    p.delete()
    
    os.system(f'{p.cmd} --new {p.root_path}')
    os.system(f'{p.cmd} --style {p.style_path} --new-logic {name}')
    
    assert file_count(p.logic_path) == 1

def test_new_style():

    p = MellProject("new_style")
    name = 'new_style2'

    p.delete()
    
    os.system(f'{p.cmd} --new {p.root_path}')
    os.system(f'{p.cmd} --root {p.root_path} --new-style {name}')

    p.set_style(name)
    
    assert file_count(p.root_path) == 4

    assert file_count(p.style_path) == 5
    assert file_count(p.meta_path) == 0
    assert file_count(p.generate_path) == 0

    assert file_count(p.template_path) == 0
    assert file_count(p.asset_path) == 0
    assert file_count(p.logic_path) == 0
    assert file_count(p.plugin_path) == 0
    assert file_count(p.static_path) == 0

