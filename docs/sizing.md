# Sizing

Every physical size here is a **proposed starting point** for the manufacturer and packaging printer to confirm. Final dielines, film widths and wipe dimensions come from them. Screen and social sizes are final.

## Product lineup

| Pack | Count | Wipe size (unfolded) | Pack size (L × W × H) | Where it lives |
| --- | --- | --- | --- | --- |
| **Original 40-pack** | 40 | 7.5 × 8 in (190 × 203 mm) | 8.3 × 4.7 × 2 in (211 × 119 × 51 mm) | Bathroom shelf, gym locker |
| **Aloe & Cucumber 40-pack** | 40 | 7.5 × 8 in | 8.3 × 4.7 × 2 in | Same as Original |
| **Unscented 40-pack** | 40 | 7.5 × 8 in | 8.3 × 4.7 × 2 in | Same as Original |
| **Travel Singles** | 20 sachets | 6 × 8 in, folded into the sachet | Carton 5.5 × 3.75 × 2.5 in; sachet 3 × 3.5 in (76 × 89 mm) | Gym bag, festival bum-bag, glovebox |
| **The Clutch** | 12 | 6 × 7 in (152 × 178 mm) | 5.75 × 3 × 0.5 in (146 × 76 × 13 mm) | Purse, jacket pocket, desk drawer |

The Clutch is designed to sit flat in a small purse: about the footprint of a phone and no thicker than one in a case. That's the size claim to use in copy: **"About the size of your phone."** The Size lineup preview draws every pack to scale next to a phone.

## Logo sizes

The wordmark is SHAT in `display` over WIPES in Inter 700 with wide tracking.

| Use | Minimum SHAT width | Notes |
| --- | --- | --- |
| Print | 0.75 in (19 mm) | Below this, drop WIPES and use SHAT alone |
| Screen | 72px | Site header, app icon tile |
| Favicon and app icon | 16px | Use a single `S` in `display`, lime on forest |

**Clear space:** keep empty space around the wordmark equal to the height of the letter H in SHAT on every side.

## Type on screens

The display sizes in the tokens are for desktop. On phones (under 640px wide) use the Mobile group, so a 105px headline doesn't break into one word per line.

| Desktop style | Desktop | Phone (under 640px) |
| --- | --- | --- |
| `display` | 105px | `display-mobile`, 56px |
| `heading-lg` | 89px | `heading-lg-mobile`, 48px |
| `heading` | 61px | `heading-mobile`, 40px |
| `heading-sm` | 45px | 32px |
| `subheading` | 36px | 26px |
| `body-lg` | 25px | 20px |
| `body` and smaller | unchanged | unchanged |

The display face still switches to Inter 700 below 60px on desktop. On phones the display face stays on at 40px and up, because the heavy uppercase look is the brand and phones are where most people will see it.

## Breakpoints

| Name | Width | Layout |
| --- | --- | --- |
| Phone | under 640px | One column, `space-16` side gutter, full-width buttons |
| Tablet | 640 to 1023px | Two columns, `space-24` gutter |
| Desktop | 1024px and up | Content rail at `page-max` (1200px), `space-32` gutter |

Tap targets are at least 44 × 44px everywhere.

## Social and ad formats

| Format | Size (px) | Safe zone |
| --- | --- | --- |
| Instagram and Facebook feed | 1080 × 1350 (4:5) | Keep the headline inside the middle 1080 × 1080 |
| Stories, Reels, TikTok | 1080 × 1920 (9:16) | Keep text out of the top 250px and bottom 340px (app UI covers them) |
| Square post | 1080 × 1080 | 64px margin on all sides |
| Web banner | 1200 × 628 | 48px margin; pack shot on the right half |
| Profile picture | 1080 × 1080, shown as a circle | Single lime `S` on forest-ink, centred |

Every social format follows the same recipe: a `forest-ink` or `paper` ground, one huge uppercase headline in `display`, a pack shot, and "No one has to know." as the sign-off.

## Print minimums

- Claim-pill text: 6pt minimum.
- Back-panel facts zone: whatever the market's labelling rules require, and never smaller than 6pt.
- Lime is printed as a spot colour or a checked CMYK build; see Packaging.
