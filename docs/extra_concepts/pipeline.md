
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
