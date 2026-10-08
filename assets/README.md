# Assets

Six SVGs, three pairs, one per theme. **Do not edit them by hand.**

They are produced by [`generate.py`](generate.py), which holds the geometry once
and substitutes only the palette. Both themes therefore come out of the same
template and cannot drift apart, which is the failure this guards against: a
colour that was tuned in light mode and never checked in dark.

```
python3 assets/generate.py
```

Palette is the Exynex warm paper set, taken from the `1. Exynex Web Design`
repository's own CSS tokens.

| | Light | Dark |
|---|---|---|
| Page | `#F4EEE2` | `#0E0C09` |
| Panel | `#FFFFFF` | `#17130E` |
| Ink | `#16120C` | `#F2EDE3` |
| Accent | `#DE4F1D` | `#ED6230` |

No web fonts. A README image is served through GitHub's camo proxy, which does
not fetch Google Fonts, so a reference to Instrument Serif would fall back to
whatever the viewer has and shift the layout. Generic families only.

Every figure in `metrics-*.svg` is counted rather than estimated, and the source
of each count is in a comment beside it in `generate.py`.
