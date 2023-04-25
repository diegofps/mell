
# Using logic scripts to extend the metadata

It is a good practice to keep your template files as simple as possible. This means that we must execute most of our business logic somewhere else. Plugins are not good for this because they execute out of order and they are intended to generate output files. The recommended way to make inferences, extend, or clean the metadata is through logic scripts. Additionally, the metadata should only be modified inside logic scripts.

These scripts carry a number with their name. The lower the number, the earlier they will execute. Its file format is `<number>.<script_name>.py` and they are stored in `<root>/style/logic`. If you want to generate the number automatically you can use the command `mell --new-logic script_name`.

This example will use logic scripts to generate models for a database. It is not supposed to be a complete example, but to demonstrate a few things we can do with it. 

## Create the Project

Let's start by creating a project called database.

```shell
mell --new database
cv database
```

## Create the metadata that we need to extend

Create a metadata with the following content in `<root>/meta/models.json`.

```json
{
    "models": {
        "User": {
            "table_name": "users",
            "columns": {
                "id": {"type": "primary_key"},
                "name": {"type": "string", "maxlength":"512"},
                "groups": {"type": "has_many", "other": "Group", "through": "owner", "column_id": "user_id"},
                "posts": {"type": "has_many", "other": "Post", "through": "owner"}
            }
        },
        "Group": {
            "columns": {
                "id": {"type": "primary key"},
                "name": {"type": "string", "maxlength": "512"},
                "posts": {"type": "has_many", "other": "Post", "through": "group"}
            }
        },
        "Post": {
            "columns": {
                "id": {"type": "primary key"},
                "text": {"type": "string", "maxlength": "512"},
				"group": {"type": "has_one", "other": "Group", "through": "posts"}
            }
        }
    }
}
```

We can ask mell to parse this metadata and show it to us with the following command. The parameter `--show-metadata` will make it print the metadata after it had applied every logic script available. The parameter `--do nothing` is a command to prevent it from generating output in the output folder, we just want to check the metadata now.

```shell
mell models --show-metadata --do nothing
```

This is the output that you should see.

```json
{
  "models": {
    "User": {
      "table_name": "users",
      "columns": {
        "id": {
          "type": "primary_key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "groups": {
          "type": "has_many",
          "other": "Group",
          "through": "owner",
          "column_id": "user_id"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "owner"
        }
      }
    },
    "Group": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "group"
        }
      }
    },
    "Post": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "text": {
          "type": "string",
          "maxlength": "512"
        },
        "group": {
          "type": "has_one",
          "other": "Group",
          "through": "posts"
        }
      }
    }
  }
}
```

These are a few issues in this metadata that we will try to fix using logic scripts. These are:

* `Fix 1:` We must guarantee that every model definition has table_name
* `Fix 2:` We must guarantee that column with types has_many and has_one will have the attribute column_id;
* `Fix 3:` We must guarantee that for every has_many, or has_one, declared, there must be an opposed attribute in the referenced class. For instance, the type User has many Posts, but the Post definition is not defining a has_one User. We would like to be sure it does.

## Fix 1. Add missing table_names

Let's execute the following command to create a logic script that will add the missing table_names.

```shell
mell --new-logic add_missing_table_names
```

The command above will generate a file named `<root>/style/logic/<timestamp>.add_missing_table_names.py`. The name `<timestamp>` will be replaced with a number containing the second since the Epoch that you executed this command. Add the following content to it.

```python
def logic(args, meta):
    for model_name, model_data in meta.models:
        if not "table_name" in model_data:
            model_data.table_name = model_name.lower() + 's'
```

The code above will iterate over the model names and, if the atribute `table_name` is not found, create it concatenating the name of the model and the character `s`. If we execute `mell models --show-metadata --do nothing` again, the output will be the following.

```json
{
  "models": {
    "User": {
      "table_name": "users",
      "columns": {
        "id": {
          "type": "primary_key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "groups": {
          "type": "has_many",
          "other": "Group",
          "through": "owner",
          "column_id": "user_id"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "owner"
        }
      }
    },
    "Group": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "group"
        }
      },
      "table_name": "groups"
    },
    "Post": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "text": {
          "type": "string",
          "maxlength": "512"
        },
        "group": {
          "type": "has_one",
          "other": "Group",
          "through": "posts"
        }
      },
      "table_name": "posts"
    }
  }
}
``` 

## Fix 2. Add missing columns_ids

We will now create a script to add the missing column_ids.

```shell
mell --new-logic add_missing_column_ids
```

And this will be its content.

