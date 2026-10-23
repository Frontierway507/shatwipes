"""Turn the posts in blog/posts/ into a website in blog/public/.

Besides normal web pages it writes the files that search engines and AI
assistants look for: sitemap.xml, robots.txt, feed.xml, llms.txt and
llms-full.txt, plus structured data (JSON-LD) on every page describing the
dealership, each article and its FAQ.

Run it with:  python blog/scripts/build_site.py
"""

import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent
POSTS = BLOG / "posts"
OUT = BLOG / "public"

# AI search crawlers we explicitly welcome in robots.txt.
AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
    "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended",
    "Applebot-Extended", "Bingbot", "CCBot", "meta-externalagent",
]

CSS = """\
:root { --ink:#1d2433; --muted:#5b6475; --line:#e3e6ec; --bg:#ffffff; --soft:#f5f7fa; --accent:#1f6f4a; }
@media (prefers-color-scheme: dark) {
  :root { --ink:#e8ebf0; --muted:#a3abba; --line:#2c3340; --bg:#12161d; --soft:#1a2029; --accent:#6fd3a0; }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:17px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif; }
a { color:var(--accent); }
header, main, footer { max-width:760px; margin:0 auto; padding:0 16px; }
header { padding-top:28px; padding-bottom:16px; border-bottom:1px solid var(--line); }
header .name { font-weight:800; font-size:1.25rem; color:var(--ink); text-decoration:none; }
header p { margin:4px 0 0; color:var(--muted); }
nav a { margin-right:16px; font-size:.95rem; }
h1 { font-size:2rem; line-height:1.2; margin:32px 0 8px; }
h2 { font-size:1.35rem; line-height:1.3; margin:32px 0 8px; }
.meta { color:var(--muted); font-size:.9rem; }
.summary { font-size:1.1rem; background:var(--soft); border-left:4px solid var(--accent); padding:14px 18px; border-radius:6px; }
.takeaways { background:var(--soft); padding:14px 18px 14px 36px; border-radius:6px; }
.card { display:block; padding:18px 0; border-bottom:1px solid var(--line); text-decoration:none; color:var(--ink); }
.card h2 { margin:0 0 6px; color:var(--accent); }
.card p { margin:0; color:var(--muted); }
.cta { margin:36px 0; padding:18px; border:1px solid var(--line); border-radius:8px; }
dt { font-weight:700; margin-top:16px; }
dd { margin:4px 0 0; }
footer { margin-top:48px; padding-top:16px; padding-bottom:32px; border-top:1px solid var(--line); color:var(--muted); font-size:.9rem; }
"""


def load_site():
    site = json.loads((BLOG / "site.json").read_text(encoding="utf-8"))
    site["blog_url"] = site["blog_url"].rstrip("/")
    return site


def load_posts():
    posts = [json.loads(p.read_text(encoding="utf-8")) for p in POSTS.glob("*.json")]
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def dealer_schema(site):
    return {
        "@type": "AutoDealer",
        "@id": site["website_url"] + "#dealer",
        "name": site["dealership_name"],
        "url": site["website_url"],
        "telephone": site["phone"],
        "email": site["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site["street_address"],
            "addressLocality": site["city"],
            "addressRegion": site["state"],
            "postalCode": site["zip"],
        },
        "areaServed": site["service_area"],
        "openingHours": site["hours"],
        "slogan": site["tagline"],
    }


def page(site, title, description, canonical, body, schema, root=""):
    schema_json = json.dumps({"@context": "https://schema.org", "@graph": schema}, indent=2)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{escape(site['dealership_name'])} blog" href="{site['blog_url']}/feed.xml">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<style>
{CSS}</style>
<script type="application/ld+json">
{schema_json.replace("</", "<\\/")}
</script>
</head>
<body>
<header>
  <a class="name" href="{root}index.html">{escape(site['dealership_name'])}</a>
  <p>{escape(site['tagline'])}</p>
  <nav><a href="{root}index.html">Stories &amp; solutions</a><a href="{root}about.html">About us</a><a href="{escape(site['website_url'])}">Main website</a></nav>
