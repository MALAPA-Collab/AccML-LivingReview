from datetime import datetime
from urllib.parse import quote

import feedparser
import pandas as pd
import requests

# --------------- CONFIG ------------------

CATEGORY = "physics.acc-ph"
KEYWORDS = [
    "machine learning",
    "deep learning",
    "reinforcement learning",
    "bayesian optimization",
    "anomaly detection",
    "active learning",
    "transfer learning",
    "semi-supervised learning",
    "unsupervised learning",
    "supervised learning",
    "meta learning",
    "self supervised learning",
    "online learning",
    "offline learning",
    "graph neural networks",
    "neural architecture",
    "hyperparameter optimization",
    "surrogate model",
    "model-based optimization",
    "model-free optimization",
    "evolutionary algorithms",
    "genetic algorithms",
    "particle swarm optimization",
    "simulated annealing",
    "gradient descent",
]  # in title or abstract, case-insensitive
START_DATE = None
END_DATE = None
MAX_RESULTS = 3000  # total papers to fetch from arXiv (max: 30000)


def parse_arxiv(
    category, keywords=None, start_date=None, end_date=None, max_results=100
):
    """
    Fetches papers from arXiv based on category and keywords.
    More info on the syntax of the query can be found here: https://info.arxiv.org/help/api/user-manual.html#Examples
    """
    base_url = "http://export.arxiv.org/api/query?"
    if keywords is None and start_date is None and end_date is None:
        query = f"cat:{category}"
    elif keywords is not None and start_date is None and end_date is None:
        if len(keywords) == 1:
            keywords[0] = keywords[0].replace(" ", "+")
            query = f"cat:{category}+AND+ti:%22{keywords[0]}%22"
        else:
            query = f"cat:{category}+AND+%28"
            for word in keywords:
                word = word.replace(" ", "+")
                if query.endswith("%28"):
                    query += f"ti:%22{word}%22"
                else:
                    query += f"+OR+ti:%22{word}%22"
            query += "%29"
    url = f"{base_url}search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    feed = feedparser.parse(url)
    entries = feed.entries
    papers = []
    for entry in entries:
        # print(entry.get("title"))
        if "title" not in entry or "summary" not in entry:
            print("Skipping entry without title or summary:", entry)
            continue
        title = entry.get("title").strip().replace("\n", "").replace("  ", " ")
        if not title:
            print("Skipping entry without title:", entry)
            continue

        abstract = entry.get("summary", "").strip().replace("\n", " ")
        if not abstract:
            print("Skipping entry without abstract:", entry)
            continue
        authors = entry.get("authors", [])
        if not authors:
            print("Skipping entry without authors:", entry)
            continue
        authors = ", ".join(author.name for author in authors)
        link = entry.get("id", None)
        updated = entry.updated[:10]
        published = entry.get("published", updated)[:10]
        year = published[:4]
        arxiv_id = entry.id.split("/abs/")[-1]
        # print("")
        # print(title)
        # print(authors)
        # print(link, year, arxiv_id)
        # print(type(year))
        # print("")
        papers.append([year, title, authors, link])
    return papers


papers = parse_arxiv(
    CATEGORY,
    KEYWORDS,
    START_DATE,
    END_DATE,
    MAX_RESULTS,
)

print("Type of papers:", type(papers))
print("Length of papers:", len(papers))
print("First paper:", papers[0] if papers else "No entries")

df = pd.DataFrame(papers, columns=["year", "title", "authors", "link"])
df.to_csv("arxiv_papers.csv", index=False)
df.to_markdown("README.md", index=False)


# Read the existing content
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Define your header or intro text
header = "# AccML-LivingReview\n\n"
header += "In the same spirit as the [HEP Living Review](https://github.com/iml-wg/HEPML-LivingReview/), the accelerator physics community needs to accurately track the ML contributions to the field.\n\n"

# Write it all back: header + original content
with open("README.md", "w", encoding="utf-8") as f:
    f.write(header + content)
