import sys
sys.path.append('Graple')
from Graple import Graple

if __name__ == '__main__':
    """Invokes the results fixup phase of the GRAPLE program"""
    sm = Graple()
    sm.SimFixup()
