# Mell

Mell is a Metaprogramming Logic Layer designer to generate anything from template files.

# Why do I need this?

There are moments in life that you may find yourself needing to customize an entire project, not only an e-mail or a single webpage in a backend response. These are the moments that I use mell. So far, I have used its concept in the following situations:

* Generating VHDL code for a static neural network, variating a few parameters. Mell is much more flexible than the generic atributes present in the language.
* Generating database model classes. I defined the model classes and relations as metadata and asked mell to generate them for me in C#.
* Generating resumes to send to job applications. I use latex to generate my resume, instead of changing multiple configuration files in my latex project I change only a single metadata file, customizing the letter, company name, color, and so on. Mell generates a latex source which I compile to PDF.

Conceptually, you may use mell in two directions. A metadata being used with multiple styles, representing different projections of the same thing, or a single style being used by multiple metadata, creating different things with the same look. 

As an example, consider the situation that we have metadata describing a mobile app and our style can render an Android app. We could change the metadata and generate different Android apps, or we could change the style and render the same app on another platform, an Apple app perhaps.


# When should I not use this?

I don't recommend using this if you are not confortable programming in the language you are generating code to, as the template files may elevate your project complexity. This works better if are at a point where you feel like everything is just repeating with a few different parameters. These few parameters will become your metadata.

You may constantly find that mell may be replaced by reflection or similar concepts on your programming language of choice. This is true and the answer to which of them is better depends on your requirements. Mell may be more efficient as many logic rules are evaluated during rendering time, whereas reflection adds more complexity during the program execution. However, reflection is also simpler and more flexible during runtime.

# Concepts

To use this library you must understand a few concepts. These are:

* `metadata:` These is data describing what we want to generate. We use json format for it.
* `style:` This is the set of features that are necessary to transform the metadata into something. It is composed by templates, assets, static files, and plugins.
* `generated folder:` This is where the rendered files will be saved and you must never change these files. However, you may want to execute or compile them if you are generating a webserver or a latex template, for instance. 
* `template:` These are models with missing parts. Mell will fill these parts with metadata when it generates the files and copy them to the generated folder, keeping the original path structure.
* `static:` These are files that will not be modified. Mell will copy them directly to the generated folder, keeping the original path structure.
* `asset:` These are files used by your logic layer but that are not automatically used by mell.
* `plugin:` Scripts that will be executed by mell. These usually access the files in the asset folder.

# Folder structure

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

# How to install / uninstall it?

```
# To install
pip install mell

# To upgrade
pip install --upgrade mell

# To uninstall
pip uninstall mell
```

# Give me Examples!

## Using the template folder

This will demonstrate how to use mell in a simple use case, changing the language for a static interface. You may be thinking now, "what a naive example, most web frameworks have much more powerful internationalization tools and I would never use it for that". Indeed, me neither. I used this in my resumes in latex, though. By doing this I had a different metadata for each place I would apply, some in portuguese, some in english, some specific for each position. Another benefit is that I could update the resume by changing only a single file. I could generate old ones again, they had their own metadata, and so on.

Create a new mell project and enter it.

```shell
mell --new template_test
cd template_test
```

Create the file `<root>/template/main.py` with the following content.

```python
print(|= meta["message"] =|)
```

Create the file `<root>/meta/pt.json` with the following content.

```json
{ "message": "Olá Mundo" }
```

Create the file `./meta/en.json` with the following content.

```json
{ "message": "Hello World" }
```

Inside the `<root>` folder, execute the following command. The parameter pt is the name of the metadata file we want to use, that is, `<root>/meta/pt.json`.

```shell
mell pt
```

Mell will generate the following file in `./generate/main.py`.

```python
print("Olá Mundo")
```

Now, execute the following command:

```shell
mell en
```

This time, mell will generate the following file in `./generate/main.py`.

```shell
print("Hello World")
```

## Using the plugin folder

This example will use a metadata to generate a bunch of letters, each addressed to a different client. We will use a plugin because the number of clients is defined on a list inside the metadata. Therefore, we will use a single template file inside the asset folder and the plugin will generate multiple files in the output. A similar approach could be used to generate model classes for an ORM, for instance.

Create a new mell project and enter it.

```shell
mell --new plugin_test
cd plugin_test
```

Create a file in `plugin_test/style/asset/letter.txt` with the following content.

```
Dear |= meta["name"] =|,

As you have added the item |= meta["product"] =| on your wishlist, I am here to tell you that this item is now available with a discount of |= meta["discount"] =|. 

If this is still of your interest, you can check it [here](|= meta["product_url"] =|). If you want to see or manage your entire wishlist you may click [here](http://shopping.com/wishlist).

Best Regards,
Bot
```

Create a file in `plugin_test/style/plugin/example_plugin.py` with the following content.

```python
def main(inflater, meta):
    for i, item in enumerate(meta["clients"]):
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
```

# Source Code

The source code is available [here](https://github.com/diegofps/mell)

