import feedparser
import pathlib
import re

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def get_blog_entries():
    entries = feedparser.parse("https://dan.makovec.net/feed/")["entries"]
    
    return [
            {
                "title": entry["title"],
                "url": entry["link"].split("#")[0],
                "published": entry["published"],
            }
            for entry in entries
        ]

if __name__ == "__main__":

    # Get the last 5 blog entries
    root = pathlib.Path(__file__).parent.resolve()
    readme = root / "README.md"
    readme_contents = readme.open().read()

    entries = get_blog_entries()[:5]
    entries_md = "\n".join(
            ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
        )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    readme.open("w").write(rewritten)