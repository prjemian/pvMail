.. index:: installation

.. _install:

====================================
Installation Guide
====================================

``PvMail`` is available for installation by ``conda``, ``pip``, or from source.
Please `report <https://github.com/BCDA-APS/pvmail/issues/new>`_ any issues you
encounter or feature requests, too.

.. tab-set::

    .. tab-item:: conda

        .. _install.conda:

        conda
        -----

        Released versions of ``PvMail`` are available on `conda-forge
        <https://anaconda.org/conda-forge/pvmail>`_.

        If you have ``conda`` installed, then you can install::

            $ conda install conda-forge::pvmail

    .. tab-item:: pip

        .. _install.pip:

        pip
        ---

        Released versions of ``PvMail`` are available on `PyPI
        <https://pypi.org/project/PvMail/>`_.

        If you have ``pip`` installed, then you can install::

            $ pip install PvMail

    .. tab-item:: source

        .. index:: source code

        .. _install.source:

        source code
        -----------

        The latest development version of ``PvMail`` can be downloaded from the
        GitHub repository::

        $ git clone https://github.com/BCDA-APS/pvmail

        Install from the source directory using ``pip`` in editable mode::

            $ cd pvmail
            $ python -m pip install -e .

.. _install.dependencies:

Dependencies
------------

This software was built with packages from the Python standard library and these
additional packages:

- `PyQt5 <https://pypi.org/project/PyQt5/>`_ package to manage the GUI
- `PyEpics <https://pypi.org/project/pyepics/>`_ for EPICS CA connections
- `PyDM <https://pypi.org/project/PyDM/>`_ for EPICS-aware Qt widgets

