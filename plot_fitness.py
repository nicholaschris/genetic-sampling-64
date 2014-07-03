import numpy as np
from matplotlib import pyplot as plt

dec = [50,100,500,1000]
ann = [1000,2000,5000,7000]
decf = [0.08,0.07,0.04,0.02]
annf = [0.03,0.02,0.02,0.02]

plt.plot(dec, decf, 'ko')
plt.ylim((0,0.1))
plt.xlim((25,1025))
plt.xlabel("Number of samples")
plt.ylabel("Mean of fitness of solutions")
#plt.axis('tight')
plt.savefig('decfitness.pdf')
plt.close('all')

plt.plot(ann, annf, 'ko')
plt.ylim((0,0.05))
plt.xlim((500,7500))
plt.xlabel("Number of samples")
plt.xlabel("Number of samples")
plt.ylabel("Mean of fitness of solutions")
#plt.axis('tight')
plt.savefig('annfitness.pdf')

plt.close('all')

