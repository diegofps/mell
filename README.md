# Mell

Mell is a Metaprogramming Logic Layer designed to generate anything from template files. 

# When should I use Mell? ⭐

Sometimes it is useful to render an entire project, not only an e-mail or a single webpage, like in a webserver response. This is when mell comes to help. So far, I have used it in the following situations:

* Generating VHDL code for a static neural network, variating a few parameters. Mell is much more flexible than the generic atributes available in the language.
* Generating model classes for an ORM. I defined the model classes and relations as metadata and asked mell to generate them for me in C#.
* Generating resumes to send to job applications. I use latex to generate my resume. Instead of changing multiple configuration files in my latex project I change only a single metadata file, customizing the letter, company name, color, and so on. Mell generates a latex source that I compile to PDF.

Conceptually, you may use mell in two directions. A metadata used with multiple styles, representing different projections of the same thing, or a single style used by multiple metadata, creating different things with the same look. 

As an example, consider the situation that we have metadata describing a mobile app and a style that can render an Android app. We could change the metadata and generate different Android apps, or we could change the style and render the same app on different platforms, like an IOS app.


# When should I not use Mell? 🚫

I don't recommend using this if you are not confortable programming in the stack you are generating code to, as the template files may elevate your project complexity. This works better if are at a point where you feel like everything is just the same with a few different parameters. These few parameters will likely become your metadata when you use mell.

You may constantly find that mell may be replaced by reflection or similar concepts on your programming language of choice. This is true and the answer to "which of them is better?" depends on your requirements. Mell may be more efficient as many logic rules are evaluated during rendering time, whereas reflection adds more complexity during the program execution. However, reflection is also simpler and more flexible during runtime. Mell is also more suitable to generate configuration files based on global parameters, like a kubernetes' configuration file or a django's settings.

# Concepts 📕

To use this library you must understand a few concepts. These are:

* `metadata:` The data describing what we want to generate. It is written using the json format.
* `style:` Set of scripts, templates, and assets that will transform the metadata into something else.
* `generated folder:` This is where the rendered files will be saved. You must never change these files as they will be overwritten the next time you execute mell. 

A style is composed of the following items:

* `template:` file snippets with a few missing parts. Mell will fill these parts with metadata when it generates the files and copy them to the generated folder, keeping the original path structure.
* `static:` files that will not be modified. Mell will copy them directly to the generated folder, keeping the original path structure.
* `asset:` files used by your style that are not automatically used by mell.
* `plugin:` Scripts that will be automatically executed by mell. These scripts will usually interact with the `inflater` variable to generate multiple output files. It may load template files from the asset folder.
* `logic:` Scripts that will be automatically executed, in order, by mell. These are used to validate and extend the metadata.

# Basic folder structure 📁

The following table describes the folders used by mell.

| Folder  | Description | 
|-------------|-------------|
| \<root\> | Base folder containing the folders meta, style, and the generated folder |
| \<root\>/style | The base folder for template, static, plugin, and asset |
| \<root\>/generate | this will hold the generated data, never edit this folder |
| \<root\>/meta | holds all metadata as json files |
| \<root\>/style/template | template files that will be automatically rendered and written to the generated folder |
| \<root\>/style/static | static files that will be copied as they are to the output folder |
| \<root\>/style/plugin | scripts that will be automatically executed by mell to render multiple output files |
| \<root\>/style/asset | extra files that are not automatically used by mell. They may be used inside plugin and logic scripts |
| \<root\>/style/logic | scripts automatically executed by mell to transform or extend the metadata |

To create a new project using the structure above, use the following command.

```shell
mell --new <name_of_root_folder>
```

# Context variables 📈

These are important variables available troughout mell. They help to interact with templates, metadata, and command arguments.

* `meta: ` an object of type Meta that encapsulates the metadata allowing easy navigation through its fields. Use `.` to access attributes and `[]` to access array elements. Navigation always returns an object with its same type, a Meta object. To access the object it references you must use the attribute `value`. You can also iterate over this object, if it references a json object the iteration will return a tuple of type `(str, Meta)`. If you iterate over an array it will always return a `Meta` object.
* `inflater: ` an object used to inflate templates in the asset folder. Use the method `inflate` to inflate a template. You may call this method from a template inside the template folder or from a template in the asset folder to render a partial template in the template being generated. You may also call it from a plugin script, in this case it makes sense to use the optional parameter `to_file`. This will save the rendered template to the corresponding file in the output folder.
* `args: ` an object holding all the program parameters. `Program parameters` are attributes that control the program executing, like the folders it reads and writes data to, and so on. You should never change any of these values during the program execution.

# How to install / uninstall it? 🚀

```shell
# To install
pip install mell

# To upgrade
pip install --upgrade mell

# To uninstall
pip uninstall mell
```

After installing the module you should be able to access the command `mell` via terminal. If it doesn't, you may try the following options: (1) check that your $PATH variable includes the local bin directory that pip uses; (2) install it in a virtual environment, like virtualenv; or (3) try to install it at the system level, running pip as root;

# Generating Programs 🏗️

