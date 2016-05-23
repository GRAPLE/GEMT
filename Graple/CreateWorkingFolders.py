import sys, os
from Graple import Graple

if __name__ == '__main__':
    """Creates the working folders use by the GRAPLE program"""
    sm = Graple(os.path.dirname(os.path.realpath(__file__)))
    sm.CreateWorkingFolders()
