
from subprocess import Popen, PIPE

import shutil
import shlex
import glob
import os


class MellHelper:

    def __init__(self, root_name):

        self.cmd       = os.path.join('.'  , 'mell', 'main.py')
        self.root_path = os.path.join('tmp', root_name        )

        self.set_style('style')

    def set_style(self, name):

        self.style_path    = os.path.join(self.root_path, name      )
        self.meta_path     = os.path.join(self.root_path, 'meta'    )
        self.generate_path = os.path.join(self.root_path, 'generate')

        self.template_path = os.path.join(self.style_path, 'template')
        self.asset_path    = os.path.join(self.style_path, 'asset'   )
        self.logic_path    = os.path.join(self.style_path, 'logic'   )
        self.plugin_path   = os.path.join(self.style_path, 'plugin'  )
        self.static_path   = os.path.join(self.style_path, 'static'  )
    
    def delete(self):

        if os.path.exists(self.root_path) and os.path.isdir(self.root_path):
            shutil.rmtree(self.root_path)
    
    def exec(self, params):

        cmd = f'{self.cmd} {params}'
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        process.wait()

        returncode = process.returncode
        stdout     = process.stdout.read().decode('utf-8')
        stderr     = process.stderr.read().decode('utf-8')

        return returncode, stdout, stderr

    def create_project(self):

        self.delete()
        self.exec(f'--new {self.root_path}')

    def create_metadata(self, meta_name, meta_data):

        meta_filepath = os.path.join(self.meta_path, meta_name + '.json')
        with open(meta_filepath, 'w') as fout:
            fout.write(meta_data)
        
    def create_logic(self, name, data):

        files_before = file_count(self.logic_path)
        status, _, _ = self.exec(f'--style {self.style_path} --new-logic {name}')
        files_after = file_count(self.logic_path)

        assert status == 0
        assert files_before + 1 == files_after

        filepaths = list(glob.glob(os.path.join(self.logic_path, f'*.{name}.py')))

        assert len(filepaths) >= 1
        
        with open(filepaths[0], 'w') as fout:
            fout.write(data)

        return filepaths[0]

    def create_plugin(self, name, data):

        filepath = os.path.join(self.plugin_path, name + '.py')
        
        assert not os.path.exists(filepath)

        status, _, _ = self.exec(f'--style {self.style_path} --new-plugin {name}')

        assert status == 0
        assert os.path.exists(filepath)
        
        with open(filepath, 'w') as fout:
            fout.write(data)

        return filepath

    def create_asset(self, relpath, data):

        filepath = os.path.join(self.asset_path, relpath)
        
        with open(filepath, 'w') as fout:
            fout.write(data)

        return filepath

    def read_generated_file(self, relpath):
        filepath = os.path.join(self.generate_path, relpath)

        assert os.path.exists(filepath)

        with open(filepath, 'r') as fin:
            return fin.read()

def file_count(folderpath):

    filepaths = glob.glob(os.path.join(folderpath, '*'))
    return len(filepaths)

def unindent(n, data):

    prefix = ' ' * n
    lines = [x[n:] if x.startswith(prefix) else x for x in data.split('\n')]
    return '\n'.join(lines[1:] if lines[0] == '' else lines)

