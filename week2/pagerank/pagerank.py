import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    pr = dict()

    # Determine probability for each page if chosing randomly from all pages in the corpus
    for key in corpus:
        pr[key] = (1 - damping_factor) / len(corpus)
    
    # If page has no outgoing links
    if len(corpus[page]) == 0:
        for key in pr:
            pr[key] += damping_factor / len(corpus)
        return (pr)
    
    # Add to the probabilitys the chance of chosing a link in the current page
    for pag in corpus[page]:
        pr[pag] += damping_factor / len(corpus[page])
    
    return pr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Amount of times surfer as visited each page
    pageranks = dict()
    for key in corpus:
        pageranks[key] = 0
    # Choose first random page
    current_page = random.choice(list(corpus))
    pageranks[current_page] += 1
    tm = transition_model(corpus, current_page, damping_factor)
    for i in range(n - 1):
        pages = list(tm)
        wts = list()
        for p in pages:
            wts.append(tm[p])
        wts = tuple(wts)
        current_page = random.choices(pages, weights=wts, k=1)
        pageranks[current_page[0]] += 1
        tm = transition_model(corpus, current_page[0], damping_factor)
    s = sum(pageranks.values())
    for key in pageranks:
        pageranks[key] = pageranks[key] / s
    return pageranks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = dict()
    diff = 1
    check = 0
    for key in corpus:
        pageranks[key] = 1 / len(corpus)
    while (diff > 0.001):
        copy = pageranks.copy()
        for key in corpus:
            pageranks[key] = (1 - damping_factor) / len(corpus)
            for page in corpus:
                if key in corpus[page]:
                    check = 1
                    pageranks[key] += (pageranks[page] / len(corpus[page])) * damping_factor
            if check == 0:
                pageranks[key] = 1 / len(corpus)
            check = 0
        x = random.choice(list(pageranks))
        diff = abs(pageranks[x] - copy[x])
        for key in pageranks:
            if abs(pageranks[key] - copy[key]) > diff:
                diff = abs(pageranks[key] - copy[key])

    return pageranks


if __name__ == "__main__":
    main()
