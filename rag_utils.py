import os, json, time
import wikipediaapi
import arxiv

CACHE_DIR = os.getenv("CACHE_DIR", "./cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_path(source, key):
    safe = source + "_" + key.replace("/", "_")
    return os.path.join(CACHE_DIR, f"{safe}.json")

def fetch_wikipedia(query, top_k=3):
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)
    text = page.text[:2000]
    path = cache_path("wiki", query)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({"title": page.title, "text": text}, f)
    return text

def fetch_arxiv(query, max_results=3):
    search = arxiv.Search(query=query, max_results=max_results)
    results = []
    for paper in search.results():
        summary = paper.summary
        results.append(summary)
    path = cache_path("arxiv", query)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(results, f)
    return results

def retrieve_context(query):
    ctx = []
    ctx.append(fetch_wikipedia(query))
    ctx.extend(fetch_arxiv(query))
    return "\n\n".join(ctx)
