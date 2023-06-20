cd "C:\Program Files (x86)\Google\Cloud SDK"
SET PATH=C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin;%PATH%;
gsutil -m rsync -d -r D:\2022-014-Bildbanken2\public gs://bildbank2
pause
