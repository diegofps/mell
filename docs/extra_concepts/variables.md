
# The variables args, meta, and inflater <font size="5">📈</font>

These are important variables available troughout mell. They help to interact with templates, metadata, and command arguments.

* `meta: ` an object of type Meta that encapsulates the metadata allowing easy navigation through its fields. Use `.` to access attributes and `[]` to access array elements. Navigation always returns an object with its same type, a Meta object. To access the object it references you must use the attribute `value`. You can also iterate over this object, if it references a json object the iteration will return a tuple of type `(str, Meta)`. If you iterate over an array it will always return a `Meta` object.
* `inflater: ` an object used to inflate templates in the asset folder. Use the method `inflate` to inflate a template. You may call this method from a template inside the template folder or from a template in the asset folder to render a partial template in the template being generated. You may also call it from a plugin script, in this case it makes sense to use the optional parameter `to_file`. This will save the rendered template to the corresponding file in the output folder.
* `args: ` an object holding all the program parameters. `Program parameters` are attributes that control the program executing, like the folders it reads and writes data to, and so on. You should never change any of these values during the program execution.
