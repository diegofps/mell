#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader, select_autoescape

import importlib.util
import argparse
import shutil
import json
import glob
import sys
import os


LOG_LEVEL = 1

def debug(*args):
    if LOG_LEVEL <= 0:
        print("DEBUG:", *args)

def info(*args):
    if LOG_LEVEL <= 1:
        print("INFO:", *args)

def warn(*args):
    if LOG_LEVEL <= 2:
        print("WARN:", *args)

def error(*args):
    if LOG_LEVEL <= 3:
        print("ERROR:", *args)
    sys.exit(1)


def parse_args():

    epilogue = """
    Recommended folder structure:

        <root>:
        |- generate: folder that will hold the generated data, do not edit this folder.
        |
        |- meta:     folder holding json files, each with a variation of the metadata.
        |
        |- template: folder holding the template files that will be rendered with the 
        |            current metadata and saved to the generate folder, using the same path.
        |
        |- static:   folder holding the static files that will be copied as they are to the 
        |            generate folder, using the same path.
        |
        |- plugin:   folder holding scripts with a main function receiving the parameters 
        |            inflater and meta.Create scripts to generate multiple files from 
        |            templates in the asset folder.
        |
        |- asset:    folder holding template and other files that are not directly copied to 
                    generate. They may be used by plugins or other tools.


    basic example:

        # Content of ./template/main.py
        print(|= meta["message"] =|)

        # Content of ./meta/pt.json
        { "message": "Olá Mundo" }

        # Content of ./meta/en.json
        { "message": "Hello World" }

        # Execute it with the following command:
        mel pt

        # It will generate the following file in ./generate/main.py
        print("Olá Mundo")
                    
        # Execute it with the following command:
        mel en

        # It will generate the following file in ./generate/main.py
        print("Hello World")


    plugin example:

        # Content of ./asset/example.txt
        Key: |= meta["key"] =|
        Value: |= meta["value"]=|

        # Content of ./plugin/example_plugin.py
        def main(inflater, meta):
            for i, item in enumerate(meta["examples"]):
                inflater.inflateAsset("example.txt", item, to_file=f"examples/ex{i}.txt")

        # Content of ./meta/en.txt
        {
            "examples": [
                {
                    "key": "nome",
                    "value": "Diego"
                },
                {
                    "key": "idade",
                    "value": "33"
                },
                {
                    "key": "sexo",
                    "value": "Masculino"
                },
                {
                    "key": "estado civil",
                    "value": "Solteiro"
                }
            ]
        }

        # Run it with the following command:
        mel en

        # Four files will be generated in ./generate/examples. The first file is ex0.txt, 
        # with the following content:
        Key: nome
        Value: Diego
    """

    parser = argparse.ArgumentParser(
                        prog='mel',
                        description='Metaprogramming layer designed to generates anything from template files.',
                        epilog=epilogue,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('metadata',
                        type=str,
                        metavar='METADATA',
                        help="name of file(s) located inside the meta folder. If multiple are provided, separated by comma, a merge will be performed.")

    parser.add_argument('-t', '--template',
                        type=str,
                        default=None,
                        dest='template',
                        help="Folder to read the template files, the default value is <root>/template",
                        action='store')

    parser.add_argument('-s', '--static',
                        type=str,
                        default=None,
                        dest='static',
                        help="Folder to read the static files, the default value is <root>/static",
                        action='store')

    parser.add_argument('-m', '--meta',
                        type=str,
                        default=None,
                        dest='meta',
                        help="Folder to read the metadata files, the default value is <root>/meta",
                        action='store')

    parser.add_argument('-g', '--generate',
                        type=str,
                        default=None,
                        dest=None,
                        help="Folder to generate the code, the default value is <root>/generate",
                        action='store')

    parser.add_argument('-p', '--plugin',
                        type=str,
                        default=None,
                        dest='plugin',
                        help="Folder to read the plugins, the default value is <root>/plugin",
                        action='store')

    parser.add_argument('-a', '--asset',
                        type=str,
                        default=None,
                        dest='asset',
                        help="Folder holding the asset files, the default value is <root>/asset",
                        action='store')

    parser.add_argument('-r', '--root',
                        type=str,
                        default='.',
                        dest='root',
                        help="Root folder that contains all other folders, the default value is '.'",
                        action='store')

    parser.add_argument('-v', '--verbose',
                        default=None,
                        dest='verbose',
                        help="Allow debug log messages to be displayed",
                        action='store_true')

    parser.add_argument('-q', '--quiet',
                        default=None,
                        dest='quiet',
                        help="Display only warning messages and above",
                        action='store_true')

    parser.add_argument('--block_start',
                        type=str,
                        default='|?',
                        dest='block_start',
                        help="String representing the start of a code block, default is |?",
                        action='store')

    parser.add_argument('--block_end',
                        type=str,
                        default='?|',
                        dest='block_end',
                        help="String representing the start of a code block, default is ?|",
                        action='store')

    parser.add_argument('--variable_start',
                        type=str,
                        default='|=',
                        dest='variable_start',
                        help="String representing the start of a printable block, default is |=",
                        action='store')

    parser.add_argument('--variable_end',
                        type=str,
                        default='=|',
                        dest='variable_end',
                        help="String representing the start of a printable block, default is =|",
                        action='store')

    parser.add_argument('--comment_start',
                        type=str,
                        default='|#',
                        dest='comment_start',
                        help="String representing the start of a comment block, default is |#",
                        action='store')

    parser.add_argument('--comment_end',
                        type=str,
                        default='#|',
                        dest='comment_end',
                        help="String representing the start of a comment block, default is #|",
                        action='store')

    parser.add_argument('-d', '--do',
                        type=str,
                        default=None,
                        choices=['clean', 'static', 'template', 'plugin'],
                        dest='do',
                        help="Define one or more tasks to be executed. Will run all of them by default",
                        action='append')

    args = parser.parse_args()

    if args.root is None:
        args.root = '.'

    if args.generate is None:
        args.generate = os.path.join(args.root, 'generate')

    if args.meta is None:
        args.meta = os.path.join(args.root, 'meta')

    if args.static is None:
        args.static = os.path.join(args.root, 'static')

    if args.template is None:
        args.template = os.path.join(args.root, 'template')

    if args.plugin is None:
        args.plugin = os.path.join(args.root, 'plugin')

    if args.asset is None:
        args.asset = os.path.join(args.root, 'asset')

    if args.do is None:
        args.do = ['clean', 'static', 'template', 'plugin']

    global LOG_LEVEL
    
    if args.quiet and args.verbose:
        error("You can't use quiet (-q) and verbose (-v) modes at the same time")

    elif args.quiet:
        LOG_LEVEL = 2

    elif args.verbose:
        LOG_LEVEL = 0

    return args


class Meta:

    def __init__(self, args):
        
        if os.path.exists(args.meta):
            self.meta = self._load(args, args.metadata)

        else:
            warn(f"Folder meta does not exists - {args.meta}")
            self.meta = {}
        
    def _load(self, args, meta_filenames):

        meta = {}

        for filename in meta_filenames.split(','):
            filepath = os.path.join(args.meta, filename) + ".json"
            
            with open(filepath, "r") as fin:
                meta_parent = json.loads(fin.read())
                
                if "__parent__" in meta_parent:
                    meta_parent_2 = self._load(args, meta_parent["__parent__"])
                    meta_parent = self._update_dict_recursively(meta_parent_2, meta_parent)
                
                meta = self._update_dict_recursively(meta, meta_parent)
        
        return meta
    
    def _update_dict_recursively(self, dst, src):

        if isinstance(dst, dict):
            for key, value in src.items():
                if key in dst:
                    dst[key] = self._update_dict_recursively(dst[key], value)
                else:
                    dst[key] = value

        elif isinstance(dst, list) and isinstance(src, list) and len(src) == len(dst):
            for i in range(len(dst)):
                src_item, dst_item = src[i], dst[i]
                dst[i] = self._update_dict_recursively(dst_item, src_item)

        else:
            dst = src
        
        return dst

    def __contains__(self, index):

        try:
            current = self.meta

            for idx in index.split("."):
                if isinstance(current, list):
                    current = current[int(idx)]
                else:
                    current = current[idx]
            
            return True
            
        except KeyError:
            return False
    
    def __getitem__(self, index):

        try:
            current = self.meta

            for idx in index.split("."):
                if isinstance(current, list):
                    current = current[int(idx)]
                else:
                    current = current[idx]

            return current
            
        except KeyError:
            raise KeyError(index)
    
    def len(self, index):

        return len(self[index])

    def __repr__(self):
        return json.dumps(self.meta, indent=2)


class Inflater:

    def __init__(self, args):
        self.args = args
        self.template_env = self._create_env(args.template)
        self.asset_env = self._create_env(args.asset)
    
    def _create_env(self, folderpath):
        if not os.path.exists(folderpath):
            return None

        return Environment(
            block_start_string=self.args.block_start,
            block_end_string=self.args.block_end,
            
            variable_start_string=self.args.variable_start, 
            variable_end_string=self.args.variable_end,
            
            comment_start_string=self.args.comment_start,  
            comment_end_string=self.args.comment_end,

            loader=FileSystemLoader(folderpath),
            autoescape=select_autoescape(),
            trim_blocks=True, 
            lstrip_blocks=True
        )
    
    def inflateTemplate(self, relpath, meta, to_file=None):
        
        if self.template_env is None:
            raise IOError("Missing template folder")
        
        template = self.template_env.get_template(relpath)
        text = template.render(meta=meta, inflater=self)

        if to_file is not None:
            self._save_as_generated_file(text, to_file)
        
        return text
    
    def inflateAsset(self, relpath, meta, to_file=None):
        
        if self.asset_env is None:
            raise IOError("Missing asset folder")
        
        template = self.asset_env.get_template(relpath)
        text = template.render(meta=meta, inflater=self)

        if to_file is not None:
            self._save_as_generated_file(text, to_file)
        
        return text
    
    def _save_as_generated_file(self, text, relpath):

        filepath_out = os.path.join(self.args.generate, relpath)
        folderpath_out = os.path.dirname(filepath_out)
        
        os.makedirs(folderpath_out, exist_ok=True)
        
        with open(filepath_out, "w") as fout:
            fout.write(text)
        

def do_clean(args, inflater, meta):

    info("Cleaning generate directory")

    if os.path.exists(args.generate):
        if os.path.isdir(args.generate):
            shutil.rmtree(args.generate)
        else:
            os.remove(args.generate)
    
    os.makedirs(args.generate, exist_ok=True)

def do_static(args, inflater, meta):

    info("Copying static data")

    for filepath in glob.glob(os.path.join(args.static, '**'), recursive=True):
        if os.path.isfile(filepath):
            relpath = os.path.relpath(filepath, args.static)
            filepath_out = os.path.join(args.generate, relpath)
            debug(f"{filepath} -> {filepath_out}")

            folderpath_out = os.path.dirname(filepath_out)
            os.makedirs(folderpath_out, exist_ok=True)
            shutil.copy2(filepath, filepath_out)

def do_template(args, inflater, meta):

    info("Generating template based files")

    for filepath in glob.glob(os.path.join(args.template, "**"), recursive=True):
        if os.path.isfile(filepath):
            relpath = os.path.relpath(filepath, args.template)
            debug("  ", relpath)

            inflater.inflateTemplate(relpath, meta, to_file=relpath)


def do_plugin(args, inflater, meta):
    
    info("Executing plugin files")

    rootpath = os.path.dirname(args.plugin)

    for filepath in glob.glob(os.path.join(args.plugin, '**', '*.py'), recursive=True):
        if os.path.isfile(filepath):
            plugin_name = os.path.relpath(filepath, rootpath).replace('\\', '.').replace('/', '.')
            debug("  ", filepath)
            
            plugin_spec = importlib.util.spec_from_file_location(plugin_name, filepath)
            plugin = importlib.util.module_from_spec(plugin_spec)
            plugin_spec.loader.exec_module(plugin)
            plugin.main(inflater, meta)


def main(*params):
    
    args = parse_args()
    debug(json.dumps(args.__dict__, indent=2))


    info("Loading the metadata")
    meta = Meta(args)
    debug(meta)


    info("Loading the inflater")
    inflater = Inflater(args)


    info("Executing actions")
    for name in args.do:
        globals()['do_' + name](args, inflater, meta)


    info("Bye!")


if __name__ == "__main__":
    main()

