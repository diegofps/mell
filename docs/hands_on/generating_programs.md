
# Generating Programs <font size="5"></font>

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

```
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
    │   ├── logic
    │   ├── plugin
    │   ├── static
    │   └── template
    │       └── main.cpp
    └── python
        ├── asset
        ├── logic
        ├── plugin
        ├── static
        └── template
            └── main.py
```
