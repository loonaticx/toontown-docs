import sys
import os
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../toontown/src"))

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../src/toontown'))
sys.path.insert(0, os.path.abspath('../../src/otp'))
sys.path.insert(0, os.path.abspath('../../src/panda3d'))

from pathlib import Path

sys.path.insert(0, str(Path('../../', 'src').resolve()))


# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src"))
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src/toontown"))
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src/toontown/uberdog"))
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src/otp"))
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src/panda3d"))
# sys.path.insert(0, os.path.join(os.getcwd(), f"../../src/panda3d/otp"))
# sys.path.insert(0, os.path.abspath('src/toontown'))
# sys.path.insert(0, os.path.abspath('src/otp'))
# sys.path.append("F:\\Work Folder\\Toontown\\dev\\9 Misc Projects\\toontown-docs\\src\\toontown")
# sys.path.append("F:\\Work Folder\\Toontown\\dev\\9 Misc Projects\\toontown-docs\\src\\otp")
# sys.path.append("F:\\Work Folder\\Toontown\\dev\\9 Misc Projects\\toontown-docs\\src\\panda3d")
for x in os.walk('../../src'):
  sys.path.insert(0, x[0])


# print(sys.path)
# exit

# os.chdir(os.path.join(os.getcwd(), f"../../toontown/src"))
# print(f'!!cwd = {os.getcwd()}')


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'toontown'
copyright = '2024, toontown'
author = 'toontown'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_mock_imports = ['uberdog', 'NametagGlobals', 'speedchat','tutorial', 'ChatBalloon']

# Built-in variables automatically resolved in references.
builtins_types = {
    'base': 'direct.showbase.ShowBase.ShowBase',
    'render': 'panda3d.core.NodePath',
    'render2d': 'panda3d.core.NodePath',
    'aspect2d': 'panda3d.core.NodePath',
    'pixel2d': 'panda3d.core.NodePath',
    'hidden': 'panda3d.core.NodePath',
    'loader': 'direct.showbase.Loader.Loader',
    'taskMgr': 'direct.task.Task.TaskManager',
    'jobMgr': 'direct.showbase.JobManager.JobManager',
    'eventMgr': 'direct.showbase.EventManager.EventManager',
    'messenger': 'direct.showbase.Messenger.Messenger',
    'bboard': 'direct.showbase.BulletinBoard.BulletinBoard',
    'ostream': 'panda3d.core.Ostream',
    'globalClock': 'panda3d.core.ClockObject',
    'vfs': 'panda3d.core.VirtualFileSystem',
    'cpMgr': 'panda3d.core.ConfigPageManager',
    'cvMgr': 'panda3d.core.ConfigVariableManager',
    'pandaSystem': 'panda3d.core.PandaSystem',
    '__dev__': 'bool',
    'NametagGlobals': 'otp.nametag.NametagGlobals'
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
