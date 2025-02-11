
def prepare_figure(fig, nrows: int, ncols: int, nax=None, nsubcols=1):
    """
    Prepare figure with nrows x ncols axes. The axes order increase columnwise first.
    Each axes can be subdiveded by nsubcols.
    """
    if nax is None:
        nax = nrows * ncols

    gs_root = fig.add_gridspec(1, ncols)

    axs = []
    for gs in gs_root:
        gss =  gs.subgridspec(nrows, nsubcols)
        for irow in range(nrows):
            ax3 = [fig.add_subplot(gss[irow, icol]) for icol in range(nsubcols)]
            axs.append(ax3)
            if len(axs) >= nax:
                return axs

    return axs


def iter_axes_rows(nrows, ncols, nax, nsubcols=1, **fig_params):
    import matplotlib.pyplot as plt

    while nax > 0:

        fig = plt.figure(**fig_params)
        axs = prepare_figure(fig, nrows, ncols, nax=nax, nsubcols=nsubcols)

        for ax_row in axs:
            yield ax_row

        nax -= len(axs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    figsize = (8, 10)
    nrows, ncols = 4, 3

    for ax_row in iter_axes_rows(nrows, ncols, 16, nsubcols=2, figsize=figsize):
        pass

