# Shat Wipes

**No one has to know.**

The design package for Shat Wipes: personal wipes for people 18 to 40, with a snarky voice and a loud, heavy look. Deep forest green, a jolt of lime, and huge uppercase type.

## What's in here

| Folder or file | What it is |
| --- | --- |
| `docs/brand-book.md` | Start here. Who it's for, the voice, taglines, colours, type, layout, imagery and icons |
| `docs/packaging.md` | The five packs and what goes on every panel |
| `docs/sizing.md` | Pack and wipe sizes, logo sizes, phone vs. desktop type sizes, breakpoints, social formats |
| `brand/tokens.json` | Every colour, type style, spacing step, corner radius and shadow, with a note on when to use each |
| `brand/tokens.css` | The same tokens as CSS variables, ready to drop into a website |
| `components/` | Buttons, tags, inputs, cards and pack mock-ups: `bundle.css` holds the styles and each folder has notes and a preview |

## The five packs

| Pack | Count | Colours |
| --- | --- | --- |
| Original | 40 | Forest green with a lime wordmark |
| Aloe & Cucumber | 40 | Lime with a forest wordmark |
| Unscented | 40 | Pale grey with a forest wordmark |
| Travel Singles | 20 sachets | Spruce green with a lime wordmark |
| The Clutch (purse size) | 12 | Black with a lime wordmark |

Pack and wipe dimensions in `docs/sizing.md` are proposed starting points to confirm with the manufacturer.

## Using the tokens on a website

Add this line inside your page's `<head>`:

```html
<link rel="stylesheet" href="brand/tokens.css">
```

Then use the variables in your CSS, for example `background: var(--forest-ink); color: var(--lime-voltage);`.

## Dealership blog

`blog/` holds a self-running "Stories & Solutions" blog: Claude writes and edits a new post every week and publishes it as a website that AI search tools can read. See `blog/README.md` for setup.