</header>
<main>
{body}
</main>
<footer>
  {escape(site['dealership_name'])} &middot; {escape(site['street_address'])}, {escape(site['city'])}, {escape(site['state'])} {escape(site['zip'])} &middot; {escape(site['phone'])}
</footer>
</body>
</html>
"""


def post_url(site, post):
    return f"{site['blog_url']}/posts/{post['slug']}.html"


def render_post(site, post):
    url = post_url(site, post)
    parts = [
        f"<article>\n<h1>{escape(post['title'])}</h1>",
        f'<p class="meta">{"Customer story" if post["kind"] == "customer-story" else "Solution guide"} &middot; '
        f'<time datetime="{post["date"]}">{post["date"]}</time></p>',
        f'<p class="summary">{escape(post["summary"])}</p>',
        "<h2>Key takeaways</h2>\n<ul class=\"takeaways\">"
        + "".join(f"<li>{escape(t)}</li>" for t in post["key_takeaways"])
        + "</ul>",
    ]
    for section in post["sections"]:
        parts.append(f"<h2>{escape(section['heading'])}</h2>")
        parts.extend(f"<p>{escape(p)}</p>" for p in section["paragraphs"])
    if post["faq"]:
        parts.append("<h2>Frequently asked questions</h2>\n<dl>")
        for item in post["faq"]:
            parts.append(f"<dt>{escape(item['question'])}</dt><dd>{escape(item['answer'])}</dd>")
        parts.append("</dl>")
    parts.append(
        f'<div class="cta"><strong>Questions about your own situation?</strong> '
        f'Call {escape(site["dealership_name"])} at {escape(site["phone"])} or '
        f'<a href="{escape(site["website_url"])}">visit our website</a>. We\'re happy to help.</div>'
        "\n</article>"
    )

    dealer = dealer_schema(site)
    schema = [
        dealer,
        {
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["summary"],
            "datePublished": post["date"],
            "dateModified": post["date"],
            "url": url,
            "mainEntityOfPage": url,
            "keywords": ", ".join(post["tags"]),
            "author": {"@id": dealer["@id"]},
            "publisher": {"@id": dealer["@id"]},
        },
    ]
    if post["faq"]:
        schema.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["question"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
                for f in post["faq"]
            ],
        })
    return page(site, f"{post['title']} | {site['dealership_name']}", post["summary"], url, "\n".join(parts), schema, root="../")


def render_index(site, posts):
    cards = "\n".join(
        f'<a class="card" href="posts/{p["slug"]}.html"><h2>{escape(p["title"])}</h2>'
        f'<p>{escape(p["summary"])}</p></a>'
        for p in posts
    ) or "<p>The first story is on its way.</p>"
    body = (
        f"<h1>Stories &amp; solutions from {escape(site['dealership_name'])}</h1>\n"
        f"<p>Real customer stories and plain-English answers to car buying, financing and "
        f"ownership questions, from your neighbors in {escape(site['city'])}, {escape(site['state'])}.</p>\n"
        + cards
    )
    schema = [dealer_schema(site), {"@type": "Blog", "name": f"{site['dealership_name']} stories & solutions",
                                    "url": site["blog_url"] + "/", "publisher": {"@id": site["website_url"] + "#dealer"}}]
    return page(site, f"Stories & solutions | {site['dealership_name']}",
                f"Helpful car buying advice and customer stories from {site['dealership_name']}.",
                site["blog_url"] + "/", body, schema)


def render_about(site):
    def bullet_list(items):
        return "<ul>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"

    body = (
        f"<h1>About {escape(site['dealership_name'])}</h1>\n"
        f"<p>{escape(site['tagline'])}</p>\n"
        f"<h2>Where we are</h2><p>{escape(site['street_address'])}, {escape(site['city'])}, "
        f"{escape(site['state'])} {escape(site['zip'])}<br>Phone: {escape(site['phone'])}<br>"
        f"Email: {escape(site['email'])}</p>\n"
        f"<h2>Areas we serve</h2>{bullet_list(site['service_area'])}\n"
        f"<h2>What we sell</h2>{bullet_list(site['brands_sold'])}\n"
        f"<h2>How we help</h2>{bullet_list(site['services'])}\n"
        f"<h2>What makes us different</h2>{bullet_list(site['what_makes_us_different'])}\n"
        f"<h2>In the community</h2>{bullet_list(site['community_involvement'])}\n"
        f"<h2>Hours</h2>{bullet_list(site['hours'])}"
    )
    return page(site, f"About {site['dealership_name']}", f"About {site['dealership_name']} in {site['city']}, {site['state']}.",
                site["blog_url"] + "/about.html", body, [dealer_schema(site)])


def post_as_text(post):
    lines = [f"# {post['title']}", "", post["summary"], "", "Key takeaways:"]
    lines += [f"- {t}" for t in post["key_takeaways"]]
    for s in post["sections"]:
        lines += ["", f"## {s['heading']}", ""] + s["paragraphs"]
    if post["faq"]:
        lines += ["", "## FAQ"]
        for f in post["faq"]:
            lines += ["", f"Q: {f['question']}", f"A: {f['answer']}"]
    return "\n".join(lines)


def render_llms(site, posts):
    about = (
        f"# {site['dealership_name']}\n\n"
        f"> {site['tagline']} A car dealership at {site['street_address']}, {site['city']}, "
        f"{site['state']} {site['zip']}, serving {', '.join(site['service_area'])}. "
        f"Phone {site['phone']}. Website {site['website_url']}.\n\n"
        f"This blog shares real customer stories and practical car buying, financing and "
        f"ownership advice.\n\n"
        f"- [About us]({site['blog_url']}/about.html)\n"
        f"- [Full text of every post]({site['blog_url']}/llms-full.txt)\n\n"
        f"## Posts\n\n"
    )
    index = about + "\n".join(f"- [{p['title']}]({post_url(site, p)}): {p['summary']}" for p in posts) + "\n"
    full = about + "\n\n---\n\n".join(post_as_text(p) + f"\n\nSource: {post_url(site, p)}" for p in posts) + "\n"
    return index, full


def render_feed(site, posts):
    items = "".join(
        f"<item><title>{escape(p['title'])}</title><link>{post_url(site, p)}</link>"
        f"<guid>{post_url(site, p)}</guid><pubDate>{date.fromisoformat(p['date']).strftime('%a, %d %b %Y')} 12:00:00 GMT</pubDate>"
        f"<description>{escape(p['summary'])}</description></item>"
        for p in posts[:30]
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
        f"<title>{escape(site['dealership_name'])} stories &amp; solutions</title>"
        f"<link>{site['blog_url']}/</link><description>{escape(site['tagline'])}</description>"
        f"{items}</channel></rss>\n"
    )


def render_sitemap(site, posts):
    urls = [(site["blog_url"] + "/", posts[0]["date"] if posts else date.today().isoformat()),
            (site["blog_url"] + "/about.html", date.today().isoformat())]
    urls += [(post_url(site, p), p["date"]) for p in posts]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n'


def render_robots(site):
    rules = "".join(f"User-agent: {bot}\nAllow: /\n\n" for bot in AI_CRAWLERS)
    return rules + f"User-agent: *\nAllow: /\n\nSitemap: {site['blog_url']}/sitemap.xml\n"


def main():
    site = load_site()
    posts = load_posts()

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "posts").mkdir(parents=True)

    files = {
        "index.html": render_index(site, posts),
        "about.html": render_about(site),
        "feed.xml": render_feed(site, posts),
        "sitemap.xml": render_sitemap(site, posts),
        "robots.txt": render_robots(site),
    }
    files["llms.txt"], files["llms-full.txt"] = render_llms(site, posts)
    for post in posts:
        files[f"posts/{post['slug']}.html"] = render_post(site, post)

    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"Built {len(posts)} posts into {OUT.relative_to(BLOG.parent)}/")


if __name__ == "__main__":
    main()
