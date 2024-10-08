# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys
import tomllib
from importlib.metadata import version

sys.path.insert(0, str(pathlib.Path().absolute().parent.parent))
import PvMail  # noqa

root_path = pathlib.Path(__file__).parent.parent.parent

with open(root_path / "pyproject.toml", "rb") as fp:
    toml = tomllib.load(fp)
metadata = toml["project"]

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

gh_org = "prjemian"
project = metadata["name"]
copyright = toml["tool"]["copyright"]["copyright"]
author = "Pete Jemian, Kurt Goetze"
description = metadata["description"]
rst_prolog = f".. |author| replace:: {author}"
github_url = f"https://github.com/{gh_org}/{project}"

# -- Special handling for version numbers ------------------------------------
# https://github.com/pypa/setuptools_scm#usage-from-sphinx

release = version(project)
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = """
    sphinx.ext.autodoc
    sphinx.ext.autosummary
    sphinx.ext.coverage
    sphinx.ext.githubpages
    sphinx.ext.inheritance_diagram
    sphinx.ext.mathjax
    sphinx.ext.todo
    sphinx.ext.viewcode
    sphinx_design
""".split()
extensions.append("sphinx_tabs.tabs")  # this must be last

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "_static/logo2.png"
html_static_path = ["_static"]
html_theme = "pydata_sphinx_theme"
html_title = f"{project} {version}"

html_context = {
    "github_user": "BCDA-APS",
    "github_repo": "pvMail",
    "github_version": "main",
    "doc_path": "docs",
}

html_theme_options = {
    "github_url": "https://github.com/BCDA-APS/pvMail",
    "logo": {
        "text": html_title,
        "image_dark": "_static/logo2.png",
    },
    "use_edit_page_button": True,
    "navbar_align": "content", 
}

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_mock_imports
autodoc_mock_imports = """
    pydm
    PyQt5
""".split()
