[Nuke]: https://www.foundry.com/products/nuke 'Nuke'


nuke_bake_metadata
==================


This package is designed to work within the software package [Nuke].
It allows the user to convert metadata values into usable keyframes inside the application.

Demo
----
Check out the [demo](https://vimeo.com/261734907) on vimeo


How it works
------------

The scripts is based in a user selection in the Nodegraph. The script will save all the metadata keys which are available at this very 
point inside script.


How to implement
----------------

For the regular Nuke user without a pipeline to follow, the implementation can be achieved by
modifying the `init.py` and `menu.py` in your `.nuke` folder. This is the most common approach to add tools
on a per user base.

**init.py**


```python
nuke.pluginAddPath('/path/to/package/on/your/system/nuke_bake_metadata')
```
These lines will add the package to your working environment


**menu.py**

```python
import Nuke
from nuke_bake_metadata import interface

menubar = nuke.menu('Nuke')
custom_menu = menubar.addMenu("your custom menu")
custom_menu.addCommand ("Bake Metadata", interface.start_from_nuke(), 'f1')

```
These will create a new menu labeled as *your custom menu* and add a menu entry labeled as
*Bake Metadata*. Optionally you have the ability to assign a shortcut/hotkey to a menu entry. In this case it's *F1*.
