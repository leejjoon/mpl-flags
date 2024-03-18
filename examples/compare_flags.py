import numpy as np
import json
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from mpl_flags import get_all_country_codes, Flags


def prepare_axes(fig, ncol, nrow, nkind, nax=None):

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
        fig.clf()
        axs = prepare_axes(fig, ncol, nrow, nkind, nax=len(country_codes))

        for ax3, country_code in zip(axs, country_codes):
            for ax, flags in zip(ax3, flagss):
                try:
                    flags.show_flag(ax, country_code)
                except KeyError:
                    print(f"no flag of {country_code}")
                ax.set_axis_off()

            ax3[0].annotate(country_code, (-0.1, 0.5), xycoords="axes fraction",
                            annotation_clip=False,
                            rotation=90, rotation_mode="anchor", va="baseline", ha="center")

        country_codes = country_codes[ncol*nrow:]


def show_all():
    import matplotlib.pyplot as plt

    country_codes = sorted(get_all_country_codes())
    kinds = ["noto_waved", "4x3", "circle"]
    ncol = 3
    nrow = 12
    show_flags(country_codes, kinds, ncol, nrow)

    plt.show()


if __name__ == '__main__':
    show_all()
