# Aplikacija za automatsku obradu i organizaciju PDF dokumenata

Ova aplikacija omogućava automatsko skeniranje, organizaciju i preimenovanje PDF dokumenata temeljenih na prepoznatom tekstu unutar dokumenata.

## Glavne funkcionalnosti

### 1. **Automatsko preimenovanje PDF dokumenata**
- Aplikacija skenira tekst u PDF dokumentu i prepoznaje fraze poput "LIJEČNIČKA SVJEDODŽBA".
- Na temelju prepoznatog teksta, PDF dokument se automatski preimenuje u oblik: LIJEČNIČKA_SVJEDOŽBA - Ime_Prezime

### 2. **Organizacija dokumenata u direktorije**
- Na temelju prepoznatog tipa dokumenta, PDF dokument se automatski premješta u odgovarajući direktorij i poddirektorij.
Na primjer: Liječničke_svjedodžbe/Prezime/LIJEČNIČKA_SVJEDOŽBA - Ime_Prezime


### 3. **Prepoznavanje i ekstrakcija teksta iz slika ili PDF datoteka**
- Prepoznaje tekst sa slika ili PDF datoteka  i izdvaja ga za daljnju obradu u novu .txt datoteku.

### 4. **Pretvorba slika u skenirane PDF dokumente**
- Aplikacija omogućava pretvorbu slika (slike s dokumentima u sebi) u PDF format.
- Automatski prepoznaje dokument unutar slike, prilagođava perspektivu (ako je potrebno) i sprema rezultat u PDF format.

## Tehnologije
Aplikacija koristi sljedeće biblioteke i alate:
- **Tkinter** – za izradu grafičkog sučelja.
- **Pytesseract** – za ekstrakciju teksta iz PDF-ova i slika (OCR).
- **Pillow** – za manipulaciju slikama.
- **OpenCV** – za prepoznavanje i prilagodbu perspektive slika te obradu vizualnih elemenata.
- **NumPy** – za efikasno rukovanje matricama i obavljanje matematičkih operacija potrebnih za obradu slika.
- **math** – za izvođenje matematičkih izračuna potrebnih pri transformacijama i prilagodbama slika.
- **pdf2image** – za konverziju PDF dokumenata u slike kako bi se omogućila obrada njihovog sadržaja.
- **Regularni izrazi** – za identifikaciju i prepoznavanje tipa dokumenta temeljenog na tekstu.

## Demo
  ### 1. **Skeniranje slike u PDF dokument** 
   ![Skeniranje slike u pdf dokument](https://github.com/user-attachments/assets/e765e358-93f4-492e-9ed8-018ec04aee34)


  ### 2. **Pretvorba sadržaja slike ili pdf-a u tekst**
  ![Pretvorba slike u tekst](https://github.com/user-attachments/assets/6bc40a2d-71e0-4ce1-af75-cf474fca3460)

  ### 3. **Automatsko preimenovanje i premještanje pdf-a s obzirom na njegov sadržaj**
  ![Premještanje i preimenovanje](https://github.com/user-attachments/assets/0f75d74d-d1d3-4667-8a59-429ba2994660)


