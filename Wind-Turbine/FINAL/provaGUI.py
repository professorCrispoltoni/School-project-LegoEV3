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
        self.root = root
        self.root.title("Campus Da Vinci - Sistema Rilevamento Colori")
       
        # Dimensioni fisse della finestra
        window_width = 600
        window_height = 700
       
        # Ottieni dimensioni dello schermo
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
       
        # Calcola posizione per centrare la finestra
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
       
        # Imposta dimensioni e posizione
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        # Disabilita il ridimensionamento
        self.root.resizable(False, False)
        # Imposta lo stile della finestra
        self.root.configure(bg=COLORI_TEMA['grigio_chiaro'])
       
        # Frame principale con padding fisso
        self.main_container = tk.Frame(self.root,
            bg=COLORI_TEMA['grigio_chiaro'])
        self.main_container.pack(expand=True, fill='both', padx=20, pady=20)
        self.main_container.pack_propagate(False)  # Mantiene dimensione fissa
       
        # Dizionario colori per il display
        self.colori = {
            'ROSSO': '#FF0000',
            'VERDE': '#00FF00',
            'BLU': '#0000FF',
            'GIALLO': '#FFFF00',
            'NERO': '#000000',
            'BIANCO': '#FFFFFF'
        }
       
        # Setup dell'interfaccia
        self.setup_gui()

    #GRAFICA
    def setup_gui(self):
        # Layout a colonna unica con Frame separati
        title_frame = tk.Frame(self.main_container, bg=COLORI_TEMA['grigio_chiaro'])
        title_frame.pack(fill='x', pady=20)
       
        # Logo e titolo
        self.setup_logo(title_frame)

        # Frame per connessione
        connection_frame = tk.Frame(self.main_container, bg=COLORI_TEMA['grigio_chiaro'])
        connection_frame.pack(fill='both', expand=True, pady=10)
        self.setup_connection_controls(connection_frame)

        # Frame per acquisizione colori
        #color_frame = tk.Frame(self.main_container, bg=COLORI_TEMA['grigio_chiaro'])
        #color_frame.pack(fill='both', expand=True, pady=10)
        #self.setup_color_display(color_frame)

        # Frame per rilevazione velocità
        velocity_frame = tk.Frame(self.main_container, bg=COLORI_TEMA['bianco'])
        velocity_frame.pack(fill='both', expand=True, pady=10)
        self.setup_velocity_display(velocity_frame)

    def setup_logo(self, main_frame):
        # Carica il logo se disponibile, altrimenti mostra il titolo
        try:
            pil_image = Image.open("logo_Leonard.png")
            pil_image = pil_image.resize((150, 150))
            self.logo_image = ImageTk.PhotoImage(pil_image)
            tk.Label(main_frame, image=self.logo_image,
                    bg=COLORI_TEMA['grigio_chiaro']).pack(pady=15)
        except:
            tk.Label(main_frame, text="IIS Campus Leonardo da Vinci",
                    font=('Helvetica', 22, 'bold'),
                    fg=COLORI_TEMA['blu_campus'],
                    bg=COLORI_TEMA['grigio_chiaro']).pack(pady=15)

    def setup_color_display(self, frame):
        # Container per il display colore con dimensioni fisse
        display_container = tk.Frame(frame,
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=2)
        display_container.pack(fill='both', expand=True, pady=10)
    
        # Titolo con stile migliorato
        title_frame = tk.Frame(display_container,
            bg=COLORI_TEMA['blu_campus'],
            height=25)  # Altezza fissa
        title_frame.pack(fill='x')
    
        label_frame = tk.Label(title_frame,
            text="Acquisizione dati",
            font=('Helvetica', 18, 'bold'),
            fg=COLORI_TEMA['bianco'],
            bg=COLORI_TEMA['blu_campus']).place(relx=0.5, rely=0.5, anchor='center')

        # Display colore centrato con dimensioni fisse
        self.color_display = tk.Frame(display_container,
            width=50,
            height=50,
            bg="gray",
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=3)
        self.color_display.pack(fill='y', expand=True, pady=10)
    
        # Etichetta colore corrente con stile migliorato
        self.color_label = tk.Label(display_container,
            text="In attesa...",
            font=('Helvetica', 16, 'bold'),
            fg=COLORI_TEMA['blu_campus'],
            bg=COLORI_TEMA['bianco'],
            pady=15)
        self.color_label.pack(fill='y', expand=False, pady=10)

    def setup_velocity_display(self, frame):
        # Container per il display della velocità con dimensioni fisse
        velocity_container = tk.Frame(frame,
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=2)
        velocity_container.pack(fill='both', expand=True, pady=10)
    
        # Titolo velocità
        title_frame = tk.Frame(velocity_container,
            bg=COLORI_TEMA['blu_campus'],
            height=25)  # Altezza fissa
        title_frame.pack(fill='x')
    
        label_frame = tk.Label(title_frame,
            text="Rilevazione velocità",
            font=('Helvetica', 18, 'bold'),
            fg=COLORI_TEMA['bianco'],
            bg=COLORI_TEMA['blu_campus']).place(relx=0.5, rely=0.5, anchor='center')

        # Etichetta velocità corrente
        self.velocity_label = tk.Label(velocity_container,
            text="Velocità: 0 m/s",
            font=('Helvetica', 16, 'bold'),
            fg=COLORI_TEMA['blu_campus'],
            bg=COLORI_TEMA['bianco'],
            pady=15)
        self.velocity_label.pack(fill='y', expand=False, pady=10)

    def setup_connection_controls(self, frame):
        # Container per i controlli
        controls_container = tk.Frame(frame,
            bg=COLORI_TEMA['bianco'],
            highlightbackground=COLORI_TEMA['azzurro'],
            highlightthickness=2)
        controls_container.pack(fill='both', expand=True, pady=10)
       
        # Titolo controlli
        tk.Label(controls_container,
            text="Controlli Robot",
            font=('Helvetica', 16, 'bold'),
            fg=COLORI_TEMA['blu_campus'],
            bg=COLORI_TEMA['bianco'],
            pady=10).pack()

        # Status label migliorata
        status_frame = tk.Frame(controls_container, bg=COLORI_TEMA['bianco'])
        status_frame.pack(fill='x', padx=15, pady=10)
       
        self.status_label = tk.Label(status_frame,
            text="In attesa della connessione...",
            font=('Helvetica', 12, 'italic'),
            fg=COLORI_TEMA['grigio_testo'],
            bg=COLORI_TEMA['bianco'])
        self.status_label.pack(fill='x')

        # IP entry con label
        ip_frame = tk.Frame(controls_container, bg=COLORI_TEMA['bianco'])
        ip_frame.pack(fill='x', padx=15, pady=10)
       
        tk.Label(ip_frame,
            text="IP Robot:",
            font=('Helvetica', 12, 'bold'),
            bg=COLORI_TEMA['bianco'],
            fg=COLORI_TEMA['blu_campus']).pack(side=tk.TOP, padx=5)
       
        self.ip_entry = tk.Entry(ip_frame,
            width=15,
            font=('Helvetica', 12),
            bg=COLORI_TEMA['grigio_chiaro'],
            fg=COLORI_TEMA['grigio_testo'],
            relief='flat',
            justify='center')
            
        self.ip_entry.insert(0, "169.254.215.169")
        self.ip_entry.pack(side=tk.TOP, padx=5, ipady=3)
       
        # Pulsanti di controllo
        btn_frame = tk.Frame(controls_container, bg=COLORI_TEMA['bianco'])
        btn_frame.pack(pady=15)
       
        btn_style = {
            'font': ('Helvetica', 12, 'bold'),
            'fg': COLORI_TEMA['bianco'],
            'relief': 'flat',
            'width': 15,
            'height': 2,
            'cursor': 'hand2'
        }
       
        self.btn_connect = tk.Button(btn_frame,
            text="Connetti",
            bg=COLORI_TEMA['blu_campus'],
            command=self.avvia_connessione,
            **btn_style)
        self.btn_connect.pack(pady=5)
       
        self.btn_motor = tk.Button(btn_frame,
            text="Start",
            bg=COLORI_TEMA['blu_campus'],
            state='disabled',
            command=self.toggle_motor,
            **btn_style)
        self.btn_motor.pack(pady=5)
       
        self.btn_stop = tk.Button(btn_frame,
            text="Close",
            bg="#E74C3C",
            state='disabled',
            command=self.ferma_programma,
            **btn_style)
        self.btn_stop.pack(pady=5)

    #LOGICA DI CONTROLLO
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
                    #print(colore)
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
        self.btn_motor.config(state='disabled', text="Start", bg=COLORI_TEMA['blu_campus'])

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
        #self.color_display.config(bg=self.colori[colore])
        self.velocity_label.config(text=f"Velocità: {colore} m/s") #f"Ciao, {nome}! Hai {eta} anni."

    def toggle_motor(self):
        try:
            if self.btn_motor['text'] == "Start":
                self.client.send("START_MOTOR".encode())
                self.btn_motor.config(text="Stop", bg="#E74C3C")
                self.status_label.config(text="Motori avviati", fg=COLORI_TEMA['blu_campus'])
            else:
                self.client.send("STOP_MOTOR".encode())
                self.btn_motor.config(text="Start", bg=COLORI_TEMA['blu_campus'])
                self.status_label.config(text="Motori spenti", fg=COLORI_TEMA['blu_campus'])
        except Exception as e:
            print(f"Errore nel commutare motori: {e}")
            self.status_label.config(text="Errore motori", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppOpenDay(root)
    root.mainloop()
