# Packaging

The pack is the brand's billboard, so it gets the loudest version of the system. The goal: a customer can spot it from across a store aisle, and still not feel awkward carrying it in a gym bag.

## The formats

| Pack | Body | Wordmark | Use |
| --- | --- | --- | --- |
| **Original 40-pack** (soft flow-wrap, resealable) | `forest-ink` | `lime-voltage` | The hero SKU and the default everywhere |
| **Aloe & Cucumber 40-pack** | `lime-voltage` | `forest-ink` | The "fresh" variant, the inverse of Original |
| **Unscented 40-pack** | `fog` | `forest-ink` | Sensitive skin, no fragrance |
| **Travel Singles, 20 individually wrapped** (carton + sachets) | `spruce` | `lime-voltage` | Gym bags, festivals, dates |
| **The Clutch, 12-pack** (slim resealable pouch) | `obsidian` | `lime-voltage` | Purses, jacket pockets, desk drawers. About the size of a phone |

Variants are told apart by **inverting the same two or three colours**, not by adding new hues. Colour carries the variant and the words confirm it. The variant name always sits in a pill on the front.

## Front panel

1. **SHAT wordmark.** `display` face, uppercase, sized so the word fills about 90% of the panel width and bleeds slightly off the left edge. This is the joke and the shelf blocker.
2. **WIPES.** Inter 700, uppercase, wide tracking, directly under SHAT at about a fifth of its height.
3. **Tagline.** One line from the "nobody needs to know" set, Inter 700, sentence case. Each SKU gets its own:
   - Original: *No one has to know.*
   - Aloe & Cucumber: *Say less. Wipe more.*
   - Unscented: *We don't have to talk about it.*
   - Travel Singles: *Clean exit. No questions asked.*
   - The Clutch: *Fits in your purse. Fits in your plans.*
4. **Claim pills.** A row of `radius-pill` tags in `micro` uppercase along the bottom: count, the variant name, and one or two claims (e.g. `40 WIPES`, `ALOE + CUCUMBER`, `PLANT-BASED`).
5. **Peel flap.** A lime pill (forest on the lime pack) with copy: **PEEL HERE. NOBODY'S WATCHING.**

Keep the panel to these five pieces: no badges, starbursts or illustrations.

## The Clutch

The purse pack is the smallest pack and the most likely to come out in public, at a bar, on a date, in an office. It keeps the full front panel but tightens it:

- The `obsidian` body reads as a sleek black accessory, not a bathroom product.
- SHAT still fills about 90% of the width. At this size, drop the tagline to one short line and show only two claim pills (`12 WIPES` and `PURSE SIZE`).
- The peel flap copy shortens to **PEEL. NOBODY'S WATCHING.**
- The back panel skips the snark headline and goes straight to the plain-facts zone, because there's no room for both.

## Back panel

- The headline is the snark line, in `heading` face: *PAPER HAD ITS CHANCE.*
- Next comes a three-line "Why wipes" block in `body-sm`, a little snarky and fully truthful.
- Then comes the plain-facts zone in `caption` on a `fog` or `linen-mist` panel with `radius-card`: ingredients, directions, disposal, manufacturer and barcode. **This zone has no jokes** and follows whatever labelling the product and market require. Only print "flushable" or other claims once they've been tested and approved for the product.

## Little moments

- **Inside the reseal flap:** "You made it. We won't mention it."
- **Single sachet, front:** SHAT wordmark plus "Leave no trace. Seriously."
- **Carton tear strip:** "Open discreetly."
- **Shipping box tape:** "NOTHING TO SEE HERE" repeated in lime on forest-ink.
- **Mock warning label (alarm-red, sparingly):** "WARNING: May cause unreasonable confidence."

## Production notes

- Print lime as a spot colour (or a checked CMYK build) so it doesn't go muddy on flexible film. Proof it against the forest-ink body.
- Matte film with a gloss spot on the wordmark, so SHAT catches the light.
- Minimum claim-pill text: 6pt printed. The back-panel facts zone follows regulatory minimums.
