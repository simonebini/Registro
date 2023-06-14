import json
import tkinter as tk
from tkinter import messagebox

def salva_registro(registro):
    try:
        with open("registro.json", "w") as file:
            json.dump(registro, file)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il salvataggio del registro: {str(e)}")

def carica_registro():
    try:
        with open("registro.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il caricamento del registro: {str(e)}")
        return {}


def calcola_media(voti, pesantezza):
    if len(voti) == 0:
        return 0
    somma_pesata = sum([voto * peso / 100 for voto, peso in voti])
    somma_pesantezze = sum([peso / 100 for _, peso in voti])
    media = somma_pesata / somma_pesantezze
    return round(media, 2)

def visualizza_registro(registro, pesantezze):
    registro_text.delete("1.0", tk.END)
    registro_text.insert(tk.END, "Registro delle valutazioni:\n\n")
    for materia, voti in registro.items():
        voto_str = ', '.join([str(voto) for voto, _ in voti])
        media = calcola_media(voti, pesantezze.get(materia, 100))
        registro_text.insert(tk.END, f"{materia}:\nVoti: {voto_str}\nMedia: {media:.2f}\n\n")


def inserisci_valutazione(event=None):
    materia = materia_var.get().lower()
    voto = voto_entry.get()
    pesantezza = pesantezza_var.get()
    voto_entry.delete(0, tk.END)

    if materia != "":
        if materia in materie_possibili:
            if voto != "":
                try:
                    voto = float(voto)
                except ValueError:
                    messagebox.showerror("Errore", "Inserisci un voto valido.")
                    return

                if materia in registro:
                    registro[materia].append((voto, pesantezza))
                else:
                    registro[materia] = [(voto, pesantezza)]

                # Aggiornamento pesantezze
                pesantezze[materia] = pesantezza

                salva_registro(registro)
                messagebox.showinfo("Successo", "Valutazione salvata correttamente.")
            else:
                messagebox.showerror("Errore", "Inserisci un voto valido.")
        else:
            messagebox.showerror("Errore", "Materia non valida. Riprova.")

        visualizza_registro(registro, pesantezze)
    else:
        messagebox.showerror("Errore", "Seleziona una materia.")


materie_possibili = ["educazione civica", "informatica", "italiano", "matematica", "inglese", "economia", "motoria", "sistemi", "storia", "tepsit", "tele"]
pesantezze = {}

registro = carica_registro()

root = tk.Tk()
root.title("Programma di Valutazione")
root.geometry("800x900")
root.resizable(False, False)

materia_label = tk.Label(root, text="Materia:")
materia_label.pack()

materia_var = tk.StringVar(root)
materia_var.set("")  # Inizialmente nessuna materia selezionata

materia_menu = tk.OptionMenu(root, materia_var, *materie_possibili)
materia_menu.pack()

pesantezza_label = tk.Label(root, text="Pesantezza (%):")
pesantezza_label.pack()

pesantezza_var = tk.IntVar(root)
pesantezza_var.set(100)  # Inizialmente pesantezza al 100%

pesantezza_menu = tk.OptionMenu(root, pesantezza_var, 20, 50, 100)
pesantezza_menu.pack()

voto_label = tk.Label(root, text="Valutazione:")
voto_label.pack()

voto_entry = tk.Entry(root)
voto_entry.pack()
voto_entry.bind("<Return>", inserisci_valutazione)  # Collegamento dell'azione alla pressione del tasto "Return"

inserisci_button = tk.Button(root, text="Inserisci Valutazione", command=inserisci_valutazione)
inserisci_button.pack()

registro_text = tk.Text(root, height=47, width=80)
registro_text.pack()


visualizza_registro(registro, pesantezze)

root.mainloop()
