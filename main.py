import collections
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def is_valid(word):  #fonction utiliser pour valider les mots traité
    if "[" in word or "]" in word:
        return False
    return True


def extract_lyrics(url):  #extraire les lyrics d'un url
    print(f"Fetching lyrics... {url}")
    r = requests.get(url)
    if r.status_code != 200:
        print('page impossible a recuperer')

    # recup l'html complet du site source
    soup = BeautifulSoup(r.content, "html.parser")
    #recup les div avec le text du chanteur
    lyrics_all = soup.find_all('div', class_="jYfhrf")
    # if not lyrics:      #recursivité si la on ne recup rien, on relance la fonction
    #     return extract_lyrics(url)

    all_words = []
    for i in lyrics_all:   # comme il ya plusieurs div on boucle sur les div et à chaque boucle on fait une autre boucle
          for sentence in i.stripped_strings:   #qui recupere chaque phrase(chaine de cara) sans les balises parasites (br, p, etc )
            # all_words.extend(sentence.split() )      #et on extends tous ca en splitant à chauqe fois par un espace pour avoir uniquement que des mots distingué
            sentence_words = [word.strip(",").strip(".").lower() for word in sentence.split() if is_valid(word)]   
            all_words.extend(sentence_words)
    return all_words


def get_all_urls():   #chopper tous les url
    number_page = 1
    links = []
    while True: 
        r = requests.get(f"https://genius.com/api/artists/1282/songs?page={number_page}&sort=popularity")   #recuperer toutes les données via l'api
        # si le code status est 200 (success) on continue le code
        if r.status_code == 200:
            print(f"Fetching page {number_page}")
            # dans le fichier on récuperer un dict response avec toutes les infos de la musiques + le next page afin de continuer la boucle
            response = r.json().get('response')
            next_page = response.get('next_page')
            number_page += 1

            # dans la response on recupere toutes url de musiques uniquement en forme d'objet
            songs = response.get('songs')
            # for song in songs: 
            #     links.append(song.get('url'))
            links.extend([song.get('url') for song in songs])  #boucle qui va extend tout les url dans un tableau

            if not next_page:
                print('No more pages to fetch')
                break
    return links


def get_all_words():   #scrip qui lance la logique
    # urls = get_all_urls()
    # words = []
    # for url in urls:
    #     lyrics = extract_lyrics(url=url)
    #     words.extend(lyrics)

    # # Logique pour ecrire dans un fichier json
    # with open("data.json", "w", encoding="utf-8") as f:
    #     json.dump(words, f, indent=4)

        #code ci dessous pour lire un fichié enregistré 
    with open("damso.json", "r") as f:
        words = json.load(f)

    counter = collections.Counter([w for w in words if len(w) > 5])
    most_words = counter.most_common(10)
    print(most_words)


get_all_words()