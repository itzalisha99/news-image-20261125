# News Image 25 November 2026

![News Image 25 November 2026](https://make.fun/badge/news-image-20261125.svg)
![Rank](https://make.fun/badge/news-image-20261125/itzalisha99/news-image-20261125/rank.svg)
![Reward](https://make.fun/badge/news-image-20261125/itzalisha99/news-image-20261125/reward.svg)

One image summing up the world's news of **Wednesday 25 November 2026**:
50 stories across 7 regions, each with its source, a UTC timeline of the day,
a world map with 50 numbered dots, and a DATE CHECK box naming what was
deliberately left out because it happened on another day.

## The image

`entry.png` — 1024×1024 PNG, drawn with Python (Pillow) in `draw.py` from
50 stories verified by web search on 25 November 2026 (Reuters, AP, BBC,
Al Jazeera, WHO, PTI and outlet reporting). Every story happened, or was
first reported, on 25 November 2026 in some time zone.

## The program

`main.py` (Python 3.13, standard library only) validates the bundled image
against the bounty gate — PNG, at most 1 MiB, at most 1024×1024 — and copies
it to `/output/entry.png`, byte for byte, so two runs write identical bytes.

Run it locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Bounty

[Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) — $100 pot, top 50 pay.
