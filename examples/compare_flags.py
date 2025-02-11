import matplotlib.pyplot as plt

from mpl_flags import Flags

from iter_axes import iter_axes_rows

def show_flags(country_codes, kinds, nrows, ncols, figsize=(8, 10)):

    flagss = [Flags(k) for k in kinds]

    nkind = len(flagss)

    boundary_prop = dict(ec="k")

    for ax_row, cc in zip(iter_axes_rows(nrows, ncols,
                                         len(country_codes), nsubcols=nkind,
                                         figsize=figsize),
                          country_codes):

            for ax, flags in zip(ax_row, flagss):
                try:
                    flags.show_flag(ax, cc, boundary_prop=boundary_prop)
                except KeyError:
                    print(f"no flag of {cc}")
                ax.set_axis_off()

            ax_row[0].annotate(cc, (-0.1, 0.5), xycoords="axes fraction",
                               annotation_clip=False,
                               rotation=90, rotation_mode="anchor",
                               va="baseline", ha="center")

def show_all():
    """
    Show all available flags in the mpl_flags package.
    """
    import matplotlib.pyplot as plt

    availabel_country_codes, _ = Flags.get_flags_summary()
    country_codes = availabel_country_codes
    kinds = ["noto_waved", "4x3", "circle"]
    ncols = 3
    nrows = 12
    show_flags(country_codes, kinds, nrows, ncols)

    plt.show()


if __name__ == '__main__':
    show_all()
