Installation
============

`PyCellID <https://pypi.org/project/pycellid/>`_ can be installed
using pip from `PyPI <https://pypi.org/>`_.

.. code-block:: bash

    $ pip install pycellid

Development
-----------

We welcome all kinds of contributions. You can build the development environment
locally with the following commands:

.. code-block:: bash

    $ git clone git@github.com:pyCellID/pyCellID.git
    $ cd pyCellID
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -e .
    $ pip install -r requirements/dev.txt

Run the tests with pytest:

.. code-block:: bash

    $ pytest -v tests/

Or run the full checks with tox:

.. code-block:: bash

    $ tox -r


Initialization
--------------

.. code-block:: bash

    >>> import pycellid
    >>> pycellid.__version__
    '0.0.18'
    >>> # Build or load your data, inspect your images and make plots.
    >>> from pycellid.core import CellData, CellsPloter
    >>> import pycellid.io as ld  # Build or load data frame.
    >>> from pycellid import images  # Get a 2-D aray representing your images.
