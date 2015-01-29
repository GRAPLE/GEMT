import sys
sys.path.append('Graple')
from Graple import Graple

if __name__ == '__main__':
    """Creates the working folders use by the GRAPLE program"""
    sm = Graple()
    sm.CreateWorkingFolders()
