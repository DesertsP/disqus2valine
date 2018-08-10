import xml.etree.ElementTree as ET
import re
# import bs4


def get_all_posts(root):
    return root.findall('./{http://disqus.com}post')


def get_thread_link(root, thread_id):
    links = root.findall('.//*[@{http://disqus.com/disqus-internals}id="'
                         + thread_id + '"]/{http://disqus.com}link')
    if len(links) > 0:
        return links[0].text


def trim_link(link):
    results = re.findall('''http.*://.+?(/.+)''', link)
    if len(results) > 0:
        return results[0]


def get_post_author(root, post_id):
    results = root.findall('{http://disqus.com}post[@{http://disqus.com/disqus-internals}id="' + post_id + '"]')
    if len(results) > 0:
        return results[0].find('{http://disqus.com}author').find('{http://disqus.com}name').text


def parse_post(root, post_node):
    message = post_node.find('{http://disqus.com}message').text
    results = re.findall('<!\[CDATA\[(.*)\]\]>', message)
    if len(results) > 0:
        message = results[0]
    # print(message)
    # message = bs4.BeautifulSoup(message, 'html.parser').text
    author_node = post_node.find('{http://disqus.com}author')
    email = author_node.find('{http://disqus.com}email').text
    name = author_node.find('{http://disqus.com}name').text
    created_at = post_node.find('{http://disqus.com}createdAt').text
    thread_id = post_node.find('{http://disqus.com}thread')\
                         .get('{http://disqus.com/disqus-internals}id')
    thread_url = trim_link(get_thread_link(root, thread_id))
    parent = post_node.find('{http://disqus.com}parent')
    if parent is None:
        parent_post_author = ''
    else:
        parent_post_author = \
            get_post_author(root,
                                  parent.get('{http://disqus.com/disqus-internals}id'))
        message = '<a class="at" href="#">@' + parent_post_author + '</a> ' + message;
    print(message)
    return {
        'message': message,
        'email': email,
        'name': name,
        'thread_url': thread_url,
        'parent_post_author': parent_post_author,
        'created_at': created_at
    }


def parse_all_posts(file_path):
    tree = ET.ElementTree(file=file_path)
    root = tree.getroot()
    return [parse_post(root, post) for post in get_all_posts(root)]
