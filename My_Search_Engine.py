import urllib2

proxy_support = urllib2.ProxyHandler({"http":"Your Proxy URL"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

def union(p,q):

    for e in q:
        if e not in p:
            p.append(e)
    

def get_next_target(page):

    start_link = page.find('<a href=')

    if start_link == -1:
        return None,0
    
    start_quote = page.find('"',start_link)
    end_quote= page.find('"',start_quote+1)

    url=page[start_quote+1:end_quote]

    return url,end_quote
    


def print_all_links(page):

    while True:
        url,end_pos =get_next_target(page)

        if url:
            print url
            page=page[end_pos:]
        else:
            break


def get_all_links(page):

    links=[]
    while True:
        url , end_pos =get_next_target(page)

        if url:            
            links.append(url)
            page=page[end_pos:]
        else:
            return links


def add_to_index(index,keyword,url):

    if keyword in index:
        index[keyword].append(url)
           
    else:
        index[keyword]=[url]


def look_up(index,keyword):

    if entry in index:
        return index[keyword]
    
    else:        
        return None



def add_page_to_index(index,url,content):

    words= content.split()

    for word in words:
        add_to_index(index,word,url)


    
def crawl_web(seed):

    tocrawl=[seed]
    crawled=[]
    index={}
    graph={}
    while tocrawl:
        page=tocrawl.pop()
       
        if page not in crawled:
            content=get_page(page)
            #add_page_to_index(index,page,content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl,outlinks)
            crawled.append(page)

    #return crawled       
    return index ,graph



def compute_ranks(graph):

    d = 0.8 #damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0/npages

    for i in range(0,numloops):
        newranks = {}

        for page in graph:
            newrank =  (1-d)/npages

            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d*(ranks[node]/len(graph[node]))

            newranks[page] = newrank

        rank = newranks

    return ranks
                    

           


    
#print crawl_web("http://www.iitg.ernet.in")
#index,graph = crawl_web("http://www.iitg.ernet.in")
index,graph = crawl_web("http://www.udacity.com/urank/index.html")
print compute_ranks(graph)
#print compute_ranks(graph)

#print crawl_web("http://www.iitg.ernet.in")




