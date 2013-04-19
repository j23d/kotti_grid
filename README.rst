==========
kotti_grid
==========

grid widget for Kotti.

`Find out more about Kotti`_

Setup
=====

To activate the ``kotti_grid`` add-on in your Kotti site, you need to
add an entry to the ``kotti.configurators`` setting in your Paste
Deploy config.  If you don't have a ``kotti.configurators`` option,
add one.  The line in your ``[app:main]`` (or ``[app:kotti]``, depending on how
you setup Fanstatic) section could then look like this::

    kotti.configurators =
        kotti_settings.kotti_configure
        kotti_grid.kotti_configure

Please note that ``kotti_grid`` depends on kotti_settings, so you have to
list it in your ``kotti.configurators`` too.

``kotti_grid`` extends your Kotti site with a widget where you have add a grid of
tiles that can be added, removed, reordered, coloured and filled with content. The
draggable tiles in ``kotti_grid`` are build with `gridster`_ and use the query
plugin `colorpicker`_, both are packed as fanstatic packages, here `js jquery_colorpicker`_
and `js gridster`_.

Do I have settings for it?
==========================

You have different settings to adjust ``kotti_grid`` to your needs.

.. image:: https://raw.github.com/j23d/kotti_grid/master/docs/images/settings.png

You can choose the slot and the context where the widget will be shown. Also you can
set the dimension of the tile and the margins between the tiles. The settings will
be used for new and existing tiles when you save the settings.

How to use it?
==============

Here you see the different options that are currently exist to change the tiles.

.. image:: https://raw.github.com/j23d/kotti_grid/master/docs/images/options.png

When you access the site with the edit permission the tiles are draggable. In every
tile you have four icons. With the first one you can rearrange the position of the tile.
The second opens a second window with a navigation browser where you can choose the
content for the tile, with the third one you can choose the background color of the
tile and with the forth one you can delete the tile. Be sure to click on "Save tiles",
otherwise the changes will not persist on a reload of the page.

With the plus sign on the right of the "Save tiles" button you create a new tile. Choose
the size of the new widget and click on the button "Add". To include your new tile in the
grid and to use the tile options you have to save the tiles.


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _gridster: http://pypi.python.org/pypi/Kotti
.. _js gridster: https://pypi.python.org/pypi/js.gridster
.. _colorpicker: http://pypi.python.org/pypi/Kotti
.. _js jquery_colorpicker: https://pypi.python.org/pypi/js.jquery_colorpicker
