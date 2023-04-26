#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    from . import consts
except ImportError:
    import consts

import importlib.util
import argparse
import shutil
import json
import glob
import time
import sys
import os
import re

LOG_LEVEL = 2

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

def run_new_root(args):

    info("Creating a new root structure at", args.new_root)

    if os.path.exists(args.new_root):
        error(f"Can't create a root structure, a folder with this name already exists: {args.new_root}")
        
    for foldernames in [("style", "asset"), ("style", "template"), ("style", "plugin"), ("style", "static"), ("style", "logic"), ("meta",), ("generate",)]:
        path = os.path.join(args.new_root, *foldernames)
        info(f"  {path}")
        os.makedirs(path)
    
    sys.exit(0)

def run_new_style(args):

    info("Creating a new style structure at", args.new_style)
    
    if os.path.exists(args.new_style):
        error(f"Can't create a style structure, a folder with this name already exists: {args.new_style}")
        
    for foldernames in ["asset", "template", "plugin", "static"]:
        path = os.path.join(args.new_style, foldernames)
        info(f"  {path}")
        os.makedirs(path)
    
    sys.exit(0)

def run_new_plugin(args):

    filepath = os.path.join(args.plugin, f"{args.new_plugin}.py")
    info("Creating a new plugin script")
    
    if os.path.exists(filepath):
        error("Can't create the plugin. A plugin with this name already exists at", filepath)
    
    info(f"  {filepath}")
    dirname = os.path.dirname(filepath)
    os.makedirs(dirname, exist_ok=True)

    with open(filepath, 'w') as fout:
        fout.write("def plugin(args, meta, inflator):\n    pass\n\n")
    
    sys.exit(0)

def run_new_logic(args):

    info("Creating a new logic script")
    
    timestamp = int(time.time())
    filepath = os.path.join(args.logic, f"{timestamp}.{args.new_logic}.py")

    if os.path.exists(filepath):
        error("Can't create the plugin. A plugin with this name already exists at", filepath)
    
    info(f"  {filepath}")
    dirname = os.path.dirname(filepath)
    os.makedirs(dirname, exist_ok=True)

    with open(filepath, 'w') as fout:
        fout.write("def logic(args, meta):\n    pass\n\n")
    
    sys.exit(0)

def parse_args():

    parser = argparse.ArgumentParser(
                        prog='mell',
                        description='Metaprogramming layer designed to generates anything from template files.',
                        epilog="Check the README.md to learn more tips on how to use this application: https://github.com/diegofps/mell/blob/main/README.md",
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('metadata',
                        type=str,
                        metavar='METADATA',
                        nargs='*',
                        help="name of file(s) located inside the meta folder. If multiple names are provided, separated by comma, a merge will be performed.")

    parser.add_argument('-v', '--verbose',
                        default=None,
                        dest='verbose',
                        help="allow debug log messages to be displayed",
                        action='store_true')

    parser.add_argument('-q', '--quiet',
                        default=None,
                        dest='quiet',
                        help="display only warning messages and above",
                        action='store_true')

    parser.add_argument('--set',
                        default=[],
                        nargs=2,
                        dest='set',
                        help="customize the value of individual properties in the metadata",
                        action='append')

    parser.add_argument('--do',
                        type=str,
                        metavar='NAME',
                        default=None,
                        choices=['nothing', 'clean', 'static', 'template', 'plugin'],
                        dest='do',
                        help="define one or more action to be executed [nothing, clean, static, template, plugin]",
                        action='append')

    parser.add_argument('--root',
                        type=str,
                        metavar='PATH',
                        default='.',
                        dest='root',
                        help="root folder that contains the folders style, meta, and generate [.]",
                        action='store')
    
    parser.add_argument('--style',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='style',
                        help="style folder that contains asset, template, plugin, and static [<root>/style]",
                        action='store')

    parser.add_argument('--template',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='template',
                        help="folder to read the template files [<style>/template]",
                        action='store')

    parser.add_argument('--static',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='static',
                        help="folder to read the static files [<style>/static]",
                        action='store')

    parser.add_argument('--plugin',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='plugin',
                        help="folder to read the plugins [<style>/plugin]",
                        action='store')

    parser.add_argument('--asset',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='asset',
                        help="folder holding the asset files [<style>/asset]",
                        action='store')

    parser.add_argument('--logic',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='logic',
                        help="folder holding the logic files [<style>/logic]",
                        action='store')

    parser.add_argument('--meta',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='meta',
                        help="folder to read the metadata files [<root>/meta]",
                        action='store')

    parser.add_argument('--generate',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest=None,
                        help="folder to generate the output files [<root>/generate]",
                        action='store')

    parser.add_argument('-M', '--show-metadata',
                        default=False,
                        dest='show_metadata',
                        help="display the metadata, after execution of the logic scripts",
                        action='store_true')

    parser.add_argument('-P', '--show-parameter',
                        default=False,
                        dest='show_parameters',
                        help="display all command line parameters and their values, received or not",
                        action='store_true')

    parser.add_argument('--new',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_root",
                        help="create a new root folder using the recommended structure",
                        action='store')
    
    parser.add_argument('--new-style',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_style",
                        help="create a new style folder using the recommended structure",
                        action='store')
    
    parser.add_argument('--new-plugin',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_plugin",
                        help="create a new plugin script using the name provided",
                        action='store')
    
    parser.add_argument('--new-logic',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_logic",
                        help="create a new logic script using the name provided",
                        action='store')
    
    parser.add_argument('--version',
                        action='version', 
                        version=f'{consts.name} {consts.version}')
    
    parser.add_argument('--block_start',
                        type=str,
                        metavar='STR',
                        default='|?',
                        dest='block_start',
                        help="string representing the start of a code block [|?]",
                        action='store')

    parser.add_argument('--block_end',
                        type=str,
                        metavar='STR',
                        default='?|',
                        dest='block_end',
                        help="string representing the start of a code block [?|]",
                        action='store')

    parser.add_argument('--variable_start',
                        type=str,
                        metavar='STR',
                        default='|=',
                        dest='variable_start',
                        help="string representing the start of a printable block [|=]",
                        action='store')

    parser.add_argument('--variable_end',
                        type=str,
                        metavar='STR',
                        default='=|',
                        dest='variable_end',
                        help="string representing the start of a printable block [=|]",
                        action='store')

    parser.add_argument('--comment_start',
                        type=str,
                        metavar='STR',
                        default='|#',
                        dest='comment_start',
                        help="string representing the start of a comment block [|#]",
                        action='store')

    parser.add_argument('--comment_end',
                        type=str,
                        metavar='STR',
                        default='#|',
                        dest='comment_end',
                        help="string representing the start of a comment block [#|]",
                        action='store')

    args = parser.parse_args()

    if args.root is None:
        args.root = '.'

    if args.generate is None:
        args.generate = os.path.join(args.root, 'generate')

    if args.meta is None:
        args.meta = os.path.join(args.root, 'meta')

    if args.style is None:
        args.style = os.path.join(args.root, 'style')

    if args.static is None:
        args.static = os.path.join(args.style, 'static')

    if args.template is None:
        args.template = os.path.join(args.style, 'template')

    if args.plugin is None:
        args.plugin = os.path.join(args.style, 'plugin')

    if args.asset is None:
        args.asset = os.path.join(args.style, 'asset')

    if args.logic is None:
        args.logic = os.path.join(args.style, 'logic')

    if args.do is None:
        args.do = ['clean', 'static', 'template', 'plugin']

    global LOG_LEVEL
    
    if args.quiet and args.verbose:
        error("You can't use quiet (-q) and verbose (-v) modes at the same time")

    elif args.quiet:
        LOG_LEVEL = 3

    elif args.verbose:
        LOG_LEVEL = 0

    if args.new_root:
        run_new_root(args)
    
    if args.new_style:
        run_new_style(args)

    if args.new_plugin:
        run_new_plugin(args)

    if args.new_logic:
        run_new_logic(args)

    if args.metadata is None:
        parser.print_help()
        sys.exit(0)
    
    return args


def load_metadata(args, meta_filenames):

    meta = {}

    if not meta_filenames:
        return meta

    for metadata_name in meta_filenames[0].split(','):
        if not metadata_name:
            continue

        filepath = os.path.join(args.meta, metadata_name) + ".json"
        
        with open(filepath, "r") as fin:
            meta_parent = json.loads(fin.read())
            
            if "__parent__" in meta_parent:
                meta_parent_2 = load_metadata(args, meta_parent["__parent__"])
                meta_parent = update_dict_recursively(meta_parent_2, meta_parent)
            
            meta = update_dict_recursively(meta, meta_parent)
    
    return meta

def update_dict_recursively(dst, src):

    if isinstance(dst, dict):
        for key, value in src.items():
            if key in dst:
                dst[key] = update_dict_recursively(dst[key], value)
            else:
                dst[key] = value

    elif isinstance(dst, list) and isinstance(src, list) and len(src) == len(dst):
        for i in range(len(dst)):
            src_item, dst_item = src[i], dst[i]
            dst[i] = update_dict_recursively(dst_item, src_item)

    else:
        dst = src
    
    return dst


class MetaIterator:

    def __init__(self, iterator, is_dict=False):
        self.iterator = iterator
        self.is_dict = is_dict
    
    def __next__(self):
        value = self.iterator.__next__()
        if self.is_dict:
            return value[0], Meta(value[1])
        else:
            return Meta(value)


class Meta:

    def __init__(self, value):

        self.__dict__['value'] = value
    
    def __iter__(self):

        v = self.value
        if v is None:
            raise IndexError("Trying to iterate over a metadata that does not exist.")
        if isinstance(v, dict):
            return MetaIterator(v.items().__iter__(), is_dict=True)
        else:
            return MetaIterator(v.__iter__())
    
    def __contains__(self, index):
        
        v = self.value
        if v is None:
            raise IndexError("Trying to check membership in a metadata that does not exist.")
        return index in v
    
    def __eq__(self, other):

        if isinstance(other, Meta):
            return self.value == other.value
        else:
            return self.value == other
    
    def __bool__(self):

        return True if self.value else False

    def __getattr__(self, index):

        v = self.value
        if v is None:
            return Meta(None)
        elif index in v:
            return Meta(v[index])
        else:
            return Meta(None)
    
    def __getitem__(self, index):
        
        v = self.value
        if v is None:
            return Meta(None)
        else:
            return Meta(v[index])
    
    def __setitem__(self, index, value):
        
        v = self.value
        if v is None:
            raise IndexError("Trying to set an attribute to a metadata that does not exist.")
        v[index] = value
    
    def __setattr__(self, index, value):
        
        v = self.value
        if v is None:
            raise IndexError("Trying to set an attribute to a metadata that does not exist.")
        v[index] = value
    
    def __len__(self):
        
        v = self.value
        if v is None:
            raise IndexError("Trying to get the length of a metadata that does not exist.")
        return len(v)

    def __repr__(self):
        
        v = self.value
        return repr(v)

    def __str__(self) -> str:

        v = self.value
        return str(v)


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
    
    def inflate(self, relpath, meta, to_file=None, from_asset=True):
        
        if from_asset:
            if self.asset_env is None:
                raise IOError("Missing asset folder")
            template = self.asset_env.get_template(relpath)
        
        else:
            if self.template_env is None:
                raise IOError("Missing template folder")
            template = self.template_env.get_template(relpath)
        
        text = template.render(args=self.args, meta=meta, inflater=self)

        if to_file is not None:

            filepath_out = os.path.join(self.args.generate, relpath)
            folderpath_out = os.path.dirname(filepath_out)
            
            os.makedirs(folderpath_out, exist_ok=True)
            
            with open(filepath_out, "w") as fout:
                fout.write(text)

        return text
        
def do_nothing(args, inflater, meta):
    pass

def do_clean(args, inflater, meta):

    info("Cleaning generate directory")

    if os.path.exists(args.generate):
        if os.path.isdir(args.generate):
            for filepath in glob.glob(os.path.join(args.generate, '*')):
                debug("  Removing:", filepath)
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
        else:
            os.remove(args.generate)
    
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

def do_template(args, inflater:Inflater, meta:Meta):

    info("Generating template based files")

    for filepath in glob.glob(os.path.join(args.template, "**"), recursive=True):
        if os.path.isfile(filepath):
            relpath = os.path.relpath(filepath, args.template)
            debug("  ", relpath)

            inflater.inflate(relpath, meta, to_file=relpath, from_asset=False)


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
            plugin.plugin(args, meta, inflater)

def get_logic_files(args):

    filepaths = []

    for filepath in glob.glob(os.path.join(args.logic, '**', '*.py'), recursive=True):
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            cells = filename.split('.', 1)
            if len(cells) == 2:
                try:
                    timestamp = int(cells[0])
                    filepaths.append((timestamp, filepath))
                except ValueError:
                    pass
    
    filepaths.sort()
    return filepaths

def do_logic_scripts(args, meta):
    
    info("Executing logic files")
    
    rootpath = os.path.dirname(args.logic)
    filepaths = get_logic_files(args)
    
    for _, filepath in filepaths:
        logic_name = os.path.relpath(filepath, rootpath).replace('\\', '.').replace('/', '.')
        debug("  ", filepath)
        
        plugin_spec = importlib.util.spec_from_file_location(logic_name, filepath)
        plugin = importlib.util.module_from_spec(plugin_spec)
        plugin_spec.loader.exec_module(plugin)
        plugin.logic(args, meta)

def do_set_values(args, meta):

    info("Applying set")
    
    r = re.compile('\[(\d+)\]')

    for address, value in args.set:
        property_names = address.split('.')
        property_names = [re.split(r, x) for x in property_names]
        property_names = [x if i % 2 == 0 else int(x) for y in property_names for i,x in enumerate(y) if x]

        current = meta.value

        try:
            for i, idx in enumerate(property_names[:-1]):
                if isinstance(idx, str):
                    if isinstance(current, dict):
                        if not idx in current:
                            next_idx = property_names[i+1]
                            current[idx] = [] if isinstance(next_idx, int) else {}
                    elif isinstance(current, list):
                        raise ValueError(f"expected an address, got the property name `.{idx}'")
                    else:
                        raise ValueError(f"expected nothing, got the property name `.{idx}'")
                else:
                    if isinstance(current, list):
                        if idx >= len(current):
                            next_idx = property_names[i+1]
                            if isinstance(next_idx, int):
                                current += [[] for _ in range(idx + 1 - len(current))]
                                current[idx] = []
                            else:
                                current += [{} for _ in range(idx + 1 - len(current))]
                                current[idx] = {}
                    elif isinstance(current, dict):
                        raise ValueError(f"expected a property name, got the address [{idx}]")
                    else:
                        raise ValueError(f"expected nothing, got the address [{idx}]")
                    
                current = current[idx]
            
            idx = property_names[-1]

            if isinstance(idx, str):
                if isinstance(current, dict):
                    current[idx] = value
                elif isinstance(current, list):
                    raise ValueError(f"expected an address, got the property name `.{idx}'")
                else:
                    raise ValueError(f"expected nothing, got the property name `.{idx}'")
            else:
                if isinstance(current, list):
                    if idx >= len(current):
                        current += [None for _ in range(idx + 1 - len(current))]
                    current[idx] = value
                elif isinstance(current, dict):
                    raise ValueError(f"expected a property name, got the address [{idx}]")
                else:
                    raise ValueError(f"expected nothing, got the address [{idx}]")
            
        except ValueError as e:
            msg = str(e)
            if msg:
                warn(f"Invalid property '{address}' - {msg}")
            else:
                warn(f"Invalid property '{address}'")
        except IndexError:
            warn(f"Invalid property '{address}', index {idx} is out of range")

def do_show_metadata(args, meta):

    if args.show_metadata:
        print("Metadata:")
        print(json.dumps(meta.value, indent=2))

def do_show_parameters(args):

    if args.show_parameters:
        print("Parameters:")
        print(json.dumps(args.__dict__, indent=2))

def do_action(name, args, inflater, meta):

    globals()['do_' + name](args, inflater, meta)

def do_load_meta(args):
    if os.path.exists(args.meta):
        return Meta(load_metadata(args, args.metadata))

    if args.metadata:
        error(f"Folder meta does not exist - {args.meta}")
    
    return Meta({})
    
def do_load_inflater(args):
    return Inflater(args)

def main(*params):
    
    args = parse_args()

    info("Loading the metadata")
    meta = do_load_meta(args)
    
    do_set_values(args, meta)
    do_logic_scripts(args, meta)

    do_show_metadata(args, meta)
    do_show_parameters(args)

    info("Loading the inflater")
    inflater = do_load_inflater(args)

    info("Executing actions")
    for name in args.do:
        do_action(name, args, inflater, meta)

    info("Bye!")


if __name__ == "__main__":
    main()

