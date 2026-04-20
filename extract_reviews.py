import json
import sys

def get_val(obj, *keys):
    for k in keys:
        if isinstance(obj, dict):
            obj = obj.get(k)
        else:
            return None
    return obj

all_reviews = []

for fname in ['reviews_page1.json', 'reviews_page2.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Try to find the list of reviews
    reviews = []
    if isinstance(data, list):
        reviews = data
    elif isinstance(data, dict):
        # common structures: data['reviews'], data['data'], data['items'], data['result']
        for key in ['reviews', 'data', 'items', 'result', 'list', 'contents', 'reviewList']:
            if key in data:
                val = data[key]
                if isinstance(val, list):
                    reviews = val
                    break
                elif isinstance(val, dict):
                    for k2 in ['reviews', 'data', 'items', 'list', 'contents', 'reviewList']:
                        if k2 in val and isinstance(val[k2], list):
                            reviews = val[k2]
                            break
                if reviews:
                    break
        if not reviews:
            # Print top-level keys for debugging
            print(f"DEBUG {fname} keys: {list(data.keys())}", file=sys.stderr)
            # Try any list value
            for k, v in data.items():
                if isinstance(v, list) and v:
                    reviews = v
                    print(f"Using key: {k}", file=sys.stderr)
                    break

    print(f"{fname}: found {len(reviews)} reviews", file=sys.stderr)
    if reviews:
        print(f"First review keys: {list(reviews[0].keys()) if isinstance(reviews[0], dict) else type(reviews[0])}", file=sys.stderr)
    all_reviews.extend(reviews)

# Sort by id descending
def get_id(r):
    return r.get('id', 0) if isinstance(r, dict) else 0

all_reviews.sort(key=get_id, reverse=True)

def esc(s):
    if s is None:
        return ''
    return str(s).replace('\\', '\\\\').replace("'", "\\'")

lines = []
for r in all_reviews:
    rid = r.get('id', '')
    writer = esc(r.get('writer', ''))
    title = esc(r.get('title', ''))
    desc = esc(r.get('seoDescription', ''))
    created = str(r.get('createdDate', ''))[:10]
    thumb = r.get('thumbnailImage', None)
    img = ''
    if isinstance(thumb, dict):
        img = esc(thumb.get('url', ''))
    elif isinstance(thumb, str):
        img = esc(thumb)
    lines.append(f"  {{id:{rid},w:'{writer}',t:'{title}',d:'{desc}',date:'{created}',img:'{img}'}}")

print("var REVIEWS = [")
print(",\n".join(lines))
print("];")
print(f"// Total: {len(all_reviews)} reviews", file=sys.stderr)
