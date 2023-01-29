# Bildbanken 2

## Introduktion

Denna databas innehåller drygt 45.000 fotografier från den svenska schackvärlden, tagna av Lars OA Hedlund, sedan 2011.  
När du startar ser du alla bilder, med de senaste högst upp.  
Du kan avgränsa sökandet på två sätt:

1. Genom att välja katalog. Hierarkin ser ut ungefär så här:
	* Home
		* År
			* Turnering/Event
				* Klass
					* Grupp

2. Genom att skriva in ett eller flera ord i sökrutan längst upp.  
	Skriver du flera ord, kommer bilderna högre upp ju fler träffar orden får.  
	(Man kan säga att **och** kommer före **eller**)

	* **Clear** rensar sökrutan
	* **Share** kopierar aktuell URL till klippbordet
	* **Help** visar denna sida
	* **Up** går till närmast högre liggande katalog
	* **None** avmarkerar alla bilder i denna utsökning
	* **All** markerar alla bilder i denna utsökning
	* **Play** Visar ett bildspel med utsökta bilder
	* **Download** hämtar alla markerade bilder i en zipfil
	* Home = aktuell katalog. Här ser du alla bilder
	* **Date** sorterar på datum, fallande
	* **Event** sorterar på event, stigande
	* **2022 (4936)** visar de 4936 bilder som tagits detta år
	* Klicka på en bild om du vill se högre upplösning
		* Nu kan du zooma (med mushjulet) och panorera (hasa med musen)
		* Bakom bilden finns tekniska data
			* T ex bländare, exponeringstid, objektiv, fotograf, tidpunkt

## Sökning

Sökning genomförs genom att fylla i sökrutan.  
Dessa ord, avgränsade av blanktecken, matchas mot texterna i kataloger och filnamn  
De kombineras automatiskt med **och** och **eller**  
Underscore (_) kan användas för att binda ihop ord, t ex *Numa_Karlsson*  

Sökningen är känslig för VERSALER och gemener.
De ord man anger kan vara delord, även enstaka tecken, och de kan stå var som helst i orden. T ex kommer "sson" att matcha ett antal Karlsson och Nilsson  

Tom söksträng innebär att alla bilder matchar.

Sökning går endast mot den katalog man valt. Välj Home om du vill söka i alla kataloger.

## Exempel

![Example](help.jpg)

Först gjordes ett urval genom att klicka på 2022.  
Då reducerades antalet bilder till 6317.  

Därefter skrevs söktexten "Anna Cramling" in.  
Det reducerade antalet bilder till 328.  
Sökningen tog 12 millisekunder.

Bara de bilder som gett träff på Anna eller Cramling, visas.

Kolumnnamnen [Date] och [Event] sorterar framsökta rader.

AB:10 innebär att båda orden förekom i 10 bilder.  
A:24 innebär att enbart Anna förekom i ytterligare 24 bilder.  
B:294 innebär att enbart Cramling förekom i 294 bilder (troligen Pia eller Dan Cramling).  
Notera att 10 + 24 + 294 = 328.

* 0 = första framsökta bilden
* AB innebär att båda orden förekommer i bildtexten
* Kryssrutan används vid Download
* Invite kan man klicka på. Då får man se inbjudan
* Result kan man klicka på. Då får man se turneringsresultatet
* Bilden har tagits av Lars OA Hedlund
* 2048 x 1194 = bredd och höjd
* 1508 kb = bildens storlek i kilobytes

Man kan se alla 328 bilderna genom att skrolla nedåt.  
Vill man avgränsa sig kan man t ex söka på Anna_Cramling eller klicka på Schack-SM Uppsala. 

Klickar man på [Up] får man se alla år och kan då klicka på 2011 för att se hur Anna såg ut då.

Klicka på en bild för att se den i högsta upplösningen.

## Bildspel

* Markera de bilder du vill visa. Samma hantering som vid Download
* Klicka på **Play**. Ny flik skapas
* Maximera bilden med **F11**
* Pausa med **mellanslag**
* Gå framåt med **pil höger**
* Gå bakåt med **pil vänster**
* Minska hastigheten med **pil upp**
* Öka hastigheten med **pil ner**
* Avsluta genom att stänga fliken
* Maximalt 1000 bilder kan visas i Chrome eller Safari.
	* [Microsoft Edge](https://www.geeksforgeeks.org/maximum-length-of-a-url-in-different-browsers/) klarar bara 60 bilder.
