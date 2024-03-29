import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from roy import setup
from roy import log 
from roy import read_config 
from roy import config 
from roy import diff 
from roy import clear_cache_volume
from roy import stage 
from roy import sync 
from roy import get_tail 

def test_setup():
    assert 2 == 2
