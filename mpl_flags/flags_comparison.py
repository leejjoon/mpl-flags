import numpy as np
import json
from matplotlib.path import Path
from matplotlib.patches import PathPatch


def get_all_country_codes():
    all_country_codes = set()
    for kind in ["circle", "noto_original", "1x1", "4x3"]:
            j = json.load(open(f"data/flags_{kind}.json", "r"))
            all_country_codes.update(j.keys())

    if False:
        for kind in ["circle", "noto_original", "1x1", "4x3"]:
            j = json.load(open(f"data/flags_{kind}.json", "r"))
            vv = all_country_flags.difference(j.keys())
            print(vv)

    return all_country_codes

class Flags:
    def __init__(self, kind="noto"):
        self._arr = np.load(f"data/flags_{kind}.npz")
        self._j = json.load(open(f"data/flags_{kind}.json", "r"))

    def get_arr(self, country_code):
        d = {}
        for k in ["split_index", "facecolors", "vertices", "codes"]:
            d[k] = self._arr[f"{country_code}_{k}"]

        return d

    def show_flag(self, ax, country_code):

        if country_code not in self._j:
            return

        _, _, xmax, ymax = self._j[country_code]["viewbox"]
        arr = self.get_arr(country_code)
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


def prepare_axes(fig, ncol, nrow, nkind, nax=None):
    fig.clf()

    if nax is None:
        nax = ncol * nrow

    gs_root = fig.add_gridspec(1, ncol)

    axs = []
    for gs in gs_root:
        gss =  gs.subgridspec(nrow, nkind)
        for irow in range(nrow):
            ax3 = [fig.add_subplot(gss[irow, icol]) for icol in range(nkind)]
            axs.append(ax3)
            if len(axs) >= nax:
                return axs

    return axs


def show_flags(country_codes, kinds, ncol, nrow):
    import matplotlib.pyplot as plt

    flagss = [Flags(k) for k in kinds]

    ncol = 3
    nrow = 12
    nkind = len(flagss)

    while country_codes:

        fig = plt.figure(figsize=(8, 10))
        axs = prepare_axes(fig, ncol, nrow, nkind, nax=len(country_codes))

        for ax3, country_code in zip(axs, country_codes):
            for ax, flags in zip(ax3, flagss):
                flags.show_flag(ax, country_code)
                ax.set_axis_off()

            ax3[0].annotate(country_code, (-0.1, 0.5), xycoords="axes fraction",
                            annotation_clip=False,
                            rotation=90, rotation_mode="anchor", va="baseline", ha="center")

        country_codes = country_codes[ncol*nrow:]


def show_all():
    import matplotlib.pyplot as plt

    country_codes = sorted(get_all_country_codes())[:44]
    kinds = ["noto_waved", "4x3", "circle"]
    ncol = 3
    nrow = 12
    show_flags(country_codes, kinds, ncol, nrow)

    plt.show()
