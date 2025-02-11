import pkg_resources

import numpy as np
import json

import numpy as np
import json
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from typing import Literal


class Flags:
    _cached = {}

    @classmethod
    def get_available_kinds(cls):
        fn = pkg_resources.resource_filename(__name__, "data/flags.json")
        j = json.load(open(fn))
        return j

    def get_default_boundary_path(self):
        """
        We use flag of SO and take its first path as a boundary path.
        """
        arr = self.get_arr("SO")
        split_index = arr["split_index"]

        vertices = np.split(arr["vertices"], split_index)
        codes = np.split(arr["codes"], split_index)

        return vertices[0], codes[0]


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

        self._boundary_vertices_codes = self.get_default_boundary_path()

    def get_arr(self, country_code):
        d = {}
        for k in ["split_index", "facecolors", "vertices", "codes"]:
            d[k] = self._arr[f"{country_code}_{k}"]

        return d

    def _draw(self, country_code, add_artist, scale=1,
              boundary_prop=None):
              # pad=0,
              # pad_prop=None):
        """

        pad_prop : dictionary for padded background. e.g. {"fc": "none", "ec": "k", "lw": 1}. A specail key is "skia_linejoin". This is used for get_padded_boundary. Possible values are "miter", "bevel" and "round", Default is "round".
        """
        # _, _, xmax, ymax = self._j[country_code]["viewbox"]
        arr = self.get_arr(country_code)
        split_index = arr["split_index"]

        vertices = np.split(arr["vertices"], split_index)
        codes = np.split(arr["codes"], split_index)

        if boundary_prop is not None:
            # boundary_prop0.update(boundary_prop)
            v0, c0 = self._boundary_vertices_codes
            boundary = Path(vertices=v0*scale,
                            codes=c0)

            patch = PathPatch(boundary, **boundary_prop)
            add_artist(patch)

        path_prop_list = []
        for v, c, fc in zip(vertices, codes, arr["facecolors"]):
            p = Path(vertices=v*scale, codes=c)
            prop = dict(facecolor=fc)
            path_prop_list.append((p, prop))

        for p, prop in path_prop_list:
            patch = PathPatch(p, ec="none", **prop)
            add_artist(patch)

    def get_drawing_area(self, country_code, wmax=np.inf, hmax=np.inf,
                         pad=0.,
                         boundary_prop=None):
        """
        pad : pad in the same unit as wmax and hmax. wmax and hamx does not include pad.

        boundary_prop : The boundary patch, which is assumed to be a first path, will be updated with this prop.
        """

        _, _, w, h = self._j[country_code]["viewbox"]

        if wmax == np.inf and hmax == np.inf:
            scale = 1
        else:
            scale = min([wmax / w, hmax / h])

        from matplotlib.offsetbox import DrawingArea
        da = DrawingArea(scale*w+2*pad, scale*h+2*pad,
                         xdescent=pad, ydescent=pad)
        self._draw(country_code, da.add_artist, scale, boundary_prop=boundary_prop)

        return da

    def show_flag(self, ax, country_code, pad=10, boundary_prop=None):

        if country_code not in self._j:
            raise KeyError(f"{country_code} not in dictionary")

        self._draw(country_code, ax.add_patch, boundary_prop=boundary_prop)

        ax.set_aspect(1)
        _, _, xmax, ymax = self._j[country_code]["viewbox"]
        ax.set(xlim=(-pad, xmax+pad), ylim=(-pad, ymax+pad))

    @classmethod
    def show_flag_kinds(cls, subplotspec, country_code, kinds=None,
                        boundary_prop=None,
                        axis_off=True):

        if kinds is None:
            kinds = cls.get_available_kinds()

        flagss = [cls(k) for k in kinds]

        inner_grid = subplotspec.subgridspec(1, len(flagss), wspace=0.11, hspace=0)
        axs = inner_grid.subplots()  # Create all subplots for the inner grid.

        for ax, flags in zip(axs, flagss):
            try:
                flags.show_flag(ax, country_code, boundary_prop=boundary_prop)
            except KeyError:
                pass
            ax.set(xticks=[], yticks=[], title=f"{flags._kind}")
            ax.set_aspect(1)
            if axis_off:
                ax.set_axis_off()


    @classmethod
    def get_flags_summary(cls):
        """
        returns a list of available flag codes and a dictionary of missing codes for each kind.
        """
        kinds = cls.get_available_kinds()

        jj = {}
        for kind in kinds:
            fn_json = pkg_resources.resource_filename(__name__, f"data/flags_{kind}.json")
            j = json.load(open(fn_json, "r"))
            jj[kind] = j

        all_country_codes = set()
        for kind in kinds:
            all_country_codes.update(jj[kind].keys())

        missing_codes = {}
        for kind in kinds:
            j = jj[kind]
            missing_codes[kind] = all_country_codes.difference(j.keys())

        return list(sorted(all_country_codes)), missing_codes

    @classmethod
    def print_flags_summary(cls):

        all_country_codes, missing_codes = cls.get_flags_summary()
        print("[All Codes]")
        while all_country_codes:
            print(" ".join(all_country_codes[:25]))
            all_country_codes = all_country_codes[25:]

        print("")
        print("[Missing Codes]")
        for kind, missing in missing_codes.items():
            print(f"{kind}: ", " ".join(missing))
