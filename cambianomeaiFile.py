import os

def rimuovi_parte_nome(cartella, parte_da_rimuovere):
    if not os.path.isdir(cartella):
        print("La cartella specificata non esiste.")
        return
    
    for file in os.listdir(cartella):
        if file.endswith(".mp3"):  # Assicurati che siano file MP3
            nuovo_nome = file.replace(parte_da_rimuovere, "")  # Rimuovi la parte specificata dal nome
            vecchio_percorso = os.path.join(cartella, file)
            nuovo_percorso = os.path.join(cartella, nuovo_nome)
            
            try:
                os.rename(vecchio_percorso, nuovo_percorso)
                print(f"File rinominato: {file} -> {nuovo_nome}")
            except Exception as e:
                print(f"Errore durante la rinomina del file {file}: {e}")


cartella_input = r"C:\Users\Downloads\Filedarinominare\"
parte_da_rimuovere = "Partedacancellare "

rimuovi_parte_nome(cartella_input, parte_da_rimuovere)
