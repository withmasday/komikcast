import requests, re, os
from bs4 import BeautifulSoup

BASE_URL = 'https://komikcast.lol/daftar-komik/?status=&type=&orderby=popular'

def get_spesific_content(link, dirCreate):
    try:
        response = requests.get(link, timeout=15).text
        soup = BeautifulSoup(response, 'html.parser')
        chapters = soup.find_all('a', class_='chapter-link-item')
        for chapter in chapters:
            chapterTitle = chapter.get_text(strip=True)
            chapterTitle = re.sub(r'[\n\s]+', '', chapterTitle)
            chapterLink = chapter.get('href')
            
            chapterPath = dirCreate + '/' + chapterTitle
            if not os.path.exists(chapterPath):
                os.makedirs(chapterPath)
                
                get = requests.get(chapterLink, timeout=15).text
                context = BeautifulSoup(get, 'html.parser')
                images = context.find_all('img', class_='alignnone size-full wp-image-72251')
                loop = 1
                for image in images:
                    image = image.get('src')
                    download = requests.get(image, timeout=15)
                    if download.status_code == 200:
                        filepath = chapterPath + '/'+ str(loop) + '.jpg'
                        print (filepath)
                        with open(filepath, 'wb') as f:
                            f.write(download.content)
                    else:
                        print(f"Failed to download image: {image}")
                    
                    loop = loop + 1
                    
            else:pass
            
    except:
        print ('[!] Something wrong.')
    
def get_url_list(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        images = soup.find_all('img', class_='ts-post-image wp-post-image attachment-medium size-medium')
        titles = soup.find_all('h3', class_='title')
        links = soup.find_all('a', class_='data-tooltip')
        
        print (len(titles))
        print (len(images))
        print (len(links))
        
        for title, image, link in zip(titles, images, links):
            title = title.get_text(strip=True)
            image = image.get('src')
            link = link.get('href')
            
            titleComic = title.replace(' ', '_')
            dirCreate = './downloads/'+ titleComic
            if not os.path.exists(dirCreate):
                os.makedirs(dirCreate)
            else:pass
            
            download = requests.get(image, timeout=15)
            if download.status_code == 200:
                extension = image.split('.')[2]
                filepath = dirCreate +'/'+ 'banner.'+ extension
                with open(filepath, 'wb') as f:
                    f.write(download.content)
            else:
                print(f"Failed to download image: {image}")
            
            get_spesific_content(link, dirCreate)
    except:
        print ('[!] Something wrong.')
        
    
    
check = requests.get(BASE_URL, timeout=15).text
get_url_list(check)