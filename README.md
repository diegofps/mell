# Mell

Mell is a Metaprogramming Logic Layer designed to generate anything from template files. 

# Why do I need this?

There are moments in life that you may find yourself needing to customize an entire project, not only an e-mail or a single webpage in a backend response. These are the moments that you may want to use mell. So far, I have used it in the following situations:

* Generating VHDL code for a static neural network, variating a few parameters. Mell is much more flexible than the generic atributes available in the language.
* Generating model classes for an ORM. I defined the model classes and relations as metadata and asked mell to generate them for me in C#.
* Generating resumes to send to job applications. I use latex to generate my resume. Instead of changing multiple configuration files in my latex project I change only a single metadata file, customizing the letter, company name, color, and so on. Mell generates a latex source that I compile to PDF.

Conceptually, you may use mell in two directions. A metadata used with multiple styles, representing different projections of the same thing, or a single style used by multiple metadata, creating different things with the same look. 

As an example, consider the situation that we have metadata describing a mobile app and a style that can render an Android app. We could change the metadata and generate different Android apps, or we could change the style and render the same app on different platforms, like an IOS app.


# When should I not use this?

I don't recommend using this if you are not confortable programming in the stack you are generating code to, as the template files may elevate your project complexity. This works better if are at a point where you feel like everything is just the same with a few different parameters. These few parameters will likely become your metadata when you use mell.

You may constantly find that mell may be replaced by reflection or similar concepts on your programming language of choice. This is true and the answer to "which of them is better?" depends on your requirements. Mell may be more efficient as many logic rules are evaluated during rendering time, whereas reflection adds more complexity during the program execution. However, reflection is also simpler and more flexible during runtime. Mell is also more suitable to generate configuration files based on global parameters, like a kubernetes' configuration file or a django's settings.

# Concepts

To use this library you must understand a few concepts. These are:

* `metadata:` These is data describing what we want to generate. We use json format for it.
* `style:` This is the set of features that are necessary to transform the metadata into something. It is composed by templates, assets, static files, and plugins.
* `generated folder:` This is where the rendered files will be saved and you must never change these files. However, you may want to execute or compile them if you are generating a webserver or a latex template, for instance. 

A style is composed of the following concepts:

* `template:` file snippets with a few missing parts. Mell will fill these parts with metadata when it generates the files and copy them to the generated folder, keeping the original path structure.
* `static:` files that will not be modified. Mell will copy them directly to the generated folder, keeping the original path structure.
* `asset:` files used by your style that are not automatically used by mell.
* `plugin:` Scripts that will be executed by mell. These usually access the files in the asset folder.

# Basic folder structure

The following table describes the folders used by mell.

| Folder  | Description | 
|-------------|-------------|
| \<root\> | The base folder that contains all folders described here |
| \<root\>/style | The base folder for template, static, plugin, and asset |
| \<root\>/generate | this will hold the generated data, never edit this folder |
| \<root\>/meta | holds all metadata as json files |
| \<root\>/style/template | holds the template files that will be automatically rendered and written to the generated folder |
| \<root\>/style/static | contains static files that will be copied as they are to the generate folder |
| \<root\>/style/plugin | contains scripts that will be executed by mell. Use these to render multiple files from templates in the asset folder |
| \<root\>/style/asset | contains template and other files that are not automatically used by mell. They may be used by plugins or other tools |

If you want to create a new project using this structure with the root folder named testing_mell, you can use the following command.

```shell
mell --new testing_mell
```

# How to install / uninstall it?

```shell
# To install
pip install mell

# To upgrade
pip install --upgrade mell

# To uninstall
pip uninstall mell
```

After installing the module you should be able to access the command `mell` via terminal. If it doesn't, you may try the following options: (1) check that your $PATH variable includes the local bin directory that pip uses; (2) install it in a virtual environment, like virtualenv; or (3) try to install it at the system level, running pip as root;

# Generating Hello Worlds

