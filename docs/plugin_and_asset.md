
# Using the plugin and asset folders

This example will use a metadata to generate a bunch of letters, each addressed to a different client. We will use a plugin because the number of clients is defined on a list inside the metadata. Therefore, we will use a single template file inside the asset folder and the plugin will generate multiple files in the output. A similar approach could be used to generate model classes for an ORM, for instance.

## Create the project

Create a new mell project and enter it.

```shell
mell --new plugin_test
cd plugin_test
```

## Create the asset

Create a file in `<root>/style/asset/letter.txt` with the following content.

```
Dear |= meta.name =|,

Your wishlist item '|= meta.product =|' is now on sale with |= meta.discount =| off. 

If this is still of your interest, you can check it [here](|= meta.product_url =|). If you want to see or manage your wishlist items, [click here](http://shopping.com/wishlist).

Best Regards,
Bot
```

## Create the plugin

Create a file in `<root>/style/plugin/example_plugin.py` with the following content. 

```python
def plugin(args, meta, inflater):
    for i, item in enumerate(meta.clients):
        inflater.inflate("letter.txt", item, to_file=f"examples/letter_{i}.txt")
```

## Create the metadata

Create a file in `<root>/meta/data.json` with the following content.

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

## Execute the plugin

Now, inside the `<root>` folder, execute the following command:

```shell
mell data
```

Three files will be generated in `<root>/generate/examples`, `letter_0.txt` to `letter_2.txt`, containing the following contents.

```
Dear Diego,

As you have added the item Tablet on your wishlist, I am here to tell you that this item is now available with a discount of 50%. 

If this is still of your interest, you can check it [here](http://shopping.com/item/12345). If you want to see or manage your entire wishlist you may click [here](http://shopping.com/wishlist).

Best Regards,
Bot
```

```
Dear Pedro,

Your wishlist item 'Microscope' is now on sale with 10% off. 

If this is still of your interest, you can check it [here](http://shopping.com/item/54321). If you want to see or manage your wishlist items, [click here](http://shopping.com/wishlist).

Best Regards,
Bot
```

```
Dear Jéssica,

Your wishlist item 'Professional Easel' is now on sale with 10% off. 

If this is still of your interest, you can check it [here](http://shopping.com/item/21543). If you want to see or manage your wishlist items, [click here](http://shopping.com/wishlist).

Best Regards,
Bot
```

# Final considerations

Keep in mind that your output don't need to always come from template files in the asset folder. You could call an external program, write your with using open, ask a library to generate something else and save it there, etc.
