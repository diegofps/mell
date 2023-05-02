
# Basic Folder Structure 📁

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

