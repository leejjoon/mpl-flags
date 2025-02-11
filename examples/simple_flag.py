import matplotlib.pyplot as plt
from mpl_flags import Flags

flags = Flags("circle")
cc = "BR"

fig, axs = plt.subplots(1, 2, num=1, clear=True)

boundary_prop=dict(ec="k")

ax0 = axs[0]
flags.show_flag(ax0, cc, boundary_prop=boundary_prop)


ax1 = axs[1]
da = flags.get_drawing_area(cc, wmax=100, boundary_prop=boundary_prop)

from matplotlib.offsetbox import AnnotationBbox
ab = AnnotationBbox(da, (0.5, 0.5), frameon=False, pad=0,
                    box_alignment=(0.5, 0.5))
ax1.add_artist(ab)

plt.show()