This will demonstrate how to use mell to generate two programs, changing the language for a static interface. You may be thinking now, "what a naive example, most web frameworks have much more powerful internationalization tools and I would never use it for that". Indeed, me neither. I used this in my resumes in latex, though. By doing this I had a different metadata for each place I would apply, some in portuguese, some in english, some specific for each position. Another benefit is that I could update the resume by changing only a single file. I could generate old ones again, they had their own metadata, and so on.

## Step 1. Create a new mell project

Execute the following command to create the standard structure.

```shell
mell --new template_test
cd template_test
```

Now, we will create a second style, named `style2`. We will make `style` render a program that prints a message using python and `style2` will render a program that prints a message using cpp.

```shell
mell --new-style style2
```

## Step 2. Create the metadata files

This is the content for `<root>/meta/en.json`.

```json
{
    "message": "Hello World"
}
```

This is the content for `<root>/meta/pt.json`.

```json
{
    "message": "Olá Mundo" 
}
```

## Step 3. Create the contents for style and style2

This is the content for `<root>/style/template/main.py`:

```python
print("|= meta.message =|")
```

This is the content for `<root>/style2/template/main.cpp`.

```shell
#include <iostream>

int main()
{
    std::cout << "|= meta.message =|" << std::endl;
    return 0;
}
```

## Step 4. Generating the programs

If we only pass the metadata name to mell, it will use the default folders for style and generate folder. The following program will use the metadata file `<root>/meta/en.json`, the style folder `<root>/style`, and render everything to `<root>/generate`.

```shell
# This must be executed inside the <root> folder
mell en
```

The command above will generate the following content in `<root>/generate/main.py`

```shell
print("Hello World")
```

The following is the program generated if we execute `mell pt`.

```python
print("Olá Mundo")
```

To generate the cpp program we need to tell mell to use the style in style2. This can be done with the following command.

```shell
# This must be executed inside the <root> folder
mell --style style2 en
```

The command above will generate the following content in `<root>/generate/main.cpp`

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello World" << std::endl;
    return 0;
}
```

The following is the program generated if we execute `mell --style style2 pt`.

```cpp
#include <iostream>

int main()
{
    std::cout << "Olá Mundo" << std::endl;
    return 0;
}
```

## Step 5. Improving the structure

If you pretend to use just one style, the default folder name is fine, but for multiple style it is better to rename and put them into something more representative, like `styles/cpp` and `styles/python`. You may also want to save the output to different output folders. You can do this using the parameter `--generate`. The following is an example of all four combinations using the new style structure.

```shell
# Create new folders to keep our styles
mkdir styles

# Rename the style folders
mv style styles/python
mv style2 styles/cpp

# Generate the programs and save them in different folders
mell --style styles/cpp --generate generates/cpp/en en
mell --style styles/cpp --generate generates/cpp/pt pt
mell --style styles/python --generate generates/python/en en
mell --style styles/python --generate generates/python/pt pt
```

This is how the project looks like in the end.

```perl
.
├── generates
│   ├── cpp
│   │   ├── en
│   │   │   └── main.cpp
│   │   └── pt
│   │       └── main.cpp
│   └── python
│       ├── en
│       │   └── main.py
│       └── pt
│           └── main.py
├── meta
│   ├── en.json
│   └── pt.json
└── styles
    ├── cpp
    │   ├── asset
    │   ├── plugin
    │   ├── static
    │   └── template
    │       └── main.cpp
    └── python
        ├── asset
        ├── plugin
        ├── static
        └── template
            └── main.py
```

# Understanding the Pipeline 📑

It is important that you understand the order that operations are executed, as these may impact the availability of data throughout the execution. The list below shows the standard order.

1. Load metadata
1. Run logic scripts
1. Execute actions to generate the output:
>4. Clean output folder [clean]
>1. Copy static files [static]
>1. Render templates and copy them to output [template]
>1. Run plugin scripts [plugin]

Loading the metadata and running the logic scripts is always executed first. You can't modify this behaviour. The list of actions to generate the output, though, can be modified or supressed. To modify it we must use the command `--do <action_name>`. By default, mell will execute all of them but if we use the parameter `--do` it will execute only the tasks it received. A few examples are listed bellow.

```shell
# These two calls are the same
mell --do clean --do static --do template --do plugin data
mell data

# This will only generate output files based on the template folder
mell --do template data

# This will only clean the generated folder
mell --do clean

# The word 'nothing' is a special keyword. It will not do any action but will still load the metadata and execute logic scripts. This is useful when used with -v (verose mode) or --show-metadata (display the metadata after executing the logic scripts).
mell --do nothing data
mell --do nothing -v data
mell --do nothing --show-metadata data
```

# Tutorials 📚

* [Metadata](https://github.com/diegofps/mell/blob/main/docs/metadata.md) - Explains how the metadata work and how to inherit and extend from existing metadata;
* [Template](https://github.com/diegofps/mell/blob/main/docs/template.md) - Explains the template syntax and how to customize it;
* [Plugin and Asset](https://github.com/diegofps/mell/blob/main/docs/plugin_and_asset.md) - Shows how to use a plugin script to generate multiple output files from a single template;
* [Logic](https://github.com/diegofps/mell/blob/main/docs/logic.md) - Shows how to extend the input metadata, generating more metadata and preventing complex rules in template files.

# List of useful command options 💻

These are a few examples of common operations.

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

# Source Code 🎼

The source code is available in the project's [repository](https://github.com/diegofps/mell).

