# Mell

Mell is a tool designed to generate anything from template files and metadata files. You can use it to generate a single file or an entire projects composed of thousands of files. It works like a preprocessor, generating code before the compilation-time. Its name is an acronym for MEtaprogramming Logic Layer, meaning its a logical layer infering pieces of code to be generated.

[![Tests](https://github.com/diegofps/mell/actions/workflows/python-app.yml/badge.svg)](https://github.com/diegofps/mell/actions/workflows/python-app.yml)

# When should I use Mell? <font size="5">⭐</font>

Sometimes it is useful to render an entire project, not only an e-mail or a single webpage, like in a webserver response. This is when mell comes to help. So far, I have used it in the following situations:

* Generating VHDL code for a static neural network, variating a few parameters. Mell is much more flexible than the generic atributes available in the language.
* Generating model classes for an ORM. I defined the model classes and relations as metadata and asked mell to generate them for me in C#.
* Generating resumes to send to job applications. I use latex to generate my resume. Instead of changing multiple configuration files in my latex project I change only a single metadata file, customizing the letter, company name, color, and so on. Mell generates a latex source that I compile to PDF.

Conceptually, you may use mell in two directions. A metadata used with multiple styles, representing different projections of the same thing, or a single style used by multiple metadata, creating different things with the same look. 

As an example, consider the situation that we have metadata describing a mobile app and a style that can render an Android app. We could change the metadata and generate different Android apps, or we could change the style and render the same app on different platforms, like an IOS app.


# When should I not use Mell? <font size="5">🚫</font>

I don't recommend using this if you are not confortable programming in the stack you are generating code to, as the template files may elevate your project complexity. This works better if are at a point where you feel like everything is just the same with a few different parameters. These few parameters will likely become your metadata when you use mell.

You may constantly find that mell may be replaced by reflection or similar concepts on your programming language of choice. This is true and the answer to "which of them is better?" depends on your requirements. Mell may be more efficient as many logic rules are evaluated during rendering time, whereas reflection adds more complexity during the program execution. However, reflection is also simpler and more flexible during runtime. Mell is also more suitable to generate configuration files based on global parameters, like a kubernetes' configuration file or a django's settings.

# Concepts <font size="5">📕</font>

To use this library, you must understand at least the following concepts:

* `metadata:` The data describing what we want to generate. It is written using the json format.
* `style:` Set of scripts, templates, and assets that will transform the metadata into something else.
* `generated folder:` This is where the rendered files will be saved. You must never change these files as they will be overwritten the next time you execute mell. 

A style is composed of the following items:

* `template:` file snippets with a few missing parts. Mell will fill these parts with metadata when it generates the files and copy them to the generated folder, keeping the original path structure.
* `static:` files that will not be modified. Mell will copy them directly to the generated folder, keeping the original path structure.
* `asset:` files used by your style that are not automatically used by mell.
* `plugin:` Scripts that will be automatically executed by mell. These scripts will usually interact with the `inflater` variable to generate multiple output files. It may load template files from the asset folder.
* `logic:` Scripts that will be automatically executed, in order, by mell. These are used to validate and extend the metadata.

# How to install / uninstall it? <font size="5">🚀</font>

```shell
# To install
pip install mell

# To upgrade
pip install --upgrade mell

# To uninstall
pip uninstall mell
```

After installing the module you should be able to access the command `mell` via terminal. If it doesn't, you may try the following options: (1) check that your `$PATH` variable includes the local bin folder, tipicaly `~/.local/bin`; (2) install it in a virtual environment, like `virtualenv`; or (3) try to install it at the system level, running pip as root (should not be necessary);

# Basic Usage <font size="5">🐣</font>

Create a project to hold your generator.

```shell
mell --new test_project
cd test_project
```

Define the metadata file in `meta/data.json`

```json
{
    "phrase": "I am hungry!",
    "times": 33
}
```

Define a template file in `style/template/example.txt`

```python
for _ in range(|= meta.times =|):
    print("|= meta.phrase =|")
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

# Documentation <font size="5">📚</font>

## Hands on

* [Generating Programs](https://github.com/diegofps/mell/blob/main/docs/hands_on/metadata.md) - Example showing the concept and how to generate 4 programs using 2 styles and 2 metadata files.
* [Metadata](https://github.com/diegofps/mell/blob/main/docs/hands_on/metadata.md) - Explains how the metadata work and how to inherit and extend from existing metadata;
* [Template](https://github.com/diegofps/mell/blob/main/docs/hands_on/template.md) - Explains the template syntax and how to customize it;
* [Plugin and Asset](https://github.com/diegofps/mell/blob/main/docs/hands_on/plugin_and_asset.md) - Shows how to use a plugin script to generate multiple output files from a single template;
* [Logic](https://github.com/diegofps/mell/blob/main/docs/hands_on/logic.md) - Shows how to extend the input metadata, generating more metadata and preventing complex rules in template files.

## Extra concepts

* [Basic Folder Structure](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/folder_structure.md) - describes the role of each folder.
* [The variables args, meta, and inflater](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/variables.md) - describes the role of the special variables.
* [Understanding the Pipeline](https://github.com/diegofps/mell/blob/main/docs/extra_concepts/pipeline.md) - describes the order that mell processes everything.

# TL;DR <font size="5">💻</font>

```shell
# This will create a folder named project_name with the recommended root folder structure
mell --new project_name

# This will create a folder named style2 with the recommended style folder structure (use it inside the root directory to keep things organized)
mell --new-style project_name

# Create a new plugin file as <root>/style/plugin/plugin_name.py
mell --new-plugin plugin_name

# Create a new logic file as <root>/style/logic/<timestamp>.logic_name.py
mell --new-logic logic_name

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
mell --do clean --do static --do template --do plugin en

# Only clean the output folder
mell --do clean en

# Only generate files from templates
mell --do template en

# Specify a different style folder. This will make mell use the folders template, asset, plugin, and static that inside it.
mell --style style2 en

# Specify a different generate folder. This is useful if you have multiple styles and want to generate different things on different folders.
mell --generate generate2 en

# An example with custom style names, distinct output folders and two metadata files. We are assuming the style folders are on local directory and named python and cpp.
mell --style styles/python --generate generates/python/en en
mell --style styles/python --generate generates/python/pt pt
mell --style styles/cpp --generate generates/cpp/en en
mell --style styles/cpp --generate generates/cpp/pt pt
```

# Source Code <font size="5">🎼</font>

The source code is available in the project's [repository](https://github.com/diegofps/mell).

