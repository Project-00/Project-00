#import matplotlib
#matplotlib.use("agg")
#matplotlib.rcParams["font.sans-serif"]="Hiragino Kaku Gothic Pro, MigMix 1P"

import matplotlib.pyplot as plt

plt.plot([1,2,3,4,5],[1,2,3,4,5], "bx-", label="1dm")

plt.plot([1,2,3,4,5],[1,4,9,16,25], "ro--", label="2dm")
plt.xlabel("x")
plt.ylabel("y")
plt.title("matplotlib to sample")
plt.legend(loc="best")
plt.xlim(0,6)
plt.savefig("advanced_graph.png", dpi=300)