```python
def logic(args, meta):
    for model_name, model in meta.models:
        for _, column in model.columns:
            type = column.type.value
            if type == "has_many":
                if not "column_id" in column:
                    column.column_id = model_name.lower() + "_id"
            elif type == "has_one":
                if not "column_id" in column:
                    column.column_id = column.other.value.lower() + "_id"
```

If we execute `mell models --show-metadata --do nothing` now, we will obtain the output shown below. Mell uses the timestamp in each script to determine that it must execute `add_missing_table_names` before `add_missing_column_ids`, as its timestamp is lower. This is important as later scripts can have some guarantees when their time to execute has arrived.

```json
  "models": {
    "User": {
      "table_name": "users",
      "columns": {
        "id": {
          "type": "primary_key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "groups": {
          "type": "has_many",
          "other": "Group",
          "through": "owner",
          "column_id": "user_id"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "owner",
          "column_id": "user_id"
        }
      }
    },
    "Group": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "group",
          "column_id": "group_id"
        }
      },
      "table_name": "groups"
    },
    "Post": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "text": {
          "type": "string",
          "maxlength": "512"
        },
        "group": {
          "type": "has_one",
          "other": "Group",
          "through": "posts",
          "column_id": "group_id"
        }
      },
      "table_name": "posts"
    }
  }
}
```

## Fix 3. Add opposing has_many and has_one

Let's create the last rule now, it will be called `add_opposing_has_many_and_has_one`.

```shell
--new-logic add_opposing_has_many_and_has_one
```

This is its content. 

```python
def logic(args, meta):
    for model_name, model in meta.models:
        for column_name, column in model.columns:
            type = column.type.value
            through = column.through.value
            other = column.other.value
            column_id = column.column_id.value

            # If we find a has_many, assure the corresponding model has a has_one
            if type == "has_many":
                for model_name2, model2 in meta.models:
                    if model_name2 == other:
                        for column_name2, column2 in model2.columns:
                            if column_name2 == through:
                                break
                        else:
                            # Column is missing, we need to add a has_one
                            model2.columns[through] = {
                                "type": "has_one", 
                                "other": model_name, 
                                "through": column_name,
                                "column_id": column_id
                            }

            # If we find a has_one, assure the corresponding model has a has_many
            elif type == "has_one":
                for model_name2, model2 in meta.models:
                    if model_name2 == other:
                        for column_name2, column2 in model2.columns:
                            if column_name2 == through:
                                break
                        else:
                            # Column is missing, we need to add a has_many
                            model2.columns[through] = {
                                "type": "has_many", 
                                "other": model_name, 
                                "through": column_name,
                                "column_id": column_id
                            }
```

This code is not complicate, but you don't need to get into the details of what it does and how it works. The important thing to take from it is that it is much better to perform these inferences here than inside the template files. If we execute `mell models --show-metadata --do nothing` this time we will get the following output.

```json
{
  "models": {
    "User": {
      "table_name": "users",
      "columns": {
        "id": {
          "type": "primary_key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "groups": {
          "type": "has_many",
          "other": "Group",
          "through": "owner",
          "column_id": "user_id"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "owner",
          "column_id": "user_id"
        }
      }
    },
    "Group": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "name": {
          "type": "string",
          "maxlength": "512"
        },
        "posts": {
          "type": "has_many",
          "other": "Post",
          "through": "group",
          "column_id": "group_id"
        },
        "owner": {
          "type": "has_one",
          "other": "User",
          "through": "groups",
          "column_id": "user_id"
        }
      },
      "table_name": "groups"
    },
    "Post": {
      "columns": {
        "id": {
          "type": "primary key"
        },
        "text": {
          "type": "string",
          "maxlength": "512"
        },
        "group": {
          "type": "has_one",
          "other": "Group",
          "through": "posts",
          "column_id": "group_id"
        },
        "owner": {
          "type": "has_one",
          "other": "User",
          "through": "posts",
          "column_id": "user_id"
        }
      },
      "table_name": "posts"
    }
  }
}
```

## Final considerations

As you can see, we have extended the original metadata with the missing information we wanted. However, there are many ways you can extend the metadata. These are a few ideas to keep your mind open:

* These are not any random information, but information that can be derived from the original metadata. Never forget that it is much more convenient to do it here than doing inferences inside the template files;
* Another use for logic scripts is to validate the metadata. We could check for inconsistencies, print warnings, errors, or abort the program in such cases;
* There is no limit to what you will run inside a logic script and how you will extend the metadata. For instance, you could use a Large Language Model to convert a metadata with use cases into a metadata with specific instructions to build a system. Or you could apply a genetic algorithm to optimize a hardware specification before saving its output;
* The specification doesn't always need to be inside the metadata. You could have a filepath in the metadata referencing a binary file that you read with a library and save something in the metadata. For instance.

