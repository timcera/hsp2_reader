.. image:: https://github.com/timcera/hsp2_reader/actions/workflows/pypi-package.yml/badge.svg
    :alt: Tests
    :target: https://github.com/timcera/hsp2_reader/actions/workflows/pypi-package.yml
    :height: 20

.. image:: https://img.shields.io/coveralls/github/timcera/hsp2_reader
    :alt: Test Coverage
    :target: https://coveralls.io/r/timcera/hsp2_reader?branch=master
    :height: 20

.. image:: https://img.shields.io/pypi/v/hsp2_reader.svg
    :alt: Latest release
    :target: https://pypi.python.org/pypi/hsp2_reader/
    :height: 20

.. image:: http://img.shields.io/pypi/l/hsp2_reader.svg
    :alt: BSD-3 clause license
    :target: https://pypi.python.org/pypi/hsp2_reader/
    :height: 20

.. image:: https://img.shields.io/pypi/pyversions/hsp2_reader
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/hsp2_reader/
    :height: 20

hsp2_reader - Quick Guide
=========================
The hsp2_reader is a pure Python module and command line script to read HSP2
time-series from HDF5 files.

Installation
------------
pip
~~~
.. code-block:: bash

    pip install hsp2_reader

conda
~~~~~
.. code-block:: bash

    conda install -c conda-forge hsp2_reader

Usage - Command Line
--------------------
Just run 'hsp2_reader --help' to get a list of subcommands::


    usage: hsp2_reader [-h]
                     {hsp2, about} ...

    positional arguments:
      {hsp2, about}

    hdf5
        Read HSP2 results from HDF5 file.
    about
        Display version number and system information.

    optional arguments:
      -h, --help            show this help message and exit

The output time-series data is printed to the screen and you can then redirect
to a file.

Usage - API
-----------
You can use all of the command line subcommands as functions.  The function
signature is identical to the command line subcommands.  The return is always
a PANDAS DataFrame.

Simply import hsp2_reader::

    from hsp2_reader import hsp2_reader

    # Then you could call the function
    ntsd = hsp2_reader.hdf5("file.h5", "yearly", [,,,"TAET"])
