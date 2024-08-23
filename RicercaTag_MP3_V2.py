# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 16:45:00 2024

@author: MadCat
"""

import os
from mutagen.easyid3 import EasyID3
import musicbrainzngs as mb

mb.set_useragent("MP3TagUpdater", "1.0", "your-email@example.com")

def search_musicbrainz(artist, title):
    try:
        result = mb.search_recordings(artist=artist, recording=title, limit=5)

        if result['recording-list']:
            for recording in result['recording-list']:
                if 'release-list' in recording:
                    for release in recording['release-list']:
                        # Ritorna i tag del primo risultato trovato
                        album = release['title']
                        release_date = release['date'][:4] if 'date' in release else None  # Prendi solo l'anno
                        release_artist = recording['artist-credit'][0]['artist']['name']
                        return release_artist, title, album, release_date
        return None, None, None, None
    except Exception as e:
        print(f"Errore durante la ricerca su MusicBrainz: {e}")
        return None, None, None, None

def get_existing_tags(file_path):
    try:
        audio = EasyID3(file_path)
        artist = audio.get('artist', [None])[0]
        title = audio.get('title', [None])[0]
        album = audio.get('album', [None])[0]
        year = audio.get('date', [None])[0]
        return artist, title, album, year
    except Exception as e:
        print(f"Errore nel leggere i tag ID3: {e}")
        return None, None, None, None

def update_id3_tag(file_path, artist, title, album, year):
    try:
        audio = EasyID3(file_path)
        audio['artist'] = artist
        audio['title'] = title
        audio['album'] = album
        audio['date'] = year
        audio.save()
        print(f"ID3 tag aggiornato per: {file_path}")
    except Exception as e:
        print(f"Errore nell'aggiornare i tag ID3: {e}")

def main():
    root_folder = r"C:\MP3\A"  
    for root, dirs, files in os.walk(root_folder):
        print(" ")
        print("partenza------>")
        print(f"root: {root}")
        for file in files:
            if file.endswith(".mp3"):
                print(f"file: {file}")
                try:
                   
                    artist, title = file.rsplit(" - ", 1)
                    title = title.replace(".mp3", "")
                    
                    existing_artist, existing_title, existing_album, existing_year = get_existing_tags(os.path.join(root, file))
                    print(f"Tag esistenti - Artista: {existing_artist}, Titolo: {existing_title}, Album: {existing_album}, Anno: {existing_year}")
                    
                    correct_artist, correct_title, correct_album, correct_year = search_musicbrainz(artist, title)
                    
                    if all([correct_artist, correct_title, correct_album, correct_year]):
                        print(f"Tag trovati su MusicBrainz - Artista: {correct_artist}, Titolo: {correct_title}, Album: {correct_album}, Anno: {correct_year}")
                        
                        changes = []
                        if existing_artist != correct_artist:
                            changes.append(f"Artista: {existing_artist} -> {correct_artist}")
                        if existing_title != correct_title:
                            changes.append(f"Titolo: {existing_title} -> {correct_title}")
                        if existing_album != correct_album:
                            changes.append(f"Album: {existing_album} -> {correct_album}")
                        if existing_year != correct_year:
                            changes.append(f"Anno: {existing_year} -> {correct_year}")
                        
                        if changes:
                            print("\nDifferenze riscontrate:")
                            for change in changes:
                                print(change)
                            confirm = input("Vuoi aggiornare i tag ID3? (y/n): ")
                            if confirm.lower() == "y":
                                update_id3_tag(os.path.join(root, file), correct_artist, correct_title, correct_album, correct_year)
                            else:
                                print("Operazione annullata.")
                        else:
                            print(f"I tag ID3 sono già corretti per {artist} - {title}.")
                    else:
                        print(f"Informazioni non trovate o incomplete per {artist} - {title}.")
                except ValueError:
                    print(f"Nome file non valido: {file}. Assicurati che sia nel formato 'Artista - Titolo.mp3'.")

if __name__ == "__main__":
    main()
y