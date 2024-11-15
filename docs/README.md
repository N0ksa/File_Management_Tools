# Upute za korištenje aplikacije

## 1. Instalacija Tesseract OCR

Za početak, potrebno je instalirati Tesseract OCR na svoj sustav.

- Preuzmite instalacijski paket za Tesseract OCR s [službene stranice](https://tesseract-ocr.github.io/tessdoc/Installation.html).
- Slijedite upute za instalaciju ovisno o operativnom sustavu koji koristite.

Ako prilikom instalacije ne odaberete zadani put za instalaciju, bit će potrebno ručno navesti put do `tesseract.exe` datoteke u konfiguracijskoj datoteci aplikacije.

## 2. Postavljanje putanje do Tesseract-a u `config.py`

* Ako niste koristili zadanu putanju za instalaciju Tesseract OCR-a, trebate specificirati ispravan put u konfiguracijskoj datoteci `config.py`.

* Trenutno je postavljena putanja na:  
`C:\Program Files\Tesseract-OCR\tesseract.exe`

* Ako je Tesseract instaliran na drugačijoj lokaciji, otvorite `config.py` i promijenite putanju do odgovarajuće lokacije

## 3. Skidanje trening podataka za jezike
* Zatim je potrebo skinuti trening podatke za one jezike koji su specificirani u projektu sa stranice https://tesseract-ocr.github.io/tessdoc/Data-Files i dodati ih u `C:\Program Files\Tesseract-OCR\tessdata`


## 4. Instalacija i postavljanje Poppler-a na Windows
Za pravilno korištenje aplikacije koja obrađuje PDF datoteke, potrebno je instalirati Poppler na svoj sustav.

* Preuzmite Poppler sa [službene GitHub stranice](https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0), raspakirajte ga i postavite u direktorij koji želite (npr. `C:\poppler-24.08.0`).
* Zatim dodajte taj direktorij u PATH:
  1. Desnim klikom na **This PC** ili **Computer** na desktopu ili u File Exploreru, odaberite **Properties**.
  2. Kliknite na **Advanced system settings** na lijevoj strani.
  3. U prozoru **System Properties**, kliknite na **Environment Variables**.
  4. U prozoru **Environment Variables**, pod "System variables", pronađite varijablu **Path** i kliknite **Edit**.
  5. Kliknite **New** i unesite putanju do `bin` mape unutar Poppler direktorija. Ako ste raspakirali Poppler u `C:\poppler-24.08.0`, unesite:
     ```
     C:\poppler-24.08.0\Library\bin
     ```
  6. Kliknite **OK** za spremanje svih promjena.