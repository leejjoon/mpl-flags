from pathlib import Path
import os
import re
from io import BytesIO
import json

import numpy as np
from mpl_simple_svg_parser import SVGMplPathIterator


def replace_mask_to_clippath(fio):
    svg = fio.read()
    svg = svg.replace(b"mask=", b"clip-path=")
    svg = svg.replace(b"mask", b"clipPath")
    return BytesIO(svg)


if False:
    fio = open("../third_party/circle-flags/flags/kr.svg", "rb")
    svgio = replace_mask_to_clippath(fio)

flag_re = re.compile('([a-zA-Z]{2}).svg')
flag_re_emoji = re.compile('emoji_u(1f1[0-9a-f]{2})_(1f1[0-9a-f]{2}).svg')


def _flag_char(char_str):
    return chr(ord('A') + int(char_str, 16) - 0x1f1e6)


def _flag_name_from_emoji_file_name(fn):

  m = flag_re_emoji.match(os.path.basename(fn))

  if m:
      flag_short_name = _flag_char(m.group(1)) + _flag_char(m.group(2))

      return flag_short_name


def _flag_name_from_file_name(fn):
  m = flag_re.match(os.path.basename(fn))
  if m:
      return fn.name[:2].upper()


flags_info = [
    dict(
        kind="1x1",
        root=Path("../third_party/flag-icons/flags/1x1"),
        get_flag_name=_flag_name_from_file_name,
        preprocess=None,
    ),
    dict(
        kind="noto_waved",
        root=Path("../third_party/noto-emoji/third_party/region-flags/waved-svg"),
        get_flag_name=_flag_name_from_emoji_file_name,
        preprocess=None,
    ),
    dict(
        kind="noto_original",
        root=Path("../third_party/noto-emoji/third_party/region-flags/svg"),
        get_flag_name=_flag_name_from_file_name,
        preprocess=None,
    ),
    dict(
        kind="4x3",
        root=Path("../third_party/flag-icons/flags/4x3"),
        get_flag_name=_flag_name_from_file_name,
        preprocess=None,
    ),
    dict(
        kind="simple",
        # The original svg uses mask to make it circular. The mask
        # directive is ignored by SVGMplPathIterator, so this gives 1x1
        # rectangle shape flags.
        root=Path("../third_party/circle-flags/flags"),
        get_flag_name=_flag_name_from_file_name,
        preprocess=None,
    ),
    dict(
        kind="circle",
        # The original svg uses mask to make it circular. We replace the mask
        # directive to clip path, which is supported by SVGMplPathIterator.
        root=Path("../third_party/circle-flags/flags"),
        get_flag_name=_flag_name_from_file_namem,
        preprocess=replace_mask_to_clippath
    )
]


def convert(kind, root, get_flag_name, preprocess=None):

    codes = []
    for fn in sorted(root.glob("*.svg")):
        code = get_flag_name(fn)
        if code is not None:
            codes.append((code, fn))

    by_codes = {}
    for code, fn in codes:
        print(code)
        if preprocess is None:
            fio = open(fn, "rb")
        else:
            fio = preprocess(open(fn, "rb"))

        svg_mpl_path_iterator = SVGMplPathIterator(fio.read(), svg2svg=True,
                                                   pico=True)
        k = list(svg_mpl_path_iterator.iter_mpl_path_patch_prop())
        viewbox = svg_mpl_path_iterator.viewbox
        by_codes[code] = dict(mpl_path_patch_prop=k,
                              viewbox=viewbox,
                              filename=fn)

    master_dict = {}
    with_gradient = set()
    for country, c in by_codes.items():
        vertices = []
        codes = []
        facecolors = []
        for path, prop in c["mpl_path_patch_prop"]:
            if isinstance(prop["fc"], str):
                # FIXME We need to support gradients!
                with_gradient.add(country)
                facecolors.append([0, 0, 0, 0])
            else:
                facecolors.append(np.concatenate([prop["fc"], [prop["alpha"]]]))
            vertices.append(path.vertices)
            codes.append(path.codes)

        nn = [len(c) for c in codes]

        master_dict.update({f"{country}_split_index": np.add.accumulate(nn[:-1]),
                            f"{country}_facecolors": np.vstack(facecolors),
                            f"{country}_vertices": np.concatenate(vertices),
                            f"{country}_codes": np.concatenate(codes),
                            },)

    # print("with gradient:", sorted(with_gradient))

    np.savez(f"flags_{kind}.npz", **master_dict)

    master_json = {}
    for country, c in by_codes.items():
        master_json[country] = dict(viewbox=c["viewbox"],
                                    filename=c["filename"].as_posix())
    json.dump(master_json, open(f"flags_{kind}.json", "w"), indent=2)


def main():
    for info in flags_info:
        convert(info["kind"], info["root"], info["get_flag_name"],
                preprocess=info.get("preprocess", None))


if __name__ == '__main__':
    main()
