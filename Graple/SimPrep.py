import sys
sys.path.append('Graple')
from Graple import Graple

if __name__ == '__main__':
    """Invokes the simulation preparation phase of the GRAPLE program"""
    sm = Graple()
    sm.CreateWorkingFolders()
    sm.SimPrep()
