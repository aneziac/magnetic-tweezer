from pycromanager import start_headless
from magnetic_tweezer import micro_manager as micro_manager
import os
import pytest


path = os.path.join('/', 'Program Files', 'Micro-Manager-2.0')
try:
    start_headless(path)
except FileNotFoundError:
    pytest.fail('Install MicroManager or fix the path')

micro_manager.MicroManagerInterface()
# TODO: FakeCamera setup
