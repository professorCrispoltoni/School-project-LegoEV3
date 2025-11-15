import tkinter as tk
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    tk.messagebox.showerror("Errore", "La libreria Pillow non è installata. Installala eseguendo 'pip install pillow'.")
    raise
import socket
import threading

# Definizione dei colori del tema Campus Da Vinci
COLORI_TEMA = {
    'blu_campus': "#1a3c6e",      # Blu scuro del logo
    'azzurro': "#3c78d8",         # Azzurro più chiaro
    'grigio_chiaro': "#f0f0f0",   # Sfondo chiaro
    'bianco': "#ffffff",          # Bianco
    'grigio_testo': "#2c3e50"     # Colore testo
}

class AppOpenDay:
    def __init__(self, root):
        # Inizializzazione della finestra principale
        self.root = root
        self.root.title("IIS Campus Da Vinci")
        self.root.geometry("400x600")
        self.root.configure(bg=COLORI_TEMA['grigio_chiaro'])
        
        # Stile base per le etichette
        self.style_label = {
            'bg': COLORI_TEMA['grigio_chiaro'],
            'fg': COLORI_TEMA['grigio_testo'],
            'font': ('Helvetica', 12)
        }
        
        # Definizione colori rilevabili
        self.colori = {
            'ROSSO':  "#E63946",  # Rosso elegante
            'BLU':    "#1a3c6e",  # Blu del campus 
            'NERO':   "#2C3E50",  # Nero elegante
            'VERDE':  "#2ECC71",  # Verde soft
            'GIALLO': "#F1C40F",  # Giallo soft
            'BIANCO': "#ECF0F1"   # Bianco soft
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        # Creazione del frame principale
        main_frame = tk.Frame(self.root, bg=COLORI_TEMA['grigio_chiaro'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Caricamento logo
        self.setup_logo(main_frame)
        
        # Setup display colore
        self.setup_color_display(main_frame)
        
        # Setup status e connessione
        self.setup_connection_controls(main_frame)
    
    def setup_logo(self, main_frame):
        # Carica il logo se disponibile, altrimenti mostra il titolo
        try:
            pil_image = Image.open("logo_campus.png")
            pil_image = pil_image.resize((300, 150))
            self.logo_image = ImageTk.PhotoImage(pil_image)
            tk.Label(main_frame, image=self.logo_image, 
                    bg=COLORI_TEMA['grigio_chiaro']).pack(pady=15)
        except:
            tk.Label(main_frame, text="IIS Campus Leonardo da Vinci",
                    font=('Helvetica', 22, 'bold'),
                    fg=COLORI_TEMA['blu_campus'],
                    bg=COLORI_TEMA['grigio_chiaro']).pack(pady=15)
    
    def setup_color_display(self, main_frame):
        # Container per il display colore
        display_container = tk.Frame(main_frame, 
            bg=COLORI_TEMA['grigio_chiaro'],
            pady=20)
        display_container.pack(fill='x')
        
        # Sottotitolo con stile migliorato
        tk.Label(display_container,
            text="Sistema di Rilevamento Colori",
            font=('Helvetica', 16, 'bold'),
            fg=COLORI_TEMA['blu_campus'],
            bg=COLORI_TEMA['grigio_chiaro']).pack()
        
        # Separatore decorativo
        separator = tk.Frame(display_container,
            height=2,
            width=100,
            bg=COLORI_TEMA['azzurro'])
        separator.pack(pady=10)
        
        # Display colore con bordo e ombra
        color_container = tk.Frame(display_container,
            bg=COLORI_TEMA['blu_campus'],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORI_TEMA['azzurro'])
        color_container.pack(pady=20)
        
        self.color_display = tk.Frame(color_container,
            width=200,
            height=200,
            bg="gray")
        self.color_display.pack(padx=2, pady=2)
        self.color_display.pack_propagate(False)
    
    def setup_connection_controls(self, main_frame):
        # Container centrale per allineare tutto
        center_frame = tk.Frame(main_frame, bg=COLORI_TEMA['grigio_chiaro'])
        center_frame.pack(expand=True)
        
        # Status label con stile migliorato e bordo sottile
        status_frame = tk.Frame(center_frame, 
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=1)
        status_frame.pack(pady=(15,5))
        
        self.status_label = tk.Label(status_frame, 
            text="In attesa della connessione...",
            font=('Helvetica', 12, 'italic'),
            fg=COLORI_TEMA['grigio_testo'],
            bg=COLORI_TEMA['bianco'],
            pady=8,
            padx=20)
        self.status_label.pack()
        
        # Box IP
        ip_container = tk.Frame(center_frame, 
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=1)
        ip_container.pack(pady=10)
        
        # Label IP centrata
        tk.Label(ip_container, 
            text="Indirizzo IP Robot",
            font=('Helvetica', 12, 'bold'),
            bg=COLORI_TEMA['bianco'],
            fg=COLORI_TEMA['blu_campus'],
            padx=20).pack(pady=(10,5))
        
        # Entry IP con stile moderno
        self.ip_entry = tk.Entry(ip_container,
            width=20,  # Ridotto per essere più compatto
            font=('Helvetica', 11),
            bg=COLORI_TEMA['grigio_chiaro'],
            fg=COLORI_TEMA['grigio_testo'],
            relief='flat',
            justify='center',
            insertbackground=COLORI_TEMA['blu_campus'])
        self.ip_entry.insert(0, "169.254.215.169")
        self.ip_entry.pack(pady=(0,10), ipady=5, padx=20)
        
        # Box Controlli
        control_container = tk.Frame(center_frame, 
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=1)
        control_container.pack(pady=(15,10))
        
        # Frame per i pulsanti centrato
        btn_frame = tk.Frame(control_container, bg=COLORI_TEMA['bianco'])
        btn_frame.pack(pady=15, padx=20)
        
        # Stile comune per i pulsanti
        btn_style = {
            'font': ('Helvetica', 11, 'bold'),
            'fg': COLORI_TEMA['bianco'],
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'width': 12,
            'cursor': 'hand2'
        }
        
        # Tutti i pulsanti in una riga
        self.btn_connect = tk.Button(btn_frame,
            text="Connetti",
            bg=COLORI_TEMA['blu_campus'],
            activebackground=COLORI_TEMA['azzurro'],
            activeforeground=COLORI_TEMA['bianco'],
            command=self.avvia_connessione,
            **btn_style)
        self.btn_connect.pack(side=tk.LEFT, padx=5)
        
        self.btn_motor = tk.Button(btn_frame,
            text="Avvia Motori",
            bg=COLORI_TEMA['blu_campus'],
            activebackground=COLORI_TEMA['azzurro'],
            activeforeground=COLORI_TEMA['bianco'],
            command=self.toggle_motor,
            state='disabled',
            **btn_style)
        self.btn_motor.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = tk.Button(btn_frame,
            text="Stop",
            bg="#E74C3C",
            activebackground="#C0392B",
            activeforeground=COLORI_TEMA['bianco'],
            command=self.ferma_programma,
            state='disabled',
            **btn_style)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Effetti hover per i pulsanti
        for btn in [self.btn_connect, self.btn_motor, self.btn_stop]:
            btn.bind('<Enter>', lambda e, b=btn: self._on_enter(b))
            btn.bind('<Leave>', lambda e, b=btn: self._on_leave(b))
    
    def avvia_connessione(self):
        # Avvia thread connessione
        if not hasattr(self, 'thread_conn') or not self.thread_conn.is_alive():
            self.thread_conn = threading.Thread(target=self.connetti_ev3)
            self.thread_conn.daemon = True
            self.thread_conn.start()
        
        # Dopo aver abilitato i controlli, abilita anche il pulsante motori
        self.btn_motor.config(state='normal')
    
    def connetti_ev3(self):
        # Gestisce connessione al robot
        self.status_label.config(text="Connessione in corso...", fg=COLORI_TEMA['azzurro'])
        try:
            self.client = socket.socket()
            self.client.settimeout(5)
            self.client.connect((self.ip_entry.get(), 12345))
            
            # Disabilita pulsante connessione
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button) and btn['text'] == "Connetti":
                                    btn.config(state='disabled')
            
            # Abilita controlli
            self.btn_stop.config(state='normal')
            self.btn_motor.config(state='normal')  # Abilita il pulsante motori
            
            # Avvia programma
            self.client.send("START".encode())
            self.status_label.config(text="Programma avviato", fg=COLORI_TEMA['blu_campus'])
            
            # Loop ricezione colori
            while True:
                try:
                    colore = self.client.recv(1024).decode()
                    if colore in self.colori:
                        self.root.after(0, self.aggiorna_display, colore)
                except socket.timeout:
                    continue  # Continua il loop se non ci sono dati
                except Exception as e:
                    print(f"Errore nella ricezione: {e}")
                    break
                
        except Exception as e:
            self.status_label.config(text=f"Errore: {str(e)}", fg='red')
            self.disconnetti()
    
    def disconnetti(self):
        # Gestisce disconnessione
        if hasattr(self, 'client'):
            try:
                self.client.close()
            except:
                pass
        self.btn_stop.config(state='disabled')
        self.btn_motor.config(state='disabled', text="Avvia Motori", bg=COLORI_TEMA['blu_campus'])
    
    def ferma_programma(self):
        # Ferma il programma
        try:
            self.client.send("STOP".encode())
            self.status_label.config(text="Programma terminato", fg=COLORI_TEMA['blu_campus'])
        except:
            pass
        finally:
            self.disconnetti()
            self.root.quit()
    
    def aggiorna_display(self, colore):
        # Aggiorna il display del colore
        self.color_display.config(bg=self.colori[colore])
        self.status_label.config(text=f"Colore rilevato: {colore}", fg=COLORI_TEMA['blu_campus'])
    
    def toggle_motor(self):
        try:
            if self.btn_motor['text'] == "Avvia Motori":
                self.client.send("START_MOTOR".encode())
                self.btn_motor.config(text="Spegni Motori", bg="#E74C3C")
                self.status_label.config(text="Motori avviati", fg=COLORI_TEMA['blu_campus'])
            else:
                self.client.send("STOP_MOTOR".encode())
                self.btn_motor.config(text="Avvia Motori", bg=COLORI_TEMA['blu_campus'])
                self.status_label.config(text="Motori spenti", fg=COLORI_TEMA['blu_campus'])
        except Exception as e:
            self.status_label.config(text=f"Errore controllo motori: {str(e)}", fg='red')

    def _on_entry_focus_in(self, event):
        """Effetto quando l'entry riceve il focus"""
        event.widget.config(
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=2
        )

    def _on_entry_focus_out(self, event):
        """Effetto quando l'entry perde il focus"""
        event.widget.config(
            bg=COLORI_TEMA['grigio_chiaro'],
            highlightthickness=0
        )

    def _on_enter(self, button):
        """Effetto hover quando il mouse entra nel pulsante"""
        if button['state'] != 'disabled':
            button.config(relief='solid', highlightthickness=1)
            # Effetto di scala
            button.config(pady=7)  # Leggermente più piccolo

    def _on_leave(self, button):
        """Effetto hover quando il mouse esce dal pulsante"""
        if button['state'] != 'disabled':
            button.config(relief='flat', highlightthickness=0)
            # Ripristina dimensione originale
            button.config(pady=8)

def main():
    # Funzione principale
    root = tk.Tk()
    app = AppOpenDay(root)
    root.mainloop()

if __name__ == "__main__":
    main() 