# Regole di Normalizzazione dei Ruoli per la Colonna Contributors

## Panoramica

Questo documento descrive il processo di normalizzazione applicato alla colonna `contributors` nel dataset delle ricerche di dottorato. Il processo di normalizzazione standardizza i nomi dei ruoli preservando la struttura e il contenuto delle informazioni sui contributori.

La normalizzazione è guidata da un file di mapping CSV che definisce la relazione tra le variazioni dei ruoli e le loro forme standardizzate, consentendo una trasformazione dei ruoli coerente e mantenibile.

---

## Finalità

La colonna contributors contiene informazioni sulle persone coinvolte nella supervisione e valutazione della ricerca di dottorato. Queste voci utilizzano varie terminologie di ruolo in diverse lingue (principalmente italiano, inglese e francese) e includono variazioni ortografiche, errori di battitura e formattazione incoerente. Il processo di normalizzazione mappa tutte le variazioni di ruolo a nomi di ruolo standardizzati per consentire un'analisi dei dati coerente.

Inoltre, quando il nome di un contributore appare senza un ruolo associato, verrà automaticamente assegnato un ruolo predefinito per garantire che tutti i contributori abbiano designazioni di ruolo esplicite nell'output normalizzato.

---

## Modelli di Formato dei Dati

La colonna `contributors` presenta quattro modelli principali:

### Modello 1: Formato Strutturato con Ruoli
**Formato:** `<ruolo>: <nome>; <ruolo>: <nome>; ...`

Tutte le voci includono sia informazioni sul ruolo che sul nome, separate da punti e virgola.

**Esempi:**
- `coordinatore: Romano Orrù; tutor: Paolo Savarese; co-tutor: Giovanni Franchi`
- `principal supervisor: Alessandro De Nisco; co-supervisor: Luca Petruzzellis`
- `supervisor: Claudia Monacelli; co-supervisor: Stefania Cerrito; program coordinator: Alessandro De Nisco`

### Modello 2: Solo Nomi
**Formato:** `<nome>; <nome>; ...`

Le voci contengono solo nomi senza specificazioni di ruolo, separati da punti e virgola.

**Esempi (Originale):**
- `Siciliano Velia; Benfenati Fabio`
- `Del Mastro Lucia; Quarto Rodolfo`
- `Lo Basso Luca; FLORISTÁN IMÍZCOZ, ALFREDO CASTILLA URBANO, FRANCISCO; Cassata Francesco`
### TODO(tommaso): posso gestire il caso virgola ?

**Nota:** Dopo la normalizzazione, verrà assegnato un ruolo predefinito a ciascun nome in questo modello.

### Modello 3: Formato Misto
**Formato:** `<ruolo>: <nome>; <nome>; ...` oppure `<nome>; <ruolo>: <nome>; ...`

Alcune voci includono ruoli mentre altre no all'interno dello stesso campo.

**Esempi (Originale):**
- `Clini Paolo; Tutor Aziendale: Panzini Alessandra; Fatone Francesco`

**Nota:** Dopo la normalizzazione, ai nomi senza ruoli verrà assegnato il ruolo predefinito.

### Modello 4: Voce Singola
**Formato:** `<nome>` oppure `<ruolo>: <nome>`

Un singolo contributore senza separatori con punto e virgola.

**Esempi (Originale):**
- `MAURIZIO RIPEPE`
- `Vigni Stefano`
- `Biondi Andrea`

**Nota:** Dopo la normalizzazione, ai singoli nomi senza ruoli verrà assegnato il ruolo predefinito.

---

## Processo di Normalizzazione dei Ruoli

### Assegnazione del Ruolo Predefinito

**Regola Chiave:** Qualsiasi nome di contributore che non ha un ruolo associato riceverà un ruolo predefinito durante il processo di normalizzazione.

**Ruolo Predefinito:** `contributor`

Questo garantisce che tutte le voci nel dataset normalizzato abbiano una designazione di ruolo esplicita, consentendo interrogazioni e analisi coerenti.

**Esempi di Assegnazione del Ruolo Predefinito:**

1. **Nome singolo senza ruolo:**
   - Originale: `MAURIZIO RIPEPE`
   - Normalizzato: `contributor: MAURIZIO RIPEPE`

2. **Nomi multipli senza ruoli:**
   - Originale: `Siciliano Velia; Benfenati Fabio`
   - Normalizzato: `contributor: Siciliano Velia; contributor: Benfenati Fabio`

3. **Formato misto (alcuni con ruoli, altri senza):**
   - Originale: `Clini Paolo; Tutor Aziendale: Panzini Alessandra; Fatone Francesco`
   - Normalizzato: `contributor: Clini Paolo; tutor: Panzini Alessandra; contributor: Fatone Francesco`

4. **Formato misto con normalizzazione del ruolo:**
   - Originale: `coordinatore: Maria Rossi; Giovanni Bianchi; tutor: Luca Verdi`
   - Normalizzato: `coordinator: Maria Rossi; contributor: Giovanni Bianchi; tutor: Luca Verdi`

---

### Passo 1: Estrazione e Identificazione dei Ruoli

Per ogni voce nella colonna contributors:

1. Analizzare la voce dividendo per punto e virgola (`;`) per identificare le singole voci dei contributori
2. Per ogni voce di contributore, verificare se contiene i due punti (`:`)
3. Se sono presenti i due punti, estrarre il testo prima dei due punti come potenziale ruolo
4. Se non sono presenti i due punti, la voce contiene solo un nome e riceverà il ruolo predefinito (`contributor`)

### Passo 2: Mappatura dei Ruoli Utilizzando il Dizionario CSV

Ogni ruolo identificato viene convertito in minuscolo e confrontato con il dizionario di mappatura dei ruoli creato dal file CSV. Il ruolo viene quindi mappato al suo equivalente normalizzato.

**Processo di Mappatura:**
1. Convertire il ruolo estratto in minuscolo
2. Cercare il ruolo nel dizionario (creato dal file CSV con mappature `role` → `normalized_role`)
3. Sostituire il ruolo originale con il ruolo normalizzato dal dizionario
4. Se il ruolo non viene trovato nel dizionario, mantenere il ruolo originale e segnalarlo per revisione manuale

#### Ruoli Normalizzati Principali

Il processo di normalizzazione mappa tutte le variazioni ai seguenti ruoli standardizzati:

| Ruolo Normalizzato | Descrizione |
|-----------------|-------------|
| `coordinator` | Coordinatore del programma o ciclo di dottorato |
| `tutor` | Tutor o mentore principale |
| `co-tutor` | Tutor o co-mentore secondario |
| `supervisor` | Supervisore accademico principale |
| `principal supervisor` | Professore supervisore principale |
| `co-supervisor` | Supervisore accademico secondario |
| `advisor` | Consigliere accademico o direttore di tesi (relatore) |
| `co-advisor` | Co-consigliere o co-direttore (correlatore) |
| `evaluator` | Valutatore o esaminatore di tesi (valutatore) |
| `reviewer` | Revisore esterno o interno |
| `contributor` | **Ruolo predefinito** assegnato quando non è specificato alcun ruolo |

#### Esempi di Mappatura

**Variazioni di Coordinatore:**
- `coordinatore` → `coordinator`
- `coordinatrice` → `coordinator` (forma femminile)
- `coordinatori` → `coordinator` (forma plurale)
- `coordinatre` → `coordinator` (errore di battitura)
- `program coordinator` → `coordinator`
- `ph.d. coordinator` → `coordinator`

**Variazioni di Supervisore:**
- `supervisore` → `supervisor`
- `supervisori` → `supervisor` (plurale)
- `principal supervisor` → `principal supervisor`
- `cosupervisore` → `co-supervisor`
- `co-supervisore` → `co-supervisor`
- `co-supervisor` → `co-supervisor`

**Variazioni di Tutor:**
- `tutor` → `tutor`
- `cotutor` → `co-tutor`
- `co-tutor` → `co-tutor`
- `tutor aziendale` → `tutor` (tutor aziendale)
- `cotutore` → `co-tutor`
- `cotutors` → `co-tutor`

**Variazioni di Relatore/Advisor:**
- `relatore` → `advisor`
- `relatrice` → `advisor` (forma femminile)
- `relatori` → `advisor` (plurale)
- `correlatore` → `co-advisor`
- `correlatrice` → `co-advisor`
- `coadvisor` → `co-advisor`
- `corelatore` → `co-advisor`

**Variazioni di Valutatore:**
- `valutatore` → `evaluator`
- `valutatrice` → `evaluator` (forma femminile)
- `valutatori` → `evaluator` (plurale)
- `valutatrici` → `evaluator` (plurale femminile)
- `evaluators` → `evaluator`
- `valutetori` → `evaluator` (errore di battitura)
- `valitatori` → `evaluator` (errore di battitura)

**Variazioni di Revisore:**
- `revisori` → `reviewer`
- `reviewers` → `reviewer`
- `reviwers` → `reviewer` (errore di battitura)

### Passo 3: Formato di Output e Assegnazione del Ruolo Predefinito

Dopo la normalizzazione, la struttura di ogni voce viene preservata e a tutti i nomi senza ruoli viene assegnato il ruolo predefinito `contributor`:

**Modello di Input 1 (Strutturato con ruoli):**
```
coordinatore: Romano Orrù; tutor: Paolo Savarese; co-tutor: Giovanni Franchi
```
**Dopo la Normalizzazione:**
```
coordinator: Romano Orrù; tutor: Paolo Savarese; co-tutor: Giovanni Franchi
```

**Modello di Input 2 (Solo nomi):**
```
Siciliano Velia; Benfenati Fabio
```
**Dopo la Normalizzazione:**
```
contributor: Siciliano Velia; contributor: Benfenati Fabio
```
(Il ruolo predefinito `contributor` viene assegnato a ciascun nome)

**Modello di Input 3 (Formato misto):**
```
Clini Paolo; Tutor Aziendale: Panzini Alessandra; Fatone Francesco
```
**Dopo la Normalizzazione:**
```
contributor: Clini Paolo; tutor: Panzini Alessandra; contributor: Fatone Francesco
```
(I nomi senza ruoli ricevono il ruolo predefinito `contributor`)

**Modello di Input 4 (Nome singolo):**
```
MAURIZIO RIPEPE
```
**Dopo la Normalizzazione:**
```
contributor: MAURIZIO RIPEPE
```
(Il nome singolo senza ruolo riceve il ruolo predefinito `contributor`)

---

## Esempi Dettagliati di Normalizzazione

### Esempio 1: Normalizzazione Completa dei Ruoli

**Voce Originale:**
```
coordinatrice: Paola Bellocchi; supervisore: Enzo Di Salvatore; valutatori: Marco Rossi
```

**Passaggi di Normalizzazione:**
1. Dividere per punto e virgola: `["coordinatrice: Paola Bellocchi", "supervisore: Enzo Di Salvatore", "valutatori: Marco Rossi"]`
2. Estrarre i ruoli: `["coordinatrice", "supervisore", "valutatori"]`
3. Normalizzare i ruoli:
   - `coordinatrice` → `coordinator`
   - `supervisore` → `supervisor`
   - `valutatori` → `evaluator`
4. Ricostruire la voce

**Voce Normalizzata:**
```
coordinator: Paola Bellocchi; supervisor: Enzo Di Salvatore; evaluator: Marco Rossi
```

### Esempio 2: Formato Misto con Errori di Battitura e Assegnazione del Ruolo Predefinito

**Voce Originale:**
```
Giovanni Bianchi; coordinatre: Maria Verdi; cotutor: Luca Neri
```

**Passaggi di Normalizzazione:**
1. Dividere per punto e virgola: `["Giovanni Bianchi", "coordinatre: Maria Verdi", "cotutor: Luca Neri"]`
2. Estrarre i ruoli dove presenti: `[null, "coordinatre", "cotutor"]`
3. Normalizzare i ruoli:
   - `null` → `contributor` (ruolo predefinito assegnato)
   - `coordinatre` → `coordinator` (correzione errore di battitura)
   - `cotutor` → `co-tutor`
4. Ricostruire la voce

**Voce Normalizzata:**
```
contributor: Giovanni Bianchi; coordinator: Maria Verdi; co-tutor: Luca Neri
```

### Esempio 3: Ruoli Multilingue

**Voce Originale:**
```
these dirigee par: Pierre Dubois; codirecteur de thèse: Marie Laurent
```

**Passaggi di Normalizzazione:**
1. Dividere per punto e virgola: `["these dirigee par: Pierre Dubois", "codirecteur de thèse: Marie Laurent"]`
2. Estrarre i ruoli: `["these dirigee par", "codirecteur de thèse"]`
3. Normalizzare i ruoli:
   - `these dirigee par` → `advisor` (francese: tesi diretta da)
   - `codirecteur de thèse` → `co-advisor` (francese: co-direttore di tesi)
4. Ricostruire la voce

**Voce Normalizzata:**
```
advisor: Pierre Dubois; co-advisor: Marie Laurent
```

### Esempio 4: Voce Complessa con Molteplici Tipi di Ruolo

**Voce Originale:**
```
coordinatore: Massimo Carlo Giannini; tutor: Francesca Fausta Gallo; co-tutor: Egidio Ivetic
```

**Passaggi di Normalizzazione:**
1. Dividere per punto e virgola: `["coordinatore: Massimo Carlo Giannini", "tutor: Francesca Fausta Gallo", "co-tutor: Egidio Ivetic"]`
2. Estrarre i ruoli: `["coordinatore", "tutor", "co-tutor"]`
3. Normalizzare i ruoli:
   - `coordinatore` → `coordinator`
   - `tutor` → `tutor`
   - `co-tutor` → `co-tutor` (già normalizzato)
4. Ricostruire la voce

**Voce Normalizzata:**
```
coordinator: Massimo Carlo Giannini; tutor: Francesca Fausta Gallo; co-tutor: Egidio Ivetic
```

### Esempio 5: Solo Nomi con Assegnazione del Ruolo Predefinito

**Voce Originale:**
```
Del Mastro Lucia; Quarto Rodolfo
```

**Passaggi di Normalizzazione:**
1. Dividere per punto e virgola: `["Del Mastro Lucia", "Quarto Rodolfo"]`
2. Estrarre i ruoli: `[null, null]`
3. Assegnare il ruolo predefinito:
   - `null` → `contributor` (ruolo predefinito assegnato al primo nome)
   - `null` → `contributor` (ruolo predefinito assegnato al secondo nome)
4. Ricostruire la voce

**Voce Normalizzata:**
```
contributor: Del Mastro Lucia; contributor: Quarto Rodolfo
```

### Esempio 6: Nome Singolo con Assegnazione del Ruolo Predefinito

**Voce Originale:**
```
Vigni Stefano
```

**Passaggi di Normalizzazione:**
1. Nessun punto e virgola presente, voce singola
2. Estrarre il ruolo: `null`
3. Assegnare il ruolo predefinito:
   - `null` → `contributor` (ruolo predefinito assegnato)
4. Ricostruire la voce

**Voce Normalizzata:**
```
contributor: Vigni Stefano
```

---

## Casi Speciali e Casi Limite

### Caso 1: Ruoli con Caratteri Speciali

Alcuni ruoli contengono caratteri speciali, trattini o punti:

- `co-supervisor` rimane `co-supervisor`
- `Ph.D. Coordinator` → `coordinator`
- `co-tutor` rimane `co-tutor`

### Caso 2: Ruoli Composti

Quando una singola voce contiene più ruoli per una persona:

**Originale:**
```
tutor: Clemencia Chaves-López; Ph.D. Coordinator: Mauro Serafini Dario Compagnone
```

**Normalizzato:**
```
tutor: Clemencia Chaves-López; coordinator: Mauro Serafini Dario Compagnone
```

### Caso 3: Sensibilità alle Maiuscole

La corrispondenza dei ruoli non è sensibile alle maiuscole:
- `COORDINATORE` → `coordinator`
- `Tutor` → `tutor`
- `supervisore` → `supervisor`

L'output normalizzato utilizza il minuscolo per i ruoli preservando le maiuscole originali per i nomi.

### Caso 4: Gestione degli Spazi Bianchi

Gli spazi bianchi extra vengono rimossi:
- `coordinatore : Maria Rossi` → `coordinator: Maria Rossi`
- `tutor:  Giovanni Bianchi` → `tutor: Giovanni Bianchi`

### Caso 5: Ruoli Sconosciuti o Non Mappati

Se un ruolo non viene trovato nel dizionario di mappatura CSV, rimane invariato con un flag per revisione manuale:
- `unknown_role: Name` → `unknown_role: Name` (segnalato per revisione)

Quando vengono identificati ruoli non mappati, possono essere aggiunti al file CSV con il loro ruolo normalizzato appropriato, e il dizionario può essere rigenerato per includere le nuove mappature.

---

## Database dei Ruoli (roles.txt) e Mappatura di Normalizzazione

Il processo di normalizzazione si basa su un database completo di variazioni di ruolo trovate in roles.txt. Questo file contiene 187 variazioni uniche di ruolo che comprendono:

- **Forme italiane:** coordinatore, coordinatrice, supervisore, tutor, relatore, valutatore
- **Forme inglesi:** coordinator, supervisor, tutor, advisor, evaluator, reviewer
- **Forme francesi:** dirigée, codirecteur, encadrants
- **Errori di battitura comuni:** coordinatre, reviwers, valutetori, superviors
- **Forme plurali e di genere:** coordinatori, valutatrici, supervisori
- **Forme composte:** co-supervisor, co-tutor, principal supervisor

Il database viene continuamente aggiornato man mano che nuove variazioni vengono scoperte nel dataset.

### Creazione del File di Mappatura CSV

Dal file roles.txt viene creato un file CSV per facilitare il processo di normalizzazione dei ruoli. Questo file CSV ha la seguente struttura:

**Struttura CSV:**
- **Colonna 1: `role`** - Contiene ogni variazione di ruolo come appare nei dati originali
- **Colonna 2: `normalized_role`** - Contiene il nome del ruolo standardizzato a cui la variazione dovrebbe essere mappata

**Esempio di contenuto CSV:**
```csv
role,normalized_role
coordinatore,coordinator
coordinatrice,coordinator
coordinatori,coordinator
coordinatre,coordinator
program coordinator,coordinator
tutor,tutor
cotutor,co-tutor
co-tutor,co-tutor
supervisore,supervisor
supervisor,supervisor
principal supervisor,principal supervisor
cosupervisore,co-supervisor
co-supervisor,co-supervisor
valutatore,evaluator
valutatrice,evaluator
relatore,advisor
correlatore,co-advisor
```

### Creazione e Utilizzo del Dizionario

La regola di normalizzazione utilizza questo file CSV come input per creare un dizionario (tabella di ricerca) che mappa ogni variazione di ruolo alla sua forma normalizzata. Il processo funziona come segue:

1. **Caricare il file CSV:** Leggere il file CSV contenente le mappature dei ruoli
2. **Creare il dizionario:** Costruire un dizionario chiave-valore dove:
   - **Chiave:** Variazione di ruolo originale (dalla colonna `role`)
   - **Valore:** Ruolo normalizzato (dalla colonna `normalized_role`)
3. **Applicare durante la normalizzazione:** Durante l'elaborazione delle voci dei contributori, cercare ogni ruolo estratto nel dizionario per trovare il suo equivalente normalizzato

**Esempio di Struttura del Dizionario:**
```python
role_mapping = {
    'coordinatore': 'coordinator',
    'coordinatrice': 'coordinator',
    'coordinatori': 'coordinator',
    'coordinatre': 'coordinator',
    'program coordinator': 'coordinator',
    'tutor': 'tutor',
    'cotutor': 'co-tutor',
    'co-tutor': 'co-tutor',
    'supervisore': 'supervisor',
    'supervisor': 'supervisor',
    # ... tutte le altre mappature
}
```

**Processo di Ricerca:**
Quando un ruolo viene estratto da una voce di contributore, la regola di normalizzazione:
1. Converte il ruolo in minuscolo per una corrispondenza non sensibile alle maiuscole
2. Cerca il ruolo nel dizionario
3. Restituisce il valore del ruolo normalizzato
4. Se il ruolo non viene trovato nel dizionario, rimane invariato (segnalato per revisione manuale)

---

## Casi Patologici e Limitazioni della Regola

Sebbene la regola di normalizzazione descritta in questo documento gestisca efficacemente la maggior parte delle voci dei contributori, ci sono diversi casi patologici trovati nel dataset completo che infrangono la semplice logica di parsing. Questi casi richiedono una gestione speciale o un intervento manuale.

### Panoramica dei Casi Patologici

Da un'analisi del dataset completo, sono state identificate 128 voci patologiche che non si conformano ai modelli attesi. Questi casi sono raggruppati nelle seguenti categorie:

1. **Informazioni Istituzionali Integrate** (83 casi) - Frequenza più alta
2. **Nomi Separati da Virgole per Singolo Ruolo** (23 casi)
3. **Nessun Ruolo Specificato** (19 casi)
4. **Parentesi Quadre Attorno ai Ruoli/Nomi** (17 casi)
5. **Informazioni su Commissione/Giuria** (14 casi)
6. **Metadati Descrittivi** (10 casi)
7. **Lingue Miste con Traduzione** (3 casi)
8. **Parentesi Angolari per Qualifiche** (1 caso)

### Categoria 1: Informazioni Istituzionali Integrate

**Problema:** Le affiliazioni istituzionali, i dipartimenti e i nomi delle università sono mescolati all'interno del campo contributors, rendendo difficile distinguere tra i nomi dei contributori e le informazioni organizzative.

**Esempio 1:**
```
ID 86736:
supervisor: Arti Ahluwalia, Giovanni Vozzi, Claudio Domenici; University Of Pisa Interdepartmental Research Center E. Piaggio
```

**Perché la regola fallisce:**
- Dopo il punto e virgola, "University Of Pisa..." appare come un nome senza ruolo
- La regola assegnerebbe: `contributor: University Of Pisa Interdepartmental Research Center E. Piaggio`
- Questo è errato poiché è un'istituzione, non una persona

**Esempio 2:**
```
ID 148610:
Centro interdipartimentale di ricerca per le scienze ambientali, Università degli studi di Bologna, Ravenna; tutore: Nadia Pinardi; Tutori Aggiunti: Marco Zavatarelli Michele Giani; coordinatore: Carlo Ferrari
```

**Perché la regola fallisce:**
- La voce inizia con informazioni istituzionali prima di qualsiasi coppia ruolo-nome
- La regola assegnerebbe: `contributor: Centro interdipartimentale di ricerca...`

### Categoria 2: Nomi Separati da Virgole per Singolo Ruolo

**Problema:** Più nomi di contributori sono elencati dopo un singolo ruolo, separati da virgole piuttosto che da punti e virgola con ruoli ripetuti.

**Esempio 1:**
```
ID 86736:
supervisor: Arti Ahluwalia, Giovanni Vozzi, Claudio Domenici
```

**Perché la regola fallisce:**
- La regola si aspetta il formato: `ruolo: nome` o `ruolo: nome; ruolo: nome`
- Qui abbiamo: `ruolo: nome1, nome2, nome3`
- La regola tratterebbe l'intero elenco separato da virgole come un singolo nome: `supervisor: Arti Ahluwalia, Giovanni Vozzi, Claudio Domenici`
- Questo è tecnicamente corretto ma non consente l'identificazione individuale dei supervisori

**Esempio 2:**
```
ID 137547:
Advisors: Paolo Dario Aldo Tucciarone
```

**Perché la regola fallisce:**
- Più nomi elencati senza separazione chiara (nessuna virgola o punto e virgola)
- La regola non può determinare se questa è una persona con più nomi o più persone

**Esempio 3:**
```
ID 168668:
Relatori: Pierugo Carbonin Jeffrey M. Isner
```

**Perché la regola fallisce:**
- Due nomi distinti senza separazione appropriata
- Ambiguo se questo è un nome o due relatori

### Categoria 3: Nessun Ruolo Specificato

**Problema:** Le voci contengono testo descrittivo, informazioni istituzionali o metadati ma nessun ruolo di contributore o nome nel formato atteso.

**Esempio 1:**
```
ID 150221:
Department Of Dermatology And Venereology University Of Rome Tor Vergata
```

**Perché la regola fallisce:**
- Nessun due punti presente, quindi nessun ruolo può essere estratto
- La regola assegnerebbe: `contributor: Department Of Dermatology...`
- Queste sono informazioni istituzionali, non un contributore

**Esempio 2:**
```
ID 149027:
coordinato da Pelio Fronzaroli
```

**Perché la regola fallisce:**
- Utilizza il linguaggio naturale "coordinato da" invece di "coordinatore:"
- La regola non può analizzare questo poiché non corrisponde al modello `ruolo: nome`

### Categoria 5: Informazioni su Commissione/Giuria

**Problema:** Le informazioni sulle commissioni d'esame, giurie o panel di valutazione sono incluse insieme alle informazioni sul supervisore.

**Esempio 1:**
```
ID 102547:
sostenue le 18 octobre 2010 devant la commission d'examen: Marcello Baldo (rapporteur); Eric Gourgoulhon (examinateur); Francesca Gulminelli (rapporteur); Elias Khan (directeur de thèse)...
```

**Perché la regola fallisce:**
- Inizia con metadati descrittivi ("sostenue le..." = discussa il...)
- Contiene termini simili ai ruoli tra parentesi: (rapporteur), (examinateur)
- I ruoli sono tra parentesi, non nel formato standard `ruolo: nome`

**Esempio 2:**
```
ID 5075:
Lettieri Gaetano; Valutatori esterni: G. Leghissa, M.C. Giorda. Membri commissione: S. Bancalari, R. Celada Ballanti, M. Valente; Betta Emanuele
```

**Perché la regola fallisce:**
- Utilizza nomi abbreviati (iniziali) per alcuni membri
- "Membri commissione:" (membri della commissione) è un ruolo di gruppo, non ruoli individuali
- Mescola nomi completi con nomi abbreviati

### Categoria 6: Metadati Descrittivi

**Problema:** Le voci contengono testo narrativo che descrive la difesa della tesi, la preparazione o altre informazioni contestuali.

**Esempio 1:**
```
ID 87619:
thèse dirigée par Venturi Ferriolo Massimo, soutenue à Milan, le 28/02/2011
```

**Perché la regola fallisce:**
- Contiene informazioni sulla difesa ("soutenue à Milan, le 28/02/2011" = discussa a Milano il...)
- Utilizza il linguaggio naturale "thèse dirigée par" (tesi diretta da) invece di `ruolo: nome`
- Informazioni su data e luogo mescolate

**Esempio 2:**
```
ID 88211:
a dissertation presented to the Faculty of Mathematical, Physical and Natural Sciences, University of Siena, in candidacy for the degree of doctor of philosophy, recommended for acceptance by the Department of Mathematics and Computer Science; adviser: Andrea Sorbi
```

**Perché la regola fallisce:**
- Lunga descrizione narrativa prima di qualsiasi coppia ruolo-nome
- La regola tenterebbe di assegnare il ruolo predefinito all'intero testo narrativo

---

### Riepilogo delle Limitazioni della Regola

La semplice regola di normalizzazione fallisce in questi casi patologici perché presuppone:

1. **Coppie ruolo-nome pulite:** Le voci seguono il formato `ruolo: nome` in modo coerente
2. **Separazione con punto e virgola:** Più contributori sono sempre separati da punti e virgola
3. **Singolo nome per ruolo:** Ogni designazione di ruolo è seguita da un singolo nome
4. **Nessun dato istituzionale:** Sono presenti solo nomi di persone e ruoli
5. **Nessun metadato:** Il testo descrittivo e le informazioni contestuali sono assenti
6. **Nessun carattere speciale:** Parentesi, parentesi e segni di uguale non vengono utilizzati
7. **Lingua singola:** Tutto il testo è in una lingua senza traduzioni

### Raccomandazioni

Per l'implementazione in produzione, questi casi patologici richiedono:

- **Pre-elaborazione:** Rilevare e segnalare le voci con parentesi, segni di uguale o parole chiave istituzionali
- **Revisione manuale:** Verifica umana per le voci che non corrispondono ai modelli attesi
- **Parsing migliorato:** Regole più sofisticate per gestire virgole, parentesi e contenuti misti
- **Riconoscimento delle entità:** Distinguere tra nomi di persone e nomi istituzionali
- **Gestione multilingue:** Analizzare le voci con marcatori di traduzione (` = `)

---

### Tabella Riepilogativa dei Casi Patologici

La seguente tabella mostra esempi rappresentativi di casi patologici e come verrebbero trattati (erroneamente) dalla regola di normalizzazione semplice:

| ID | Campo Contributors Originale | Come Verrebbe Trattato dalla Regola | Problema |
|----|------------------------------|--------------------------------------|----------|
| 86736 | `supervisor: Arti Ahluwalia, Giovanni Vozzi, Claudio Domenici; University Of Pisa Interdepartmental Research Center E. Piaggio` | `supervisor: Arti Ahluwalia, Giovanni Vozzi, Claudio Domenici; contributor: University Of Pisa Interdepartmental Research Center E. Piaggio` | Istituzione trattata come contributore; nomi multipli non separati |
| 140119 | `[coordinarore]: Carlo Gallina` | Potrebbe non essere riconosciuto o `[coordinarore]: Carlo Gallina` (ruolo non normalizzato) | Parentesi quadre interferiscono; errore di battitura nel ruolo |
| 150221 | `Department Of Dermatology And Venereology University Of Rome Tor Vergata` | `contributor: Department Of Dermatology And Venereology University Of Rome Tor Vergata` | Informazioni istituzionali trattate come nome di contributore |
| 149027 | `coordinato da Pelio Fronzaroli` | `contributor: coordinato da Pelio Fronzaroli` | Linguaggio naturale non analizzabile; intero testo trattato come nome |
| 102547 | `sostenue le 18 octobre 2010 devant la commission d'examen: Marcello Baldo (rapporteur); Eric Gourgoulhon (examinateur)...` | `sostenue le 18 octobre 2010 devant la commission d'examen: Marcello Baldo (rapporteur); contributor: Eric Gourgoulhon (examinateur)... [RUOLO NON PRESENTE]` | Metadati descrittivi e ruoli tra parentesi non analizzabili correttamente |
| 79158 | `thése dirigée par = tesi diretta da Johannes Bartuschat et = e Roberta Cella; preparée au sein du = preparato presso il GERCI...` | `contributor: thése dirigée par = tesi diretta da Johannes Bartuschat et e Roberta Cella; contributor: preparée au sein du = preparato presso il GERCI...` | assegnazione erronea del ruolo contributor |
| 87619 | `thèse dirigée par Venturi Ferriolo Massimo, soutenue à Milan, le 28/02/2011` | `contributor: thèse dirigée par Venturi Ferriolo Massimo, soutenue à Milan, le 28/02/2011` | Linguaggio naturale e metadati sulla difesa non analizzabili |
| 58864 | `Pranovi Fabio; Tonielli Renato; Bonanno Angelo <Ricercatore Cnr>` | `contributor: Pranovi Fabio; contributor: Tonielli Renato; contributor: Bonanno Angelo <Ricercatore Cnr>` | Qualifiche tra parentesi angolari non separate dal nome |
| 5075 | `Lettieri Gaetano; Valutatori esterni: G. Leghissa, M.C. Giorda. Membri commissione: S. Bancalari, R. Celada Ballanti, M. Valente; Betta Emanuele` | `Lettieri Gaetano; Valutatori esterni: G. Leghissa, M.C. Giorda. Membri commissione: S. Bancalari, R. Celada Ballanti, M. Valente; Betta Emanuele [RUOLO NON PRESENTE]` | Nomi abbreviati; ruolo di gruppo ("Membri commissione") non gestito; virgole e punti mescolati, sistema confuso dalla presenza di due ":" fra due ";" |
| 150524 | `[Coordinatore: Giuseppe Barbieri Carmen Andriani]; [relatore: Francesco Garofalo]; [Università degli studi G. D'Annunzio...]` | Parsing fallisce o tratta ogni sezione tra parentesi come singola unità | Parentesi quadre multiple; nomi multipli per ruolo; info istituzionali |
| 150524bis | `[Coordinatore: Giuseppe Barbieri Carmen Andriani]; [relatore: Francesco Garofalo]; [Università degli studi G. D'Annunzio...]` | TODO(tommaso): con una fase di preprocessing che elimina le parentesi quadre possiamo far funzionare la regola (rimane il problema che ci sarebbe il campo contributor: "Università degli studi G. D'Annunzio...) | Parentesi quadre multiple; nomi multipli per ruolo; info istituzionali |
| 88211 | `a dissertation presented to the Faculty of Mathematical, Physical and Natural Sciences, University of Siena, in candidacy for the degree of doctor of philosophy, recommended for acceptance by the Department of Mathematics and Computer Science; adviser: Andrea Sorbi` | `contributor: a dissertation presented to the Faculty of Mathematical, Physical and Natural Sciences, University of Siena, in candidacy for the degree of doctor of philosophy, recommended for acceptance by the Department of Mathematics and Computer Science; advisor: Andrea Sorbi` | Lunga descrizione narrativa trattata come nome di contributore |
| 137547 | `sede consorziarta: Laboratorio CRIM, Scuola superiore Sant'Anna, Pisa; candidate: Vittoria Raffa; Advisors: Paolo Dario Aldo Tucciarone` | `sede consorziata: Laboratorio CRIM, Scuola superiore Sant'Anna, Pisa; contributor: Vittoria Raffa (dopo normalizzazione di "candidate"); advisor: Paolo Dario Aldo Tucciarone` | nomi multipli senza separazione |
| 148610 | `Centro interdipartimentale di ricerca per le scienze ambientali, Università degli studi di Bologna, Ravenna; tutore: Nadia Pinardi; Tutori Aggiunti: Marco Zavatarelli Michele Giani; coordinatore: Carlo Ferrari` | `contributor: Centro interdipartimentale di ricerca per le scienze ambientali, Università degli studi di Bologna, Ravenna; tutor: Nadia Pinardi; contributor: Marco Zavatarelli Michele Giani (dopo normalizzazione di "Tutori Aggiunti"); coordinator: Carlo Ferrari` | Informazioni istituzionali all'inizio; nomi multipli per "Tutori Aggiunti" |
| 113236 | `Thèse Dirigée Par = Relatori Di Dottorato = Advisors: Buso Simone Ventura Laurent; Rapporteurs = Esaminatori = Examiners: Berthon Alain Kaer Sōren Knudsen` | `Thèse Dirigée Par = Relatori Di Dottorato = Advisors: Buso Simone Ventura Laurent; Rapporteurs = Esaminatori = Examiners: Berthon Alain Kaer Sōren Knudsen [RUOLO NON PRESENTE]`| formato completamente non standard |
| 168668 | `Relatori: Pierugo Carbonin Jeffrey M. Isner` | `advisor: Pierugo Carbonin Jeffrey M. Isner` | Due nomi trattati come un singolo nome; nessuna separazione chiara |

**Legenda della tabella:**
- **ID**: Identificativo della voce nel dataset
- **Campo Contributors Originale**: Il valore originale della colonna contributors
- **Come Verrebbe Trattato dalla Regola**: Il risultato della normalizzazione applicando la regola semplice
- **Problema**: Descrizione del motivo per cui il trattamento è errato o problematico

---

## Appendice: Tabella Completa di Mappatura dei Ruoli

| Variazioni di Ruolo Originali | Ruolo Normalizzato |
|-------------------------|-----------------|
| coordinatore, coordinatrice, coordinatori, coordinatre, program coordinator, ph.d. coordinator, cooordinator, coordimator, coordinater, coodinatore, ccordinatore, coocrdinatore, ccoordinatore, coordinatore del dottorato, coordinbatore, coordinartore, coordinetore, coordinbatore del dottorato, coordinbatore del ciclo, coordinarore, coordintatore, coiordinatore, coordiatore, coordiantore, coordinaorte | coordinator |
| tutor, cotutor, co-tutor, cotutore, cotutors, tutore, turtor, turore, turor, cotuture, tutordi percorso formativo | tutor / co-tutor |
| supervisore, supervisori, supervisor, supervisors, cosupervisore, co-supervisore, co-supervisor, principal supervisor, suprvisor, superviors, superisor, supevisors, superviosre, superviosre, supervisoe, supevisore, suprvisore, graduate supervisior | supervisor / co-supervisor |
| relatore, relatrice, relatori, realtore, reatore, relators | advisor |
| correlatore, correlatrice, corelatore, correlator, controrelatore, corelatori, coorrelatori | co-advisor |
| valutatore, valutatrice, valutatori, valutatrici, valutetori, valitatori, valotatori, valutatatori, valutatoti, evaluators, validatori | evaluator |
| revisori, reviewers, reviwers, revesore | reviewer |
| coadvisor, coadvisors, coadiutore, coadiutrice, adivisor, avisor, adivors | co-advisor |
| curatori, curatrice | curator |
| codirecteur, codirecteur de thèse, codirettore, codirettrice, codirector, condirettore, condirettori | co-director |
| these dirigee par, dirigée, dirigÃ©e, direcyeur de thèse, docente guida | advisor |
| examiners, esaminatrice, esaminatori | examiner |
| commentor, discussant | discussant |
| referenti, referÃ©e, internetional referees | referee |
| encadrants, berichter | supervisor |
| promotors | promoter |

---

## Cronologia delle Versioni

- **v1.0** (2024): Framework iniziale di normalizzazione dei ruoli
- Documento aggiornato a novembre 2025

---

## Contatti

Per domande sulla normalizzazione dei ruoli o per segnalare variazioni di ruolo non mappate, contattare il team di gestione dei dati.
