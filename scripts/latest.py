"""Write the 5 newest Models to Margins deep dives into README.md between LATEST markers."""
import json, re, urllib.request

API = "https://api.github.com/repos/vinayagrw/models-to-margins/contents/src/content/deep-dives"
SITE = "https://models-to-margins.vinayagrw.workers.dev/deep-dives/"


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-feed",
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


items = []
for f in json.loads(get(API)):
    if not f["name"].endswith(".md"):
        continue
    text = get(f["url"], raw=True)
    fm = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not fm:
        continue
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", fm.group(1), re.M))
    if meta.get("listed", "true").strip() == "false":
        continue
    items.append((meta.get("pubDate", "").strip(), meta.get("title", "").strip().strip('"'), f["name"][:-3]))

items.sort(reverse=True)
lines = [f"- `{d}` [{t}]({SITE}{slug}/)" for d, t, slug in items[:5]]
readme = open("README.md").read()
new = re.sub(r"(<!-- LATEST:START -->).*?(<!-- LATEST:END -->)",
             lambda m: m.group(1) + "\n" + "\n".join(lines) + "\n" + m.group(2), readme, flags=re.S)
open("README.md", "w").write(new)
print("\n".join(lines))