This will demonstrate how to use mell in a simple use case, changing the language for a static interface. You may be thinking now, "what a naive example, most web frameworks have much more powerful internationalization tools and I would never use it for that". Indeed, me neither. I used this in my resumes in latex, though. By doing this I had a different metadata for each place I would apply, some in portuguese, some in english, some specific for each position. Another benefit is that I could update the resume by changing only a single file. I could generate old ones again, they had their own metadata, and so on.

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

This is how the project looks in the end.

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
# The metadata syntax

Mell uses json to represent metadata. For instance, the following is a valid metadata file representing a letter. It may be located in `<root>/meta/letter_basic.json`.

```json
{
    "to": "Juliana",
    "address": "juliana@gmail.com",
    "subject": "Notification",
    "opening": "Dear Ju,",
    "first_paragraph": "I hope you are doing well :)",
    "paragraphs": ["This is a standard message just to remind you to drink water.", "Did you drink water today?"],
    "last_paragraph": "I am always here for you.",
    "ending": "Your friend,",
    "signature": "Bot"
}
```

Currently, the only one reserved word we use is `__parent__`. It allows us to generate a new metadata based on a previous one. It works similarly to inheritance in object oriented languages. The following example, located in `<root>/meta/letter_beach.json`, shows an extension to the previous metadata that customizes the attributes first_paragraph, paragraphs, and last_paragraph.

```json
{
    "__parent__": "letter_basic",
    "first_paragraph": "",
    "paragraphs": ["I checked the weather for this weekend and it will be great to go to the beach.", "Would you like me to invite a friend?"],
    "last_paragraph": ""
}
```

We will talk a little bit more about the template syntax in the next section, but given the following template file is saved in `<root>/style/template/letter.txt`.

```c
To: |= meta.to. =| <|= meta.address =|>
Subject: |= meta.subject. =|

|? if meta.opening. ?|
|= meta.opening. =|

|? endif ?|
|? if meta.first_paragraph. ?|
|= meta.first_paragraph. =|

|? endif ?|
|? for paragraph in meta.paragraphs. ?|
|= paragraph =|

|? endfor ?|
|? if meta.last_paragraph. ?|
|= meta.last_paragraph. =|

|? endif ?|
|= meta.ending. =|
|= meta.signature. =|

```

We may generate a letter with the first content, or the second content depending on the metadata we use. For instance, if we run `mell letter_basic` inside `<root>` we will generate the following content in the file `<root>/generate/letter.txt`:

```
To: Juliana <juliana@gmail.com>
Subject: Notification

Dear Ju,

I hope you are doing well :)

This is a standard message just to remind you to drink water.

Did you drink water today?

I am always here for you.

Your friend,
Bot
```

Whereas `mell letter_beach` would generate the following:

```
To: Juliana <juliana@gmail.com>
Subject: Notification

Dear Ju,

I checked the weather for this weekend and it will be great to go to the beach.

Would you like me to invite a friend?

Your friend,
Bot
```


# The template syntax

