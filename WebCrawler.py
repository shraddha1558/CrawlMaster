import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import threading
import queue
import sys
import time

linksVisited = set()

class workerThreads(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            try:
                site = urllib.request.urlopen(url)
                siteContent = site.read()

                for links in BeautifulSoup(siteContent, 'html.parser').find_all('a'):
                    if links.has_attr('href'):
                        linkUrl = links['href']

                        if not linkUrl.startswith('http'):
                            linkUrl = target + linkUrl

                        if not linkUrl.startswith(target):
                            continue

                        if linkUrl not in linksVisited:
                            linksVisited.add(linkUrl)
                            self.queue.put(linkUrl)
                            print(linkUrl)

            except urllib.error.HTTPError:
                continue
            except:
                continue
            finally:
                # Adding a delay to avoid overloading the server
                time.sleep(1)  # Adjust time delay as needed
            self.queue.task_done()

queue = queue.Queue()

if len(sys.argv) < 2:
    print("Please pass a target url in the format https://www.example.com")
    exit(0)

target = sys.argv[1]
linksVisited.add(target)
linksVisited.add(target + '#')

allThreads = []
for i in range(10):
    threadInstance = workerThreads(queue)
    threadInstance.daemon = True
    threadInstance.start()
    allThreads.append(threadInstance)

queue.put(target)

for j in allThreads:
    j.join()

queue.join()

print("Crawling completed")
