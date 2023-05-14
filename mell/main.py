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
        
    for foldernames in [("style", "assets"), ("style", "templates"), ("style", "generators"), ("style", "statics"), ("style", "migrations"), ("meta",), ("output",)]:
        path = os.path.join(args.new_root, *foldernames)
        info(f"  {path}")
        os.makedirs(path)
    
    sys.exit(0)

def run_new_style(args):

    folderpath = os.path.join(args.root, args.new_style)

    info("Creating a new style structure at", folderpath)
    
    if os.path.exists(folderpath):
        error(f"Can't create a style structure, a folder with this name already exists: {folderpath}")
        
    for foldernames in ["assets", "templates", "generators", "statics", "migrations"]:
        path = os.path.join(folderpath, foldernames)
        info(f"  {path}")
        os.makedirs(path)
    
    sys.exit(0)

def run_new_generator(args):

    filepath = os.path.join(args.generators, f"{args.new_generator}.py")
    info("Creating a new generator script")
    
    if os.path.exists(filepath):
        error("Can't create the generator. A file with this name already exists at", filepath)
    
    info(f"  {filepath}")
    dirname = os.path.dirname(filepath)
    os.makedirs(dirname, exist_ok=True)

    with open(filepath, 'w') as fout:
        fout.write("def generate(args, meta, inflator):\n    pass\n\n")
    
    sys.exit(0)

