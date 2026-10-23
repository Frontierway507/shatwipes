"""Write one new blog post with two Claude agents: a writer and an editor.

1. Picks the work: a real customer story from inbox/ (if any), otherwise the
   next idea in topics.txt.
2. The writer agent drafts the post.
3. The editor agent checks it against the rules (no made-up facts, positive,
   helpful, easy for AI search tools to quote) and fixes anything wrong.
4. Saves the approved post to posts/ as JSON.

Run it with:  python blog/scripts/write_post.py
Needs the ANTHROPIC_API_KEY environment variable.
"""

import datetime
import json
import re
import shutil
import sys
from pathlib import Path

import anthropic

BLOG = Path(__file__).resolve().parent.parent
POSTS = BLOG / "posts"
INBOX = BLOG / "inbox"
TOPICS = BLOG / "topics.txt"

MODEL = "claude-opus-5-5"

POST_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "slug", "summary", "key_takeaways", "sections", "faq", "tags"],
    "properties": {
        "title": {"type": "string"},
        "slug": {"type": "string"},
        "summary": {"type": "string"},
        "key_takeaways": {"type": "array", "items": {"type": "string"}},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["heading", "paragraphs"],
                "properties": {
                    "heading": {"type": "string"},
                    "paragraphs": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "faq": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["question", "answer"],
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                },
            },
        },
        "tags": {"type": "array", "items": {"type": "string"}},
    },
}

REVIEW_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["publish", "problems_found", "post"],
    "properties": {
        "publish": {"type": "boolean"},
        "problems_found": {"type": "array", "items": {"type": "string"}},
        "post": POST_SCHEMA,
    },
}

RULES = """\
Hard rules (never break these):
- Only state facts about the dealership that appear in the DEALERSHIP FACTS below.
  Never invent awards, years in business, prices, rates, inventory, staff names or reviews.
- Never invent customers, customer names or quotes. Customer details may only come
  from a CUSTOMER STORY provided to you, and quotes must be copied word for word.
- No specific prices, interest rates, payments or financing promises.
- No putting down other dealerships, brands or people.
- General car advice must be accurate and safe. When something depends on the
  person's situation (credit, insurance, state law), say so.

Style:
- Warm, positive and genuinely helpful. The reader should leave with a solution.
- Plain English at about an 8th-grade reading level. Short paragraphs.
- Write so an AI assistant could quote it: the summary answers the main question
  in 2-3 sentences, each section heading is a clear question or task, and each
  section opens with a direct answer before the details.
- Mention the dealership naturally once or twice (usually near the end), as a
  friendly local option in its service area. No hard selling.
- 900-1400 words across 4-7 sections. 4-6 key takeaways. 4-6 FAQ entries that
  real shoppers would type into a search box or ask an AI assistant.
- slug: lowercase words joined by hyphens, under 70 characters.
"""


def ask_claude(client, system, prompt, schema):
    """Send one request and return the JSON reply as a Python dict."""
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": schema}},
        # If Claude declines a request, retry it automatically on a fallback model.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        sys.exit("Claude declined this request. Try a different topic or story.")
    if response.stop_reason == "max_tokens":
        sys.exit("The reply was cut off before it finished. Try again.")
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)


def pick_story():
    """Return the first inbox story the customer agreed to share, or None."""
    for path in sorted(INBOX.glob("*.md")):
        if path.name in ("README.md", "TEMPLATE.md"):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"^Customer permission:\s*yes\b", text, re.IGNORECASE | re.MULTILINE):
            return path, text
        print(f"Skipping {path.name}: no 'Customer permission: yes' line.")
    return None


def next_topic():
    lines = TOPICS.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.strip() and not line.startswith("#"):
            return line.strip()
    return None


def remove_topic(topic):
    lines = TOPICS.read_text(encoding="utf-8").splitlines()
    lines.remove(topic)
    TOPICS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_slug(slug):
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return slug[:70].rstrip("-") or "post"


def main():
    site = json.loads((BLOG / "site.json").read_text(encoding="utf-8"))
    site.pop("_note", None)

    story = pick_story()
    topic = None if story else next_topic()
    if story:
        print(f"Writing a customer story from {story[0].name}")
        task = (
            "Turn this real customer story into a positive story-and-solution post. "
            "Lead with the problem the customer faced, show how it was solved, then give "
            "readers practical advice for the same situation.\n\n"
            f"CUSTOMER STORY:\n{story[1]}"
        )
    elif topic:
        print(f"Writing a solution post about: {topic}")
        task = (
            "Write a positive, practical solution post on this topic. Don't mention any "
            f"specific customers.\n\nTOPIC: {topic}"
        )
    else:
        print("Nothing to write: inbox/ has no approved stories and topics.txt is empty.")
        return

    facts = f"DEALERSHIP FACTS:\n{json.dumps(site, indent=2)}"
    existing = [json.loads(p.read_text(encoding="utf-8"))["title"] for p in POSTS.glob("*.json")]
    already = "Titles already on the blog (don't repeat them):\n" + "\n".join(existing or ["(none yet)"])

    client = anthropic.Anthropic()

    writer_system = "You write blog posts for a local car dealership's helpful-stories blog.\n\n" + RULES
    draft = ask_claude(client, writer_system, f"{facts}\n\n{already}\n\n{task}", POST_SCHEMA)

    editor_system = (
        "You are the careful editor for a local car dealership's blog. Check the draft "
        "against every rule, fix any problem you find directly in the post, and list each "
        "problem you fixed. Set publish to false only if the post can't be fixed, for "
        "example the source story is too thin or isn't actually positive.\n\n" + RULES
    )
    review = ask_claude(
        client,
        editor_system,
        f"{facts}\n\nTHE ASSIGNMENT THE WRITER GOT:\n{task}\n\n"
        f"DRAFT:\n{json.dumps(draft, indent=2)}",
        REVIEW_SCHEMA,
    )
    for problem in review["problems_found"]:
        print(f"Editor fixed: {problem}")
    if not review["publish"]:
        sys.exit("The editor decided this post shouldn't be published. Nothing was saved.")

    post = review["post"]
    today = datetime.date.today().isoformat()
    post["slug"] = clean_slug(post["slug"])
    used_slugs = {json.loads(p.read_text(encoding="utf-8"))["slug"] for p in POSTS.glob("*.json")}
    base, n = post["slug"], 2
    while post["slug"] in used_slugs:
        post["slug"], n = f"{base}-{n}", n + 1
    post["date"] = today
    post["kind"] = "customer-story" if story else "solution"

    POSTS.mkdir(exist_ok=True)
    out = POSTS / f"{today}-{post['slug']}.json"
    out.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {out.relative_to(BLOG.parent)}")

    if story:
        shutil.move(story[0], INBOX / "used" / story[0].name)
    else:
        remove_topic(topic)


if __name__ == "__main__":
    main()
