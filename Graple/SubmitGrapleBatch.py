import sys
sys.path.append('Graple')
from Graple import Graple

if __name__ == '__main__':
    """Invokes the simulation preparation phase of the GRAPLE program"""
    sm = Graple()
    if len(sys.argv) > 1:
        sm.CONFIG['SimsPerJob'] = sys.argv[1]
    sm.CreateWorkingFolders()
    sm.SimPrep()
