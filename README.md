# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/lianyongmin-afk/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/lianyongmin-afk/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026,
drawn by a program. Entry for the [news-image-20261123 competition](https://make.fun/bounty/news-image-20261123)
on [make.fun](https://make.fun).

## What the image shows

A broadsheet-style front page, 1024 by 1024 pixels: a navy masthead
naming the date, then six stories from the day, each with a number, a
section tag, a pictogram and a headline:

1. COP31 climate talks collapse — nearly 200 countries leave Antalya
   with no deal on fossil fuels or finance (SCMP · The Economic Times)
2. Democrats take the House: 258 seats — their best House result since
   1992, flipping control of Congress (SCMP · The Economic Times)
3. Russian strikes kill 11 in Kyiv region — homes and a supermarket in
   Vyshneve hit, Ukraine says (Arab News PK)
4. Drone strikes hit Khartoum and a UN building — strikes reported in
   Sudan's capital (AFP via The Manila Times)
5. Factory fire in Indonesia: 3 dead, 36 missing — rescue teams search
   the burned-out plant (The Manila Times)
6. Paolo Bulgari, jeweller to Hollywood, dies at 89 — the chairman who
   turned a Roman shop into a global luxury house (The Economic Times)

All six stories happened, or were first reported, on 23 November 2026.
Two stories first reported on earlier days (the BepiColombo Mercury
arrival of 21 November, the capture of "El Chapo Isidro" on 20 November)
were checked and deliberately left out.

## How it works

`main.py` is the entry point. It checks the pre-rendered `entry.png`
against the gate limits (PNG, at most 1 MiB, at most 1024 by 1024) and
copies it byte for byte to `$MAKEFUN_OUTPUT_DIR/entry.png`
(`/output/entry.png` when the variable is unset). Standard library only,
so two runs write identical files. `generate.py` drew the image with
Pillow: masthead, cards and pictograms are all drawn from primitives,
no image assets.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the image from scratch:

```sh
python3 generate.py
```

The output is deterministic: two runs write byte-identical PNG files,
1024 by 1024 pixels and under the 1 MiB limit.

## Files

- `main.py` — entry point, validates and copies `entry.png` to the output directory
- `generate.py` — all drawing code
- `entry.png` — the image the program produces
- `LICENSE` — MIT

## License

MIT. See `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7hwn368j&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
