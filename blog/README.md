# Stories & Solutions blog (runs itself with Claude)

A blog that writes a new helpful post every week, publishes it as a website, and is set up so AI assistants (ChatGPT, Claude, Perplexity, Google's AI answers) can read it and recommend your dealership.

## How it works

```
Every Monday (automatic)
   │
   ├─ 1. Pick what to write:  a real customer story in inbox/  →  otherwise the next idea in topics.txt
   ├─ 2. Writer agent (Claude) drafts the post
   ├─ 3. Editor agent (Claude) checks it against the rules and fixes problems
   ├─ 4. The post is saved in posts/
   └─ 5. The website is rebuilt and published
```

## Files you'll touch

| File | What it's for |
| --- | --- |
| `site.json` | **Your dealership's details.** Fill this in first. The AI only says things about you that are in here. |
| `topics.txt` | Ideas for solution posts, one per line. Add your own any time. |
| `inbox/` | Real customer stories. Copy `inbox/TEMPLATE.md`, fill it in, and set `Customer permission: yes`. |
| `posts/` | The finished posts. You can edit or delete them like any file. The first one is an example. |

You won't need to touch `scripts/` or `.github/workflows/blog.yml`.

## What makes it easy for AI to find and recommend you

- **Answer-first writing.** Every post opens with a 2–3 sentence answer, then key takeaways, then sections headed by real questions, then an FAQ.
- **Structured data** on every page tells machines "this is a car dealership, here's its address and phone, this is an article, these are questions and answers".
- **`llms.txt` and `llms-full.txt`**: plain-text summaries made for AI tools.
- **`robots.txt`** that welcomes the AI crawlers by name, plus a `sitemap.xml` and an RSS `feed.xml`.
- **The same name, address and phone everywhere.** AI tools trust businesses whose details match across the web, so make `site.json` match your Google Business Profile exactly.

## Built-in honesty rules

The writer and editor agents are told never to invent customers, quotes, reviews, prices, interest rates or awards. Fake testimonials break FTC rules and hurt trust with search engines and AI tools. Real stories from `inbox/` are the most valuable thing you can feed it.

## One-time setup (about 15 minutes)

1. **Fill in `site.json`** with your real details. Set `blog_url` to where the blog will live (see step 4).
2. **Get a Claude API key** at <https://console.anthropic.com> (Settings → API keys). Each post costs roughly a few cents to run.
3. **Add the key to GitHub:** in this repo go to Settings → Secrets and variables → Actions → New repository secret. Name it `ANTHROPIC_API_KEY` and paste the key.
4. **Turn on the website:** Settings → Pages → under "Source" pick **GitHub Actions**. Your blog address will be `https://<your-github-name>.github.io/<repo-name>/`.
5. **Merge this work into your default branch.** GitHub only runs the weekly schedule from the default branch.
6. **Try it now:** Actions tab → "Blog" → **Run workflow**. In a few minutes a new post appears in `posts/` and on the website.

After that it runs by itself every Monday.

## Tips to get recommended by AI

- Link to the blog from your main website and your Google Business Profile.
- Add a real customer story to `inbox/` whenever you can. One a month makes a big difference.
- Keep `topics.txt` full of questions customers actually ask your staff.
- Want a post more often? Change the `cron` line in `.github/workflows/blog.yml` (ask Claude to help).

## Preview on your own computer (optional)

```bash
python blog/scripts/build_site.py      # builds the site into blog/public/
# then open blog/public/index.html in your browser
```

To write a post from your computer: `pip install -r blog/requirements.txt`, set `ANTHROPIC_API_KEY`, then run `python blog/scripts/write_post.py`.
