import pkg_resources

import numpy as np
import json

all_country_flags = set()
for kind in ["circle", "noto_original", "1x1", "4x3"]:
        j = json.load(open(f"flags_{kind}.json", "r"))
        all_country_flags.update(j.keys())

for kind in ["circle", "noto_original", "1x1", "4x3"]:
        j = json.load(open(f"flags_{kind}.json", "r"))
        vv = all_country_flags.difference(j.keys())
        print(vv)

class Flags:
    def __init__(self, kind="noto"):
        self._arr = np.load(f"flags_{kind}.npz")
        self._j = json.load(open(f"flags_{kind}.json", "r"))

    def get_arr(self, country_code):
        d = {}
        for k in ["split_index", "facecolors", "vertices", "codes"]:
            d[k] = self._arr[f"{country_code}_{k}"]

        return d

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

fig, axs = plt.subplots(10, 10, num=1, clear=True)

flags = Flags("noto_waved")
# country_codes = sorted(flags._j.keys())[100:]
country_codes = sorted(all_country_flags)
for ax, country_code in zip(axs.flat, country_codes):
    ax.set_axis_off()

    if country_code not in flags._j:
        continue

    _, _, xmax, ymax = flags._j[country_code]["viewbox"]
    arr = flags.get_arr(country_code)
    split_index = arr["split_index"]

    vertices = np.split(arr["vertices"], split_index)
    codes = np.split(arr["codes"], split_index)
    path_prop_list = []
    for v, c, fc in zip(vertices, codes, arr["facecolors"]):
        p = Path(vertices=v, codes=c)
        prop = dict(facecolor=fc)
        path_prop_list.append((p, prop))

    for p, prop in path_prop_list:
        patch = PathPatch(p, ec="none", **prop)
        ax.add_patch(patch)

    ax.set_aspect(1)
    ax.set(xlim=(0, xmax), ylim=(0, ymax))
    # ax.set_axis_off()
