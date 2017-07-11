# CASA session
from asap import opacity
import numpy as np
import matplotlib.pyplot as plt
c=opacity.model(273.,62500.,0.3,3200.)
d=opacity.model(273.,62500.,0.9,3200.)
e=opacity.model(285.,72500.,0.9,2600.)
freq=np.linspace(1e9,400e9,1000)
opc=np.log10(100*np.array([c.get_opacities(i) for i in freq])*.01)
ope=np.log10(100*np.array([e.get_opacities(i) for i in freq])*0.01)
np.savetxt('e.txt',ope)
np.savetxt('c.txt',opc)
np.savetxt('freq.txt',freq)
opd=np.log10(100*np.array([d.get_opacities(i) for i in freq])*.01)
np.savetxt('d.txt',opd)