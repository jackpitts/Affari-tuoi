import os
import math

# =====================================================================
# CONFIGURAZIONE COLORI ANSI
# =====================================================================
CLR_RESET = "\033[0m"
CLR_BLU = "\033[94m"
CLR_ROSSO = "\033[91m"
CLR_VERDE = "\033[92m"
CLR_GIALLO = "\033[93m"
CLR_VIOLA = "\033[95m"
CLR_CYAN = "\033[96m"
BG_ROSSO = "\033[41m\033[97m"
BG_VERDE = "\033[42m\033[97m"

VALORE_ROSSO_INIZIALE_PACCO_NERO = 10000.0

TABELLONE_INIZIALE = {
    "0": 0.0, "1": 1.0, "Drolunga": 0.0, "10": 10.0, "20": 20.0, 
    "50": 50.0, "Gennarino": 0.0, "100": 100.0, "200": 200.0, "Ballerina": 0.0,
    "Pacco Nero": VALORE_ROSSO_INIZIALE_PACCO_NERO, "10000": 10000.0, "15000": 15000.0, 
    "20000": 20000.0, "30000": 30000.0, "50000": 50000.0, "75000": 75000.0, 
    "100000": 100000.0, "200000": 200000.0, "300000": 300000.0
}

class ConsulenteStatistico:
    
    @staticmethod
    def calcola_valore_atteso(premi_rimasti):
        if not premi_rimasti: return 0
        return sum(premi_rimasti.values()) / len(premi_rimasti)

    @staticmethod
    def mostra_analisi_dettagliata_offerta(premi_rimasti, offerta, coefficiente_avversione=0.55):
        n_tot = len(premi_rimasti)
        ev = ConsulenteStatistico.calcola_valore_atteso(premi_rimasti)
        
        ordine_blu = ["0", "1", "Drolunga", "10", "20", "50", "Gennarino", "100", "200", "Ballerina"]
        n_blu = sum(1 for k in premi_rimasti.keys() if k in ordine_blu)
        n_rossi = n_tot - n_blu
        
        prob_blu = (n_blu / n_tot) * 100
        prob_rossi = (n_rossi / n_tot) * 100
        percentuale_ev = (offerta / ev) * 100 if ev > 0 else 0
        
        utilita_tabellone = 0
        for p in premi_rimasti.values():
            val_sicuro = p if p > 0 else 0.01
            utilita_tabellone += math.pow(val_sicuro, 1 - coefficiente_avversione)
        utilita_media = utilita_tabellone / n_tot
        utilita_offerta = math.pow(offerta if offerta > 0 else 0.01, 1 - coefficiente_avversione)
        
        print(f"\n{CLR_VIOLA}🔬 --- REPORT ANALITICO: OFFERTA DEL DOTTORE ---{CLR_RESET}")
        print(f" • Composizione Tabellone: {CLR_BLU}{n_blu} Blu ({prob_blu:.1f}%){CLR_RESET} | {CLR_ROSSO}{n_rossi} Rossi ({prob_rossi:.1f}%){CLR_RESET}")
        print(f" • Valore Atteso Matematico (EV): € {ev:,.2f}")
        print(f" • Offerta Esaminata: € {offerta:,}")
        print(f" • Rapporto di Copertura dell'Offerta: {CLR_GIALLO}{percentuale_ev:.2f}% dell'EV{CLR_RESET}")
        print("-" * 60)
        
        if utilita_offerta > utilita_media:
            verdetto = f"{BG_VERDE} ACCETTA L'OFFERTA {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: L'offerta è solida e supera il valore di utilità del tabellone instabile. Monetizza il percorso riducendo il rischio di crollo.{CLR_RESET}"
        else:
            verdetto = f"{BG_ROSSO} RIFIUTA L'OFFERTA {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Il Dottore offre troppo poco rispetto al patrimonio potenziale dei rossi rimasti. Continua a giocare.{CLR_RESET}"
        
        print(f" {CLR_GIALLO}VERDETTO DEFINITIVO:{CLR_RESET}")
        print(f" {verdetto}\n")

    @staticmethod
    def mostra_analisi_dettagliata_cambio(premi_rimasti, N_totali_rimasti, pacchi_cambiati_log):
        """Calcola la probabilità pura di vincere un rosso basandosi sul momento esatto dell'acquisizione."""
        ordine_blu = ["0", "1", "Drolunga", "10", "20", "50", "Gennarino", "100", "200", "Ballerina"]
        n_blu_attuali = sum(1 for k in premi_rimasti.keys() if k in ordine_blu)
        n_rossi_attuali = len(premi_rimasti) - n_blu_attuali
        
        # Recupero sicuro della memoria storica per evitare qualsiasi crash
        if not pacchi_cambiati_log:
            rossi_al_momento_del_prelievo = 10.0
            quota_al_momento_del_prelievo = 20.0
        else:
            ultimo_elemento = pacchi_cambiati_log[-1]
            if isinstance(ultimo_elemento, tuple):
                quota_al_momento_del_prelievo, rossi_al_momento_del_prelievo = ultimo_elemento
            else:
                # Fallback di sicurezza se trova ancora un vecchio intero nel log
                quota_al_momento_del_prelievo = float(ultimo_elemento)
                rossi_al_momento_del_prelievo = 10.0  # Stima standard iniziale

        # Calcolo probabilità reale congelata del proprio pacco
        prob_mio_pacco_rosso = (rossi_al_momento_del_prelievo / quota_al_momento_del_prelievo) * 100
        if prob_mio_pacco_rosso > 100.0: prob_mio_pacco_rosso = 100.0
        
        # Calcolo probabilità di una singola scatola sul bancone dello studio
        N_altri_pacchi_studio = N_totali_rimasti - 1
        
        if N_altri_pacchi_studio > 0:
            rossi_rimasti_nello_studio = n_rossi_attuali - (prob_mio_pacco_rosso / 100.0)
            if rossi_rimasti_nello_studio < 0: rossi_rimasti_nello_studio = 0
            prob_pacco_studio_rosso = (rossi_rimasti_nello_studio / N_altri_pacchi_studio) * 100
        else:
            prob_pacco_studio_rosso = 0.0

        print(f"\n{CLR_VIOLA}🔬 --- ANALISI STORICA REALE: PROPOSTA DI CAMBIO ---{CLR_RESET}")
        print(f" • Pacchi totali in gioco: {N_totali_rimasti} (Il tuo + {N_altri_pacchi_studio} sul bancone)")
        print(f" • Bilancio attuale tabellone: {CLR_BLU}{n_blu_attuali} Blu{CLR_RESET} vs {CLR_ROSSO}{n_rossi_attuali} Rossi{CLR_RESET}")
        print("-" * 60)
        print(f" {CLR_CYAN}PROBABILITÀ REALE DI CONTENERE UN PREMIO ROSSO:{CLR_RESET}")
        print(f"  -> Se TIENI il tuo pacco attuale (preso a quota {quota_al_momento_del_prelievo:.0f}): {CLR_GIALLO}{prob_mio_pacco_rosso:.2f}%{CLR_RESET} di probabilità che sia ROSSO")
        print(f"  -> Se ACCETTI un pacco dal bancone attuale:        {CLR_GIALLO}{prob_pacco_studio_rosso:.2f}%{CLR_RESET} di probabilità che sia ROSSO")
        print("-" * 60)
        
        if n_rossi_attuali == 0:
            verdetto = f"{BG_ROSSO} CAMBIO INUTILE {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Non ci sono più rossi in gioco.{CLR_RESET}"
        elif abs(prob_pacco_studio_rosso - prob_mio_pacco_rosso) < 0.01:
            verdetto = f"{BG_ROSSO} RIFIUTA IL CAMBIO (EQUILIBRIO) {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: La probabilità è identica ({prob_mio_pacco_rosso:.2f}%). Non c'è alcun vantaggio statistico nel variare, mantieni la tua scelta iniziale.{CLR_RESET}"
        elif prob_pacco_studio_rosso > prob_mio_pacco_rosso:
            verdetto = f"{BG_VERDE} ACCETTA IL CAMBIO {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: I pacchi sul bancone hanno una concentrazione di ROSSI maggiore rispetto alla probabilità congelata nel tuo pacco. Conviene cambiare per massimizzare le probabilità.{CLR_RESET}"
        else:
            verdetto = f"{BG_ROSSO} RIFIUTA IL CAMBIO {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Il tuo pacco ha una probabilità di essere ROSSO superiore rispetto alle scatole rimaste in studio. Difendilo.{CLR_RESET}"
            
        print(f" {CLR_GIALLO}VERDETTO DEFINITIVO:{CLR_RESET}")
        print(f" {verdetto}\n")

# =====================================================================
# LIVE TRACKER CON MEMORIA STORICA
# =====================================================================
class LiveTrackerAffariTuoi:
    def __init__(self):
        self.premi_rimasti = dict(TABELLONE_INIZIALE)
        self.pacchi_rimasti = list(range(1, 21))
        self.pacco_giocatore = None
        self.pacchi_cambiati_log = [] 

    def imposta_pacco_giocatore(self, numero):
        self.pacco_giocatore = numero
        self.pacchi_rimasti.remove(numero)

    def elimina_premio_dal_tabellone(self, chiave_premio):
        if chiave_premio in self.premi_rimasti:
            del self.premi_rimasti[chiave_premio]
            return True
        return False

    def aggiorna_valore_premio(self, chiave_premio, nuovo_valore):
        if chiave_premio in self.premi_rimasti:
            self.premi_rimasti[chiave_premio] = nuovo_valore

    def registra_cambio_pacco(self, nuovo_pacco, quota_pacchi_totale, n_rossi_momento):
        self.pacchi_rimasti.append(self.pacco_giocatore)
        self.pacco_giocatore = nuovo_pacco
        self.pacchi_rimasti.remove(nuovo_pacco)
        # Salvataggio esplicito della tupla
        self.pacchi_cambiati_log.append((quota_pacchi_totale, n_rossi_momento))

# =====================================================================
# INTERFACCIA RENDERING GRAFICA
# =====================================================================
def render_interfaccia_live(tracker):
    os.system('cls' if os.name == 'nt' else 'clear')
    ev = ConsulenteStatistico.calcola_valore_atteso(tracker.premi_rimasti)
    n_tot_rimasti = len(tracker.pacchi_rimasti) + 1
    
    print(f"{CLR_GIALLO}" + "=" * 78 + f"{CLR_RESET}")
    print(f" {CLR_VIOLA}         AFFARI TUOI - CONSOLLE CON MEMORIA STORICA DEI CAMBI{CLR_RESET}")
    print(f"{CLR_GIALLO}" + "=" * 78 + f"{CLR_RESET}")
    print(f" Il tuo Pacco attuale: {CLR_CYAN}[{tracker.pacco_giocatore}]{CLR_RESET} | Numeri ancora in gioco in studio: {CLR_GIALLO}{sorted(tracker.pacchi_rimasti)}{CLR_RESET}")
    print(f" Conteggio Pacchi Rimasti: {CLR_CYAN}{n_tot_rimasti} su 20{CLR_RESET}")
    if tracker.pacchi_cambiati_log:
        storia_stampa = []
        for x in tracker.pacchi_cambiati_log:
            if isinstance(x, tuple):
                storia_stampa.append(f"Q:{x[0]} R:{x[1]}")
            else:
                storia_stampa.append(f"Q:{x}")
        print(f" Registro storico cambi (Quota/Rossi): {CLR_VIOLA}{' -> '.join(storia_stampa)}{CLR_RESET}")
    print("-" * 78)
    
    ordine_blu = ["0", "1", "Drolunga", "10", "20", "50", "Gennarino", "100", "200", "Ballerina"]
    ordine_rossi = ["Pacco Nero", "10000", "15000", "20000", "30000", "50000", "75000", "100000", "200000", "300000"]
    
    print(f"  {CLR_BLU}TABELLONE BLU (SINISTRA){CLR_RESET}".ljust(45) + f"|  {CLR_ROSSO}TABELLONE ROSSI (DESTRA){CLR_RESET}")
    print("-" * 78)
    
    for i in range(10):
        chiave_b = ordine_blu[i]
        if chiave_b in tracker.premi_rimasti:
            val_b = tracker.premi_rimasti[chiave_b]
            lbl_b = f"€ {val_b:,}" if val_b > 0 or chiave_b.isdigit() else chiave_b
            b_str = f"{CLR_BLU}● {lbl_b}{CLR_RESET}"
        else: b_str = f"\033[90mX {chiave_b}\033[0m"
            
        chiave_r = ordine_rossi[i]
        if chiave_r in tracker.premi_rimasti:
            val_r = tracker.premi_rimasti[chiave_r]
            if chiave_r == "Pacco Nero":
                lbl_r = f"Pacco Nero (Rosso Presunto: € {val_r:,.0f})" if val_r == VALORE_ROSSO_INIZIALE_PACCO_NERO else f"Pacco Nero (Adattato: € {val_r:,})"
                r_str = f"{CLR_ROSSO}● {lbl_r}{CLR_RESET}"
            else: r_str = f"{CLR_ROSSO}● € {val_r:,}{CLR_RESET}"
        else: r_str = f"\033[90mX {chiave_r}\033[0m"
            
        print(f"  {b_str.ljust(44)} |  {r_str}")
        
    print("-" * 78)
    colore_ev = CLR_VERDE if ev > 35000 else CLR_ROSSO
    print(f" >>> VALORE ATTESO REALE DEL TABELLONE (Media): {colore_ev}€ {ev:,.2f}{CLR_RESET} <<<")
    print(f"{CLR_GIALLO}" + "=" * 78 + f"{CLR_RESET}")

# =====================================================================
# LOOP PRINCIPALE
# =====================================================================
def main():
    tracker = LiveTrackerAffariTuoi()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CLR_CYAN}=== INIZIALIZZAZIONE PARTITA ==={CLR_RESET}")
    while True:
        try:
            pacco_iniziale = int(input("Che numero di pacco ha il concorrente stasera? (1-20): "))
            if 1 <= pacco_iniziale <= 20:
                tracker.imposta_pacco_giocatore(pacco_iniziale)
                break
        except ValueError: pass
        print("Numero non valido.")

    while len(tracker.premi_rimasti) > 1:
        render_interfaccia_live(tracker)
        n_tot_rimasti = len(tracker.pacchi_rimasti) + 1
        
        print(f" {CLR_VIOLA}[MENU LIVE CONSOLE]{CLR_RESET}")
        print("  1 -> Elimina un premio uscito in TV")
        print("  2 -> È stato aperto il PACCO NERO")
        print("  3 -> Il Dottore offre dei SOLDI")
        print("  4 -> Il Dottore offre il CAMBIO PACCO")
        print("  0 -> Chiudi programma")
        
        scelta = input("\nSeleziona l'azione: ").strip()
        
        if scelta == "1":
            chiave = input("\nScrivi il NOME o il VALORE del premio uscito: ").strip()
            if tracker.elimina_premio_dal_tabellone(chiave):
                try:
                    npacco = int(input("Quale numero di pacco fisico è stato aperto? "))
                    if npacco in tracker.pacchi_rimasti: tracker.pacchi_rimasti.remove(npacco)
                except ValueError: pass
            else:
                print(f"{CLR_ROSSO}Errore: Elemento non trovato!{CLR_RESET}")
                input("Premi INVIO per continuare...")
                
        elif scelta == "2":
            if "Pacco Nero" in tracker.premi_rimasti:
                try:
                    valore = float(input("\nQuale valore reale è uscito dal Pacco Nero? € "))
                    tracker.aggiorna_valore_premio("Pacco Nero", valore)
                except ValueError: pass
            else: input("Pacco Nero già eliminato. Premi INVIO...")
                
        elif scelta == "3":
            try:
                offerta = float(input("\nInserisci la cifra offerta dal Dottore: € "))
                ConsulenteStatistico.mostra_analisi_dettagliata_offerta(tracker.premi_rimasti, offerta)
                
                esito = input("Il concorrente ha ACCETTATO o RIFIUTATO l'offerta? (accettato/rifiutato): ").strip().lower()
                if esito == "accettato": return
            except ValueError: pass
            
        elif scelta == "4":
            ConsulenteStatistico.mostra_analisi_dettagliata_cambio(tracker.premi_rimasti, n_tot_rimasti, tracker.pacchi_cambiati_log)
            
            esito = input("Il concorrente accetta il cambio? (si/no): ").strip().lower()
            if esito == 'si':
                try:
                    nuovo = int(input(f"Quale numero di pacco prende tra i rimasti {sorted(tracker.pacchi_rimasti)}? "))
                    if nuovo in tracker.pacchi_rimasti: 
                        ordine_blu = ["0", "1", "Drolunga", "10", "20", "50", "Gennarino", "100", "200", "Ballerina"]
                        n_blu = sum(1 for k in tracker.premi_rimasti.keys() if k in ordine_blu)
                        n_rossi_momento = len(tracker.premi_rimasti) - n_blu
                        
                        tracker.registra_cambio_pacco(nuovo, n_tot_rimasti, n_rossi_momento)
                except ValueError: pass
                
        elif scelta == "0":
            break

if __name__ == "__main__":
    main()