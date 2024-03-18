import matplotlib.pyplot as plt
from mpl_flags import Flags

flags = Flags("noto_original")

fig, axs = plt.subplots(1, 2)

ax0 = axs[0]
flags.show_flag(ax0, "KR")


ax1 = axs[1]
da = flags.get_drawing_area("KR", wmax=100)

from matplotlib.offsetbox import AnnotationBbox
ab = AnnotationBbox(da, (0.5, 0.5), frameon=True,
                    box_alignment=(0.5, 0.5))
ax1.add_artist(ab)

plt.show()
