
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

def file_count(folderpath):

    filepaths = glob.glob(os.path.join(folderpath, '*'))
    return len(filepaths)
