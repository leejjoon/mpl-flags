import pkg_resources

import numpy as np
import json

import numpy as np
import json
from matplotlib.path import Path
from matplotlib.patches import PathPatch


class Flags:
    _cached = {}

    @classmethod
    def get_available_kinds(cls):
        fn = pkg_resources.resource_filename(__name__, "data/flags.json")
        j = json.load(open(fn))
        return j

    def __init__(self, kind="noto"):
        # FIXME I wanted to cache the resources. not sure this is good enough

        if kind in self._cached:
            arr = self._cached[kind]["arr"]
            j = self._cached[kind]["j"]

        else:
            fn_npz = pkg_resources.resource_filename(__name__, f"data/flags_{kind}.npz")
            fn_json = pkg_resources.resource_filename(__name__, f"data/flags_{kind}.json")

            arr = np.load(fn_npz)
            j = json.load(open(fn_json, "r"))

            self._cached[kind] = dict(arr=arr, j=j)

        self._kind = kind
        self._arr = arr
        self._j = j

    def get_arr(self, country_code):
        d = {}
        for k in ["split_index", "facecolors", "vertices", "codes"]:
            d[k] = self._arr[f"{country_code}_{k}"]

        return d

    def _draw(self, country_code, add_artist, scale=1):
        # _, _, xmax, ymax = self._j[country_code]["viewbox"]
        arr = self.get_arr(country_code)
        split_index = arr["split_index"]

        vertices = np.split(arr["vertices"], split_index)
        codes = np.split(arr["codes"], split_index)
        path_prop_list = []
        for v, c, fc in zip(vertices, codes, arr["facecolors"]):
            p = Path(vertices=v*scale, codes=c)
            prop = dict(facecolor=fc)
            path_prop_list.append((p, prop))

        for p, prop in path_prop_list:
            patch = PathPatch(p, ec="none", **prop)
            add_artist(patch)

    def get_drawing_area(self, country_code, wmax=np.inf, hmax=np.inf):

        _, _, w, h = self._j[country_code]["viewbox"]

        if wmax == np.inf and hmax == np.inf:
            scale = 1
        else:
            scale = min([wmax / w, hmax / w])

        from matplotlib.offsetbox import DrawingArea
        da = DrawingArea(scale*w, scale*h)

        self._draw(country_code, da.add_artist, scale)

        return da

    def show_flag(self, country_code, ax):

        if country_code not in self._j:
            raise KeyError(f"{country_code} not in dictionary")

        self._draw(country_code, ax.add_patch)

        ax.set_aspect(1)
        _, _, xmax, ymax = self._j[country_code]["viewbox"]
        ax.set(xlim=(0, xmax), ylim=(0, ymax))

    @classmethod
    def show_flag_kinds(cls, subplotspec, country_code, kinds=None):

        if kinds is None:
            kinds = cls.get_available_kinds()

        flagss = [cls(k) for k in kinds]

        inner_grid = subplotspec.subgridspec(1, len(flagss), wspace=0.11, hspace=0)
        axs = inner_grid.subplots()  # Create all subplots for the inner grid.

        for ax, flags in zip(axs, flagss):
            flags.show_flag(country_code, ax)
            ax.set(xticks=[], yticks=[], title=f"{flags._kind}")
            # ax.set_axis_off()


def get_all_country_codes():
    all_country_codes = set()
    for kind in ["circle", "noto_original", "1x1", "4x3"]:
            fn_json = pkg_resources.resource_filename(__name__, f"data/flags_{kind}.json")
            j = json.load(open(fn_json, "r"))
            all_country_codes.update(j.keys())

    if False:
        for kind in ["circle", "noto_original", "1x1", "4x3"]:
            j = json.load(open(f"data/flags_{kind}.json", "r"))
            vv = all_country_flags.difference(j.keys())
            print(vv)

    return all_country_codes