Mell currently uses [jinja2](https://jinja.palletsprojects.com) to parse the templates, but we don't use the standard tokens as we also want to generate templates from our templates, like those used by classic web servers. The standard tokens also cause problems with latex scripts. The following table summarizes the tokens we use and a short description of them.

| type | description | syntax |
| ---- | ----------- | ------ |
| block | tokens used to wrap pieces of code, like a for, endfor, if, else, endif, and so on. These will not produce any output in the rendered template. | \|? for x in items ?\| |
| variables | tokens used to wrap a piece of code that will produce a string that must be inserted in the rendered template | \|= for x in items =\| |
| comments | tokens used to wrap a comment. These will not be executed and will not generate output in the final render | \|# this is a comment #\| |

You may also customize the tokens to anything you want if you find that these tokens conflict with the source you are generating to. Customize them with the following commands.

```shell
# Customize the block tokens
mell --block_start '{B:' --block_end ':B}' metadata

# Customize the variable tokens
mell --variable_start '{V:' --variable_end ':V}' metadata

# Customize the comment tokens
mell --comment_start '{C:' --comment_end ':C}' metadata

# Customizing all of them
mell --block_start '{B:' --block_end ':B}' --variable_start '{V:' --variable_end ':V}' --comment_start '{C:' --comment_end ':C}' metadata
```

There are two special variables that we can use in the template syntax. These are:

* `meta:` to access the data in the metadata
* `inflater:` to inflate nested templates located in the asset

# Using the plugin and asset folders

This example will use a metadata to generate a bunch of letters, each addressed to a different client. We will use a plugin because the number of clients is defined on a list inside the metadata. Therefore, we will use a single template file inside the asset folder and the plugin will generate multiple files in the output. A similar approach could be used to generate model classes for an ORM, for instance.

Create a new mell project and enter it.

```shell
mell --new plugin_test
cd plugin_test
```

Create a file in `plugin_test/style/asset/letter.txt` with the following content.

```
Dear |= meta.name. =|,

Your wishlist item '|= meta.product. =|' is now on sale with |= meta.discount. =| off. 

If this is still of your interest, you can check it [here](|= meta.product_url. =|). If you want to see or manage your wishlist items, [click here](http://shopping.com/wishlist).

Best Regards,
Bot
```

Create a file in `plugin_test/style/plugin/example_plugin.py` with the following content.

```python
def main(inflater, meta):
    for i, item in enumerate(meta.clients.):
        inflater.inflateAsset("letter.txt", item, to_file=f"examples/letter_{i}.txt")
```

Create a file in `plugin_test/meta/data.json` with the following content.
```json
{
    "clients": [
        {
            "name": "Diego",
            "product": "Tablet",
            "discount": "50%",
            "product_url": "http://shopping.com/item/12345"
        },
        {
            "name": "Pedro",
            "product": "Microscope",
            "discount": "10%",
            "product_url": "http://shopping.com/item/54321"
        },
        {
            "name": "Jéssica",
            "product": "Professional Easel",
            "discount": "10%",
            "product_url": "http://shopping.com/item/21543"
        }
    ]
}
```

Now, inside the `<root>` folder, execute the following command:

```shell
mell data
```

Three files will be generated in `<root>/generate/examples`. The first file is `letter_0.txt`, containing the following content. The remaining files contain similar content, but with their remaining data:

```
Dear Diego,

As you have added the item Tablet on your wishlist, I am here to tell you that this item is now available with a discount of 50%. 

If this is still of your interest, you can check it [here](http://shopping.com/item/12345). If you want to see or manage your entire wishlist you may click [here](http://shopping.com/wishlist).

Best Regards,
Bot
```

# Using the logic folder to extend the metadata



## Special Command Options

These are a few examples of common operations.

```shell
# This will create a folder named project_name with the recommended root folder structure
mell --new project_name

# This will create a folder named style2 with the recommended style folder structure (use it inside the root directory to keep things organized)
mell --new-style project_name

# Display more info during execution (verbose mode)
mell -v en

# Display less info during execution (quiet mode)
mell -q en

# Specify what we want to generate
mell -d clean -d static -d template -d plugin en

# Only clean the output folder
mell -d clean en

# Only generate files from templates
mell -d template en

# Specify a different style folder. This will make mell use the folders template, asset, plugin, and static that inside it.
mell --style style2 en

# Specify a different generate folder. This is useful if you have multiple styles and want to generate different things on different folders.
mell --generate generate2 en

# An example with custom style names, distinct output folders and two metadata files. We are assuming the style folders are on local directory and named python and cpp.
mell --style python --generate genPythonEn en
mell --style python --generate genPythonPt pt
mell --style cpp --generate genCppEn en
mell --style cpp --generate genCppPt pt
```

# Source Code

The source code is available [here](https://github.com/diegofps/mell)

