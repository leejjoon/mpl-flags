# mpl-flags

National flags for Matplotlib.


## Flags data

`mpl-flags` contains the flag data in vector format readily usable with
Matplotlib. The original flags data are in svg format, and are converted to
matplotlib's `Path` data using `mpl-simple-svg-parser`. `mpl-flags` does not
contain the original svg files, only the converted data in numpy format
(vertices and codes).

The flag data is collected from various sources. Currently, it includes flags from

1. Google's noto color emoji font : https://github.com/googlefonts/noto-emoji
2. circle-flags : https://github.com/HatScripts/circle-flags
3. flag-icons : https://github.com/lipis/flag-icons

Different sources can render the flags differently.

## Usage

```python
from mpl_flags import Flags

flags = Flags("noto_waved") # You initialize the Flags class specifying what kind of
                            # flags you like to use.
                            # `noto_waved` is flags from google's noto emoji fonts.

fig, ax = plt.subplots(figsize=(3, 3))
flags.show_flag(ax, "KR")
```

```python
from matplotlib.offsetbox import AnnotationBbox

flags = Flags("noto_original")

fig, ax = plt.subplots(figsize=(3, 3))
da = flags.get_drawing_area("KR", wmax=100)
ab = AnnotationBbox(da, (0.5, 0.5), frameon=True,
                    box_alignment=(0.5, 0.5))
ax.add_artist(ab)
```

## Installation

You can install using `pip`:

```bash
pip install mpl_flags
```

## Development Installation


```bash
pip install -e ".[dev]"
```

