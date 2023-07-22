import requests
import lxml.html


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def search_movies(title):
    url = 'https://nerdfilmes.com.br/?s=' + title.strip().replace(' ', '+')
    var = requests.get(url, headers=headers)
    parser =  lxml.html.fromstring(var.text)

    movie_titles = parser.cssselect('[class="elementor-post__title"]')
    movie_titles = [x.text_content().strip() for x in movie_titles]

    movie_links = parser.cssselect('[class="elementor-post__thumbnail__link"]')
    movie_links = [x.attrib['href'] for x in movie_links]

    posters = parser.cssselect('[class="elementor-post__thumbnail"] img')
    posters = [x.attrib['src'] for x in posters]

    all_movies = []

    for x in range(0, len(posters)):
        all_movies.append({
            'title': movie_titles[x],
            'link': movie_links[x],
            'poster': posters[x]
        })
    
    return all_movies


def createHTML(title):
    all_movies = search_movies(title)
    
    html = ''

    for movie in all_movies:
        html += f"""<div class="movie"><a class="links" href="{movie['link']}"><img class="poster-img" min-width="342" src="{movie['poster']}"></a><p class="title">"{movie['title']}</p></div>"""
        
    return html


def getLink(url):
    var = requests.get(url, headers=headers)
    parser =  lxml.html.fromstring(var.text)
    magneticLink = parser.cssselect('[class="botao"]')[0].attrib['href']
    
    return magneticLink