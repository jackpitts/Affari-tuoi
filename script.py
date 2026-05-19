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

TABELLONE_INIZIALE = {
    "0": 0.0, "1": 1.0, "Gioco 1": 0.0, "10": 10.0, "20": 20.0, 
    "50": 50.0, "Gennarino": 0.0, "100": 100.0, "200": 200.0, "Gioco 2": 0.0,
    "10000": 10000.0, "15000": 15000.0, "20000": 20000.0, "30000": 30000.0, 
    "50000": 50000.0, "75000": 75000.0, "100000": 100000.0, "200000": 200000.0, 
    "300000": 300000.0, "Pacco Nero": "NEUTRO"
}

ORDINE_BLU = ["0", "1", "Gioco 1", "10", "20", "50", "Gennarino", "100", "200", "Gioco 2"]
ORDINE_ROSSI = ["10000", "15000", "20000", "30000", "50000", "75000", "100000", "200000", "300000"]

class ConsulenteStatistico:
    
    @staticmethod
    def calcola_valore_atteso(premi_rimasti):
        valori_noti = [v for k, v in premi_rimasti.items() if isinstance(v, (int, float))]
        if not valori_noti: return 0
        return sum(valori_noti) / len(valori_noti)

    @staticmethod
    def conta_colori_puri(premi_rimasti):
        blu = sum(1 for k in premi_rimasti.keys() if k in ORDINE_BLU)
        rossi = sum(1 for k in premi_rimasti.keys() if k in ORDINE_ROSSI)
        return blu, rossi

    @staticmethod
    def mostra_analisi_dettagliata_offerta(premi_rimasti, offerta, coefficiente_avversione=0.55):
        n_blu, n_rossi = ConsulenteStatistico.conta_colori_puri(premi_rimasti)
        pacco_nero_presente = "Pacco Nero" in premi_rimasti
        n_tot_calcolabili = n_blu + n_rossi
        
        ev = ConsulenteStatistico.calcola_valore_atteso(premi_rimasti)
        prob_blu = (n_blu / n_tot_calcolabili) * 100 if n_tot_calcolabili > 0 else 0
        prob_rossi = (n_rossi / n_tot_calcolabili) * 100 if n_tot_calcolabili > 0 else 0
        percentuale_ev = (offerta / ev) * 100 if ev > 0 else 0
        
        utilita_tabellone = 0
        for k, p in premi_rimasti.items():
            if isinstance(p, (int, float)):
                val_sicuro = p if p > 0 else 0.01
                utilita_tabellone += math.pow(val_sicuro, 1 - coefficiente_avversione)
        
        utilita_media = utilita_tabellone / n_tot_calcolabili if n_tot_calcolabili > 0 else 0
        utilita_offerta = math.pow(offerta if offerta > 0 else 0.01, 1 - coefficiente_avversione)
        
        print(f"\n{CLR_VIOLA}🔬 --- REPORT ANALITICO: OFFERTA DEL DOTTORE ---{CLR_RESET}")
        p_nero_str = f" | + {CLR_GIALLO}Pacco Nero Ignoto{CLR_RESET}" if pacco_nero_presente else ""
        print(f" • Composizione Certificata: {CLR_BLU}{n_blu} Blu ({prob_blu:.1f}%){CLR_RESET} | {CLR_ROSSO}{n_rossi} Rossi ({prob_rossi:.1f}%){CLR_RESET}{p_nero_str}")
        print(f" • Valore Atteso Matematico dei noti (EV): € {ev:,.2f}")
        print(f" • Offerta Esaminata: € {offerta:,}")
        print(f" • Rapporto di Copertura dell'Offerta: {CLR_GIALLO}{percentuale_ev:.2f}% dell'EV{CLR_RESET}")
        print("-" * 60)
        
        if utilita_offerta > utilita_media:
            verdetto = f"{BG_VERDE} ACCETTA L'OFFERTA {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: L'offerta copre bene l'utilità dei premi noti riducendo l'incertezza.{CLR_RESET}"
        else:
            verdetto = f"{BG_ROSSO} RIFIUTA L'OFFERTA {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: L'offerta è speculativa rispetto al patrimonio dei rossi certi rimasti.{CLR_RESET}"
        
        print(f" {CLR_GIALLO}VERDETTO DEFINITIVO:{CLR_RESET}")
        print(f" {verdetto}\n")

    @staticmethod
    def mostra_analisi_dettagliata_cambio(premi_rimasti, N_totali_rimasti, pacchi_cambiati_log):
        _, n_rossi_attuali = ConsulenteStatistico.conta_colori_puri(premi_rimasti)
        
        if not pacchi_cambiati_log:
            rossi_al_momento_del_prelievo = 9.0
            quota_al_momento_del_prelievo = 20.0
        else:
            quota_al_momento_del_prelievo, rossi_al_momento_del_prelievo = pacchi_cambiati_log[-1]

        prob_mio_pacco_rosso = (rossi_al_momento_del_prelievo / quota_al_momento_del_prelievo) * 100
        if prob_mio_pacco_rosso > 100.0: prob_mio_pacco_rosso = 100.0
        
        N_altri_pacchi_studio = N_totali_rimasti - 1
        
        if N_altri_pacchi_studio > 0:
            rossi_rimasti_nello_studio = n_rossi_attuali - (prob_mio_pacco_rosso / 100.0)
            if rossi_rimasti_nello_studio < 0: rossi_rimasti_nello_studio = 0
            prob_pacco_studio_rosso = (rossi_rimasti_nello_studio / N_altri_pacchi_studio) * 100
        else:
            prob_pacco_studio_rosso = 0.0

        print(f"\n{CLR_VIOLA}🔬 --- ANALISI STORICA REALE: PROPOSTA DI CAMBIO ---{CLR_RESET}")
        print(f" • Pacchi totali fisici in gioco: {N_totali_rimasti} (Il tuo + {N_altri_pacchi_studio} sul bancone)")
        print(f" • Rossi puri rimasti sul tabellone: {CLR_ROSSO}{n_rossi_attuali} su 9 complessivi{CLR_RESET}")
        print("-" * 60)
        print(f" {CLR_CYAN}PROBABILITÀ REALE DI CONTENERE UN PREMIO ROSSO PURO:{CLR_RESET}")
        print(f"  -> Se TIENI il tuo pacco attuale (preso a quota {quota_al_momento_del_prelievo:.0f}): {CLR_GIALLO}{prob_mio_pacco_rosso:.2f}%{CLR_RESET} di probabilità che sia ROSSO")
        print(f"  -> Se ACCETTI un pacco dal bancone attuale:        {CLR_GIALLO}{prob_pacco_studio_rosso:.2f}%{CLR_RESET} di probabilità che sia ROSSO")
        print("-" * 60)
        
        if n_rossi_attuali == 0:
            verdetto = f"{BG_ROSSO} CAMBIO INUTILE {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Non ci sono più rossi puri in gioco.{CLR_RESET}"
        elif abs(prob_pacco_studio_rosso - prob_mio_pacco_rosso) < 0.01:
            verdetto = f"{BG_ROSSO} RIFIUTA IL CAMBIO (EQUILIBRIO) {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Le probabilità sui rossi sono identiche. Mantieni il tuo pacco attuale.{CLR_RESET}"
        elif prob_pacco_studio_rosso > prob_mio_pacco_rosso:
            verdetto = f"{BG_VERDE} ACCETTA IL CAMBIO {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: I pacchi sul bancone hanno una densità di ROSSI puri superiore rispetto alla probabilità congelata nel tuo pacco.{CLR_RESET}"
        else:
            verdetto = f"{BG_ROSSO} RIFIUTA IL CAMBIO {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Il tuo pacco ha una probabilità di essere ROSSO puro superiore rispetto ai pacchi rimasti sul bancone.{CLR_RESET}"
            
        print(f" {CLR_GIALLO}VERDETTO DEFINITIVO:{CLR_RESET}")
        print(f" {verdetto}\n")

    @staticmethod
    def mostra_analisi_finalissima_due_pacchi(premi_rimasti, pacco_giocatore, pacco_studio, pacchi_cambiati_log):
        # Estraiamo i due valori effettivi rimasti sul tabellone
        valori = []
        for k, v in premi_rimasti.items():
            if isinstance(v, (int, float)):
                valori.append((v, k))
        
        # Se non ci sono esattamente due premi calcolabili, interrompiamo
        if len(valori) != 2:
            return
            
        # Ordiniamo i premi per capire qual è il più alto e qual è il più basso
        valori.sort(key=lambda x: x[0])
        premio_basso_val, premio_basso_nome = valori[0]
        premio_alto_val, premio_alto_nome = valori[1]

        # Recuperiamo la probabilità storica che il pacco del giocatore sia un ROSSO PURO
        if not pacchi_cambiati_log:
            rossi_origine = 9.0
            quota_origine = 20.0
        else:
            quota_origine, rossi_origine = pacchi_cambiati_log[-1]
            
        prob_mio_rosso = rossi_origine / quota_origine

        # Definiamo la probabilità che il proprio pacco contenga il premio più alto
        # Caso A: Sul tabellone ci sono 1 Blu e 1 Rosso
        if premio_basso_nome in ORDINE_BLU and premio_alto_nome in ORDINE_ROSSI:
            prob_alto_nel_mio = prob_mio_rosso
            
        # Caso B: Sul tabellone ci sono 2 Rossi (vince chi ha la densità storica maggiore di contenere un rosso generico)
        elif premio_basso_nome in ORDINE_ROSSI and premio_alto_nome in ORDINE_ROSSI:
            prob_alto_nel_mio = 0.50 + (prob_mio_rosso * 0.05) # Correzione statistica di ponderazione
            
        # Caso C: Sul tabellone ci sono 2 Blu (equilibrio perfetto di probabilità)
        else:
            prob_alto_nel_mio = 0.50

        # Controllo dei limiti matematici
        if prob_alto_nel_mio > 1.0: prob_alto_nel_mio = 0.95
        if prob_alto_nel_mio < 0.0: prob_alto_nel_mio = 0.05
        
        prob_alto_nel_banco = 1.0 - prob_alto_nel_mio

        print(f"\n{CLR_VIOLA}🏁 --- ANALISI FINALE: SCONTRO DIRETTO DEGLI ULTIMI 2 PACCHI ---{CLR_RESET}")
        print(f" • Premio Minore Rimasto: {CLR_BLU if premio_basso_nome in ORDINE_BLU else CLR_ROSSO}€ {premio_basso_val:,} ({premio_basso_nome}){CLR_RESET}")
        print(f" • Premio Maggiore Rimasto: {CLR_ROSSO}€ {premio_alto_val:,} ({premio_alto_nome}){CLR_RESET}")
        print("-" * 60)
        print(f" {CLR_CYAN}PROBABILITÀ STATISTICA DI CONTENERE IL PREMIO PIÙ ALTO (€ {premio_alto_val:,}):{CLR_RESET}")
        print(f"  -> Nel TUO pacco attuale [{pacco_giocatore}]: {CLR_VERDE if prob_alto_nel_mio >= prob_alto_nel_banco else CLR_GIALLO}{prob_alto_nel_mio*100:.2f}%{CLR_RESET}")
        print(f"  -> Nel pacco sul BANCONE [{pacco_studio}]: {CLR_VERDE if prob_alto_nel_banco > prob_alto_nel_mio else CLR_GIALLO}{prob_alto_nel_banco*100:.2f}%{CLR_RESET}")
        print("-" * 60)
        
        if abs(prob_alto_nel_mio - prob_alto_nel_banco) < 0.001:
            verdetto = f"{BG_VERDE} MATEMATICAMENTE EQUIVALENTE (50/50) {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: Entrambi i pacchi hanno la stessa identica probabilità. Scegli di pancia.{CLR_RESET}"
        elif prob_alto_nel_mio > prob_alto_nel_banco:
            verdetto = f"{BG_VERDE} TIENI IL TUO PACCO {CLR_RESET}\n{CLR_VERDE}MOTIVAZIONE: La storia dei cambi indica che il tuo pacco ha conservato una probabilità superiore rispetto al bancone.{CLR_RESET}"
        else:
            verdetto = f"{BG_ROSSO} ACCETTA IL CAMBIO / APRI IL BANCONE {CLR_RESET}\n{CLR_ROSSO}MOTIVAZIONE: Statisticamente il pacco rimasto in studio ha una densità favorevole superiore rispetto al tuo.{CLR_RESET}"
            
        print(f" {CLR_GIALLO}CONSIGLIO ESTRATTO:{CLR_RESET}")
        print(f" {verdetto}\n")

# =====================================================================
# LIVE TRACKER
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

    def registra_cambio_pacco(self, nuovo_pacco, quota_pacchi_totale, n_rossi_momento):
        self.pacchi_rimasti.append(self.pacco_giocatore)
        self.pacco_giocatore = nuovo_pacco
        self.pacchi_rimasti.remove(nuovo_pacco)
        self.pacchi_cambiati_log.append((quota_pacchi_totale, n_rossi_momento))

# =====================================================================
# INTERFACCIA RENDERING GRAFICA
# =====================================================================
def render_interfaccia_live(tracker):
    os.system('cls' if os.name == 'nt' else 'clear')
    ev = ConsulenteStatistico.calcola_valore_atteso(tracker.premi_rimasti)
    n_tot_rimasti = len(tracker.pacchi_rimasti) + 1
    
    print(f"{CLR_GIALLO}" + "=" * 78 + f"{CLR_RESET}")
    print(f" {CLR_VIOLA}      AFFARI TUOI - CONSOLLE OTTIMIZZATA (MEMORIA STORICA ATTIVA){CLR_RESET}")
    print(f"{CLR_GIALLO}" + "=" * 78 + f"{CLR_RESET}")
    print(f" Il tuo Pacco attuale: {CLR_CYAN}[{tracker.pacco_giocatore}]{CLR_RESET} | Numeri in gioco in studio: {CLR_GIALLO}{sorted(tracker.pacchi_rimasti)}{CLR_RESET}")
    print(f" Conteggio Pacchi Fisici Rimasti: {CLR_CYAN}{n_tot_rimasti} su 20{CLR_RESET}")
    if tracker.pacchi_cambiati_log:
        storia_stampa = [f"Q:{x[0]} R_Puri:{x[1]}" for x in tracker.pacchi_cambiati_log]
        print(f" Registro storico cambi (Quota/Rossi Puri): {CLR_VIOLA}{' -> '.join(storia_stampa)}{CLR_RESET}")
    print("-" * 78)
    
    print(f"  {CLR_BLU}TABELLONE BLU (SINISTRA){CLR_RESET}".ljust(45) + f"|  {CLR_ROSSO}TABELLONE ROSSI (DESTRA){CLR_RESET}")
    print("-" * 78)
    
    for i in range(10):
        if i < len(ORDINE_BLU):
            chiave_b = ORDINE_BLU[i]
            if chiave_b in tracker.premi_rimasti:
                val_b = tracker.premi_rimasti[chiave_b]
                lbl_b = f"€ {val_b:,}" if val_b > 0 or chiave_b.isdigit() else chiave_b
                b_str = f"{CLR_BLU}● {lbl_b}{CLR_RESET}"
            else: b_str = f"\033[90mX {chiave_b}\033[0m"
        else: b_str = ""
            
        if i < len(ORDINE_ROSSI):
            chiave_r = ORDINE_ROSSI[i]
            if chiave_r in tracker.premi_rimasti:
                val_r = tracker.premi_rimasti[chiave_r]
                r_str = f"{CLR_ROSSO}● € {val_r:,}{CLR_RESET}"
            else: r_str = f"\033[90mX {chiave_r}\033[0m"
        elif i == 9: 
            if "Pacco Nero" in tracker.premi_rimasti:
                stato_nero = tracker.premi_rimasti["Pacco Nero"]
                if stato_nero == "NEUTRO":
                    r_str = f"{CLR_GIALLO}● Pacco Nero (In Gioco - Neutro){CLR_RESET}"
                else:
                    r_str = f"\033[90mX Pacco Nero (Aperto - Conteneva: {stato_nero}){CLR_RESET}"
            else:
                r_str = f"\033[90mX Pacco Nero (Aperto ed Eliminato)\033[0m"
            
        print(f"  {b_str.ljust(44)} |  {r_str}")
        
    print("-" * 78)
    print(f" >>> VALORE ATTESO REALE (Solo premi certi conosciuti): {CLR_VERDE}€ {ev:,.2f}{CLR_RESET} <<<")
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
        
        # INTERCETTATORE FINALE: Se mancano solo 2 pacchi totali, stampa l'analisi predittiva automatica
        if n_tot_rimasti == 2:
            pacco_studio_rimasto = tracker.pacchi_rimasti[0]
            ConsulenteStatistico.mostra_analisi_finalissima_due_pacchi(
                tracker.premi_rimasti, 
                tracker.pacco_giocatore, 
                pacco_studio_rimasto, 
                tracker.pacchi_cambiati_log
            )

        print(f" {CLR_VIOLA}[MENU LIVE CONSOLLE]{CLR_RESET}")
        print("  1 -> Elimina un premio uscito in TV (Blu o Rosso Puro)")
        print("  2 -> È STATO APERTO IL PACCO NERO")
        print("  3 -> Il Dottore offre dei SOLDI")
        print("  4 -> Il Dottore offre il CAMBIO PACCO")
        print("  0 -> Chiudi programma")
        
        scelta = input("\nSeleziona l'azione: ").strip()
        
        if scelta == "1":
            try:
                # 1. Chiede il numero del pacco fisico con controllo duplicati
                npacco = int(input("\nQuale numero di pacco fisico è stato aperto? "))
                if npacco == tracker.pacco_giocatore:
                    print(f"{CLR_ROSSO}Errore: Il pacco {npacco} è quello in possesso del giocatore!{CLR_RESET}")
                    input("Premi INVIO per continuare...")
                    continue
                if npacco not in tracker.pacchi_rimasti:
                    print(f"{CLR_ROSSO}Errore: Il pacco {npacco} è già uscito o non è valido!{CLR_RESET}")
                    input("Premi INVIO per continuare...")
                    continue
                
                # 2. Chiede il valore/nome del premio con controllo presenza
                chiave = input("Scrivi il NOME o il VALORE del premio trovato dentro: ").strip()
                
                if chiave == "Pacco Nero":
                    print(f"{CLR_ROSSO}Usa l'opzione 2 per gestire l'apertura del Pacco Nero!{CLR_RESET}")
                    input("Premi INVIO...")
                    continue
                    
                if chiave not in tracker.premi_rimasti:
                    print(f"{CLR_ROSSO}Errore: Il premio '{chiave}' è già uscito o non esiste!{CLR_RESET}")
                    input("Premi INVIO per continuare...")
                    continue
                    
                # Se i controlli passano, elimina il premio e il pacco
                if tracker.elimina_premio_dal_tabellone(chiave):
                    tracker.pacchi_rimasti.remove(npacco)
            except ValueError:
                print(f"{CLR_ROSSO}Errore: Inserisci un numero valido per il pacco!{CLR_RESET}")
                input("Premi INVIO per continuare...")
                
        elif scelta == "2":
            if "Pacco Nero" in tracker.premi_rimasti and tracker.premi_rimasti["Pacco Nero"] == "NEUTRO":
                try:
                    # 1. Chiede il numero del pacco fisico con controllo duplicati
                    npacco = int(input("\nQuale numero di pacco fisico conteneva il Pacco Nero? "))
                    if npacco == tracker.pacco_giocatore:
                        print(f"{CLR_ROSSO}Errore: Il pacco {npacco} è quello in possesso del giocatore!{CLR_RESET}")
                        input("Premi INVIO per continuare...")
                        continue
                    if npacco not in tracker.pacchi_rimasti:
                        print(f"{CLR_ROSSO}Errore: Il pacco {npacco} è già uscito o non è valido!{CLR_RESET}")
                        input("Premi INVIO per continuare...")
                        continue
                    
                    # 2. Chiede il valore estratto (SENZA blocchi o controlli sul testo inserito)
                    valore_estratto = input("Quale valore/premio è uscito dal Pacco Nero? ").strip()
                    
                    tracker.premi_rimasti["Pacco Nero"] = valore_estratto
                    tracker.pacchi_rimasti.remove(npacco)
                        
                    print(f"{CLR_VERDE}Registrato. Il Pacco Nero è stato escluso dai calcoli matematici.{CLR_RESET}")
                except ValueError:
                    print(f"{CLR_ROSSO}Errore: Inserisci un numero valido per il pacco!{CLR_RESET}")
            else:
                print(f"{CLR_ROSSO}Il Pacco Nero è già stato aperto ed eliminato!{CLR_RESET}")
            input("Premi INVIO per continuare...")
                
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
                        _, n_rossi_puri = ConsulenteStatistico.conta_colori_puri(tracker.premi_rimasti)
                        tracker.registra_cambio_pacco(nuovo, n_tot_rimasti, n_rossi_puri)
                except ValueError: pass
                
        elif scelta == "0":
            break

if __name__ == "__main__":
    main()