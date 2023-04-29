
# The template syntax <font size="5">📰</font>

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

There are three special variables that we can use in the template syntax. These are:

* `meta:` to access the data in the metadata. Use `'.'` to access metadata attributes and `'[]'` to access array elements;
* `inflater:` to inflate nested templates located in the asset. Use `inflater.inflate("path_to_asset_file", meta)` to inflate an asset into this position;
* `args:` to access the program parameters and program parameters.
