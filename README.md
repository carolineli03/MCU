# The MCU, In Order

A single-page, self-contained watch-order flowchart for the Marvel Cinematic Universe.

- `index.html` — the whole thing. No build step, no dependencies (Google Fonts is the only external request).
- Open it locally by double-clicking, or serve it with any static host.

## Publishing with GitHub Pages

1. Repo → **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `main`, folder `/ (root)` → **Save**

The page goes live at `https://carolineli03.github.io/MCU/`.

## Editing the data

Titles live in `DATA`, characters in `CHARS`, storylines in `THREADS` and
relationships in `RELS`, all inside `index.html`.

After changing any of them, run:

```bash
python3 tools/prerender.py
```

That rewrites the plain-HTML copy of the watch order, the character list and the
storylines inside `index.html`. The page's own scripts replace those blocks on
load, so visitors see no difference — but search engines and anyone whose
JavaScript fails get the real content instead of an empty page.

Add new titles to the **end** of `CODE_ORDER`, never in the middle: progress
codes are one bit per title in that order, so inserting one would scramble every
code people have already saved.
