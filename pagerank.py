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
    result = dict()
    
    #Get the list and number of page's links
    link_pages = corpus[page]
    list_pages = list(corpus.keys())
    number_pages = len(link_pages)
    
    if number_pages == 0:
        #Get total pages in the corpus
                
        probability = 1 / len(list_pages)
        #Create a dictionary with all the pages with the same probability
        for p in list_pages:
            result[p] = probability
    else:
        #Calculate the probability of choosing one of the links using damping factor
        random_prob_links = damping_factor / number_pages
        #Calculate the probability of choosing one of all the pages (including current one) using 1 - damping factor
        random_prob = (1 - damping_factor) / (len(list_pages))
        
        
        #Add the same probability in every page
        for p in list_pages:
            result[p] = random_prob
        
        #Create result dictionary
        for p in link_pages:
            result[p] = result[p] + random_prob_links
            
        
            
    return result
        
    
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    #Get a list with all the pages in the corpus
    list_pages = list(corpus.keys())
    
    #Add the pages in the dictionary and initialize the samples in 0
    for s in list_pages:
        result[s] = 0
    
    #Get the first page randomly
    page_one = random.choice(list_pages)
    
    #Increment the samples of the first page
    result[page_one] = result[page_one] + 1
    
    current_page = page_one
    
    #Get samples using transition model
    for i in range(n):
        transition_list = transition_model(corpus, current_page, damping_factor)
        #Get new sample using transition model
        list_keys = list(transition_list.keys())
        list_values = list(transition_list.values())
        current_page = random.choices(list_keys, list_values,k=1)[0]
        #Increment sample for the page 
        result[current_page] = result[current_page] + 1
    
    #Normalize the samples to probabilities which sum up 1
    for page in list(result.keys()):
        result[page] = result[page] / n
        
    return result

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    
    #Get a list with all the pages in the corpus
    list_pages = list(corpus.keys())
    list_linked_pages = list(corpus.values())
    N = len(list_pages)
    #Add pages to the dictionary and add 1 / N as probability, N as the number of pages in the corpus
    for p in list_pages:
        result[p] = 1 / N        
    
    stop = False
    iterations = 0
    #Start iteration
    while (not stop):
        iterations = iterations + 1
        #Create an initial copy of PR
        PR = result.copy()
        #Calculate PR based on the PageRank formula
        for page in list_pages:
            old_PR = PR[page]
            sumatory = 0
            linking_pages = list()
            #Find linking pages to "page"
            for p in enumerate(list_linked_pages):
                if page in p[1]:
                    linking_pages.append(list_pages[p[0]])
                elif len(p[1]) == 0:
                    sumatory = sumatory + PR[list_pages[p[0]]] / N
                    
            for i in linking_pages:
                if len(corpus[i]) > 0:
                    sumatory = sumatory + PR[i] / len(corpus[i])
                else:
                    sumatory = sumatory + PR[i] / N
            New_PR = ((1 - damping_factor) / N) + (damping_factor * sumatory)
             
            result[page] = New_PR
            
            if abs(New_PR - old_PR) > 0.001:
                stop = False
            else:
                stop = True
        
    return result    
        
    raise NotImplementedError


if __name__ == "__main__":
    main()
