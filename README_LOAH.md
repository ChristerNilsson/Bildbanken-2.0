### Detta har redan gjorts av Christer

* Google Cloud Control Panel
  * create bucket "bildbank2"
* se till att bildbank2 är publik, mha Google Cloud Control Panel

### Detta görs om installation ska ske på annan dator

* installera Python 3.11.4 (hamnar på C:\Users\Lars OA Hedlund\AppData\Local\Programs\Python\Python311\python.exe)
* pip install pillow       (hamnar på C:\Users\Lars OA Hedlund\AppData\Local\Programs\Python\Python311\)
* download gsutil          (hamnar på C:\Program Files (x86)\Google\Cloud SDK)

### Detta görs vid varje uppdatering

* steg 1 (uppdaterar bilder.json)
  * ställ dig i katalogen D:\2022-014-Bildbanken2
  * python python\bilderflat.py
  * Svara Y om allt ser ok ut
  
* steg 2 (kopierar nya och ändrade filer till Google Cloud Storage)
  * Start Google Cloud SDK Shell
  * gsutil -m rsync -d -r D:\2022-014-Bildbanken2\public gs://bildbank2

* starta bildbanken med
  * https://storage.googleapis.com/bildbank2/index.html