def run_new_migration(args):

    info("Creating a new migration script")
    
    timestamp = int(time.time())
    filepath = os.path.join(args.migrations, f"{timestamp}.{args.new_migration}.py")

    if os.path.exists(filepath):
        error("Can't create migration. A file with this name already exists at", filepath)
    
    info(f"  {filepath}")
    dirname = os.path.dirname(filepath)
    os.makedirs(dirname, exist_ok=True)

    with open(filepath, 'w') as fout:
        fout.write("def migrate(args, meta):\n    pass\n\n")
    
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
                        nargs='*',
                        dest='set',
                        help="customize the value of individual properties in the metadata (before migrations)",
                        action='append')

    parser.add_argument('--do',
                        type=str,
                        metavar='NAME',
                        default=None,
                        choices=['nothing', 'statics', 'templates', 'generators'],
                        dest='do',
                        help="define one or more action to be executed [nothing, statics, templates, generators]",
                        action='append')

    parser.add_argument('--root',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='root',
                        help="root folder that contains the folders style, meta, and generate [.]",
                        action='store')
    
    parser.add_argument('--style',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='style',
                        help="style folder containing assets, templates, generators, migrations, and statics [<root>/style]",
                        action='store')

    parser.add_argument('--templates',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='templates',
                        help="folder to read the template files [<style>/template]",
                        action='store')

    parser.add_argument('--statics',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='statics',
                        help="folder to read the static files [<style>/static]",
                        action='store')

    parser.add_argument('--generators',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='generators',
                        help="folder to read the generators [<style>/generators]",
                        action='store')

    parser.add_argument('--assets',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='assets',
                        help="folder holding the asset files [<style>/assets]",
                        action='store')

    parser.add_argument('--migrations',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='migrations',
                        help="folder holding the migration files [<style>/migrations]",
                        action='store')

    parser.add_argument('--meta',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest='meta',
                        help="folder to read the metadata files [<root>/meta]",
                        action='store')

    parser.add_argument('--output',
                        type=str,
                        metavar='PATH',
                        default=None,
                        dest=None,
                        help="folder to generate the output files [<root>/output]",
                        action='store')

    parser.add_argument('-M', '--show-metadata',
                        default=False,
                        dest='show_metadata',
                        help="display the metadata, after executing the migration scripts",
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
    
    parser.add_argument('--new-generator',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_generator",
                        help="create a new generator script using the name provided",
                        action='store')
    
    parser.add_argument('--new-migration',
                        type=str,
                        metavar='NAME',
                        default=None,
                        dest="new_migration",
                        help="create a new migration script using the name provided",
                        action='store')
    
    parser.add_argument('--clean',
                        dest="clean",
                        help="clean the output folder before generating the files",
                        action='store_true')
    
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

    if args.output is None:
        args.output = os.path.join(args.root, 'output')

    if args.meta is None:
        args.meta = os.path.join(args.root, 'meta')

    if args.style is None:
        args.style = os.path.join(args.root, 'style')

    if args.statics is None:
        args.statics = os.path.join(args.style, 'statics')

    if args.templates is None:
        args.templates = os.path.join(args.style, 'templates')

    if args.generators is None:
        args.generators = os.path.join(args.style, 'generators')

    if args.assets is None:
        args.assets = os.path.join(args.style, 'assets')

    if args.migrations is None:
        args.migrations = os.path.join(args.style, 'migrations')

    if args.do is None:
        args.do = ['statics', 'templates', 'generators']

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

    if args.new_generator:
        run_new_generator(args)

    if args.new_migration:
        run_new_migration(args)

    if args.metadata is None:
        parser.print_help()
        sys.exit(0)
    
    return args


def load_metadata(args, meta_parameters):

    meta = {}

    for metadata_names in meta_parameters:
        for metadata_name in metadata_names.split(','):
            if not metadata_name:
                continue

            filepath = os.path.join(args.meta, metadata_name) + ".json"
            
            with open(filepath, "r") as fin:
                meta_parent = json.loads(fin.read())
                
                if "__parent__" in meta_parent:
                    meta_parent_2 = load_metadata(args, meta_parent["__parent__"].split())
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
            child_value = v[index]
            return Meta(child_value) if isinstance(child_value, (list, dict)) else child_value
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
        self.template_env = self._create_env(args.templates)
        self.asset_env = self._create_env(args.assets)
    
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

            filepath_out = os.path.join(self.args.output, to_file)
            folderpath_out = os.path.dirname(filepath_out)
            
            os.makedirs(folderpath_out, exist_ok=True)
            
            with open(filepath_out, "w") as fout:
                fout.write(text)

        return text
        
def do_action_nothing(args, inflater, meta):
    pass

def do_clean(args):

    if not args.clean:
        return

    info("Cleaning output directory")

    if os.path.exists(args.output):
        if os.path.isdir(args.output):
            for filepath in glob.glob(os.path.join(args.output, '*')):
                debug("  Removing:", filepath)
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
        else:
            os.remove(args.output)
    
def do_action_statics(args, inflater, meta):

    info("Copying static data")

    for filepath in glob.glob(os.path.join(args.statics, '**'), recursive=True):
        if os.path.isfile(filepath):
            relpath = os.path.relpath(filepath, args.statics)
            filepath_out = os.path.join(args.output, relpath)
            debug(f"{filepath} -> {filepath_out}")

            folderpath_out = os.path.dirname(filepath_out)
            os.makedirs(folderpath_out, exist_ok=True)
            shutil.copy2(filepath, filepath_out)

def do_action_templates(args, inflater:Inflater, meta:Meta):

    info("Generating template based files")

    for filepath in glob.glob(os.path.join(args.templates, "**"), recursive=True):
        if os.path.isfile(filepath):
            relpath = os.path.relpath(filepath, args.templates)
            debug("  ", relpath)

            inflater.inflate(relpath, meta, to_file=relpath, from_asset=False)


def do_action_generators(args, inflater, meta):
    
    info("Executing generator files")

    rootpath = os.path.dirname(args.generators)

    for filepath in glob.glob(os.path.join(args.generators, '*.py'), recursive=True):
        if os.path.isfile(filepath):
            generator_name = os.path.relpath(filepath, rootpath).replace('\\', '.').replace('/', '.')
            debug("  ", filepath)
            
            generator_spec = importlib.util.spec_from_file_location(generator_name, filepath)
            generator = importlib.util.module_from_spec(generator_spec)
            generator_spec.loader.exec_module(generator)
            generator.generate(args, meta, inflater)

def get_sorted_script_files(folderpath):

    filepaths = []

    for filepath in glob.glob(os.path.join(folderpath, '*.py'), recursive=True):
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

def do_migrations(args, meta):
    
    info("Executing migration files")
    
    rootpath = os.path.dirname(args.migrations)
    filepaths = get_sorted_script_files(args.migrations)
    
    for _, filepath in filepaths:
        migration_name = os.path.relpath(filepath, rootpath).replace('\\', '.').replace('/', '.')
        debug("  Applying migration ", filepath)
        
        migration_spec = importlib.util.spec_from_file_location(migration_name, filepath)
        migration = importlib.util.module_from_spec(migration_spec)
        migration_spec.loader.exec_module(migration)
        migration.migrate(args, meta)

def do_set_values(args, meta):

    info("Applying set")
    
    r = re.compile('\[(\d+)\]')

    value_types = {
        'str':str, 
        'int': int, 
        'float': float, 
        'bytes':bytes, 
        'bool':bool
    }

    for set in args.set:

        value_type = str if len(set) < 3 else value_types[set[2]]

        address = set[0]
        value = value_type(set[1])

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

    globals()['do_action_' + name](args, inflater, meta)

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
    do_migrations(args, meta)

    do_show_metadata(args, meta)
    do_show_parameters(args)

    info("Loading the inflater")
    inflater = do_load_inflater(args)

    info("Executing actions")
    do_clean(args)
    for name in args.do:
        do_action(name, args, inflater, meta)

    info("Bye!")


if __name__ == "__main__":
    main()

