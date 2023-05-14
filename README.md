# Mell

[![Tests](https://github.com/diegofps/mell/actions/workflows/python-app.yml/badge.svg)](https://github.com/diegofps/mell/actions/workflows/python-app.yml)

Mell is a tool designed to generate anything from template and metadata files. You can use it to generate a single file or an entire projects composed of thousands of files. It works like a preprocessor, generating code before the compilation-time. Its name is an acronym for MEtaprogramming Logic Layer, meaning its a logical layer infering pieces of code to be generated. You can install it with the following command.

```shell
pip install mell
```

# Basic Usage 🐣

Create a project to hold your generator.

```shell
mell --new test_project
cd test_project
```

Define the metadata file in `meta/data.json`

```json
{
    "phrase": "I am hungry!",
    "repeat": {
        "times": 33
    }
}
```

Define a template file in `style/template/example.txt`

```python
|? if meta.repeat.times < 5 ?|
    |? for x in range(meta.repeat.times) ?|
print("|= meta.phrase =|")
    |? endfor ?|
|? else ?|
for _ in range(|= meta.repeat.times =|):
    print("|= meta.phrase =|")
|? endif ?|
```

Execute mell from the project folder passing the name of the metadata.

```shell
mell data
```

The following is the content of `generate/example.txt`, created by mell using the metadata we specified and the style folder in this project.

```python
for _ in range(33):
    print("I am hungry!")
```

# Documentation 📚

## Glossary 📕

To use this library, you must understand at least the following concepts:

* `metadata:` The data describing what we want to generate. It is written using the json format.
* `style:` Set of scripts, templates, and assets that will transform the metadata into something else.
* `generated folder:` This is where the rendered files will be saved. You must never change these files as they will be overwritten the next time you execute mell. 

A style is composed of the following items:

* `templates:` file snippets with a few missing parts. Mell will fill these parts with metadata when it generates the files and copy them to the generated folder, keeping the original path structure.
* `statics:` files that will not be modified. Mell will copy them directly to the generated folder, keeping the original path structure.
* `assets:` files used by your style that are not automatically used by mell.
* `generators:` Scripts that will be automatically executed by mell. These scripts will usually interact with the `inflater` variable to generate multiple output files. It may load template files from the asset folder.
* `migrations:` Scripts that will be automatically executed, in order, by mell. These are used to validate and extend the metadata.

## Tutorials

* [Generating Programs](https://github.com/diegofps/mell/blob/main/docs/hands_on/metadata.md) - Example showing the concept and how to generate 4 programs using 2 styles and 2 metadata files;
* [Metadata](https://github.com/diegofps/mell/blob/main/docs/hands_on/metadata.md) - Explains how the metadata work and how to inherit and extend from existing metadata;
* [Template](https://github.com/diegofps/mell/blob/main/docs/hands_on/template.md) - Explains the template syntax and how to customize it;
* [Generators and Asset](https://github.com/diegofps/mell/blob/main/docs/hands_on/generators_and_assets.md) - Shows how to use a generator script to generate multiple output files from a single template;
* [migrations](https://github.com/diegofps/mell/blob/main/docs/hands_on/migrations.md) - Shows how to extend the input metadata, generating more metadata and avoiding complex rules in template files.

## Extra concepts

* [Basic Folder Structure](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/folder_structure.md) - describes the role of each folder;
* [The variables args, meta, and inflater](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/variables.md) - describes the role of the special variables;
* [Understanding the Pipeline](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/pipeline.md) - describes the order that mell processes everything;
* [When should I use mell?](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/when_to_use_it.md) - a few thoughts about using mell and developing code directly directly.

# TL;DR 💻

```shell
# This will create a folder named project_name with the recommended root folder structure
mell --new project_name

# This will create a folder named style2 with the recommended style folder structure (use it inside the root directory to keep things organized)
mell --new-style project_name

# Create a new generator file as <root>/style/generators/generator_name.py
mell --new-generator generator_name

# Create a new migration file as <root>/style/migrations/<timestamp>.migration_name.py
mell --new-migration migration_name

# Display the version number and exit
mell --version

# Use --set to customize the metadata from command line - useful when an external scripts needs to change something
mell --set message 'Hello World!' en
mell --set company.name 'Wespa' en
mell --set users[2].name 'Diego Souza' en

# Display more info during execution (verbose mode)
mell -v en

# Display less info during execution (quiet mode)
mell -q en

# Specify what we want to generate
mell --do statics --do templates --do generators en

# Only clean the output folder
mell --clean --do nothing

# Only generate files from templates
mell --do templates en

# Specify a different style folder. This will make mell use the folders templates, assets, generators, migrations, and statics that are inside this style.
mell --style style2 en

# Specify a different output folder. This is useful if you have multiple styles and want to generate different things on different folders.
mell --output output2 en

# An example with custom style names, distinct output folders and two metadata files. We are assuming the style folders are on local directory and named python and cpp.
mell --style styles/python --generate outputs/python/en en
mell --style styles/python --generate outputs/python/pt pt
mell --style styles/cpp --generate outputs/cpp/en en
mell --style styles/cpp --generate outputs/cpp/pt pt
```

# Source Code 🎼

The source code is available in the project's [repository](https://github.com/diegofps/mell).

