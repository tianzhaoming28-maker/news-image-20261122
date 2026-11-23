# news-image-20261122

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261122)
[![competition](https://img.shields.io/badge/competition-news--image--20261122-green)](https://github.com/tianzhaoming28-maker/news-image-20261122)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

Sum up the world's news of Sunday 22 November 2026 in one image.

The front page leads with the collapse of the COP31 climate talks in
Antalya — the longest COP in history ending with no deal — and carries
seven more stories from the day: Iran's strike on Bahrain, a Russian
drone levelling a Kyiv apartment block, the Indonesian candy-factory
fire, BepiColombo reaching Mercury, the US spy chief's rebuke of
Trump's "friend" label for Putin, settler arson in the West Bank, and
Shuri Castle rising again in Okinawa. Every story is double-sourced
in [SOURCES.md](SOURCES.md).

## Run it

```sh
python3 draw.py        # renders entry.png (1024x1024, Pillow)
node pack.mjs          # embeds entry.png into main.ts as one base64 line
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

`main.ts` decodes the embedded image and writes it to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`), byte for
byte identical to `entry.png`.

---

Built for the [make.fun](https://make.fun/r/qn2pqd71) bounty
news-image-20261122 — $100 shared by the 50 best-ranked images.
