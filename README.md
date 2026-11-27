# THE WORLD IN ONE DAY — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/knownmyface/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/knownmyface/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A single 1024×1024 image that sums up Thursday 26 November 2026's world news:
**60 stories across 7 regions**, in one newspaper front page.

## What's on the page

- **3 large illustrated leads** — the nor'easter that stopped the 100th Macy's
  parade; Kyiv hit overnight by ballistic missiles and 113 drones; the Gulf
  war widening (Riyadh intercepts, Jazan refinery hit, 2 Italians killed in
  Kuwait). Each lead carries a "WHY IT MATTERS" line.
- **10 small illustrated cards** — Gukesh–Sindarov Game 3 drawn 1.5-1.5, the
  world's answer to the US tariff plan, the Cairo tanker toll at 31, India
  marking 18 years since 26/11, Mackenzie guilty on all counts, Andy Taylor
  dies at 65, Bears stun Lions 39-35, a second judge blocks the birthright
  order, Ukraine hits Savasleyka airbase, the $621.9m F-16 package.
- **47 more stories** in the index, every one with a named source.
- **Numbers band** — 100th parade, 113 / 87 drones, 31 dead in Cairo,
  600,000+ without power, 20% top tariff rate, 1.5-1.5 in Geneva.
- **Day by the Clock** — a UTC timeline strip across the whole day, 00:11 to
  21:30, honest times only.
- **Where It Happened** — a numbered dotted world map with place labels next
  to pins and a legend under the map. Two places (Kuwait City, Washington)
  are named in the legend instead of pinned: their neighbours sit too close
  for a separate pin, so no pin was faked.
- **The Tariff Plan, in Rates** — bar chart of the USTR's capped tariff rates
  (USTR via Reuters), with the 40% China headline rate if the truce fails.
- **DATE CHECK** — 11 lookalike stories that are NOT 26 Nov news (COP31, the
  House majority, the Netanyahu judges, the Solomon Islands treaty, and more),
  plus **NOT YET HAPPENED** and **WHAT TO WATCH ON FRIDAY**.

Every story was verified against Reuters / BBC / AP / IANS / Chess.com /
Ukrinform before drawing. Unverified claims are flagged [CLAIM]; forecasts
[FORECAST]. Nothing was invented — where the day's data was not yet published,
the image says so.

## How it is built

`render.py` draws everything from scratch with Pillow — flat code-drawn
illustrations, no photos, no network, no randomness. Running it twice produces
byte-identical output:

```sh
python3 render.py   # writes entry.png (1024x1024, < 1 MiB)
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`).

## License

MIT — see [LICENSE](LICENSE).
