import {writable} from 'svelte/store'

export let Home          = writable({}) // json-strukturen. Objekt i objekt. Pekar på utökad lista
export let invHome       = writable({}) // objekt med md5 som nyckel. Pekar på utökad lista, gemensam med Home
export let images        = writable([]) // lista över framsökta md5 i aktuell folder.
export let selected      = writable({}) // Objekt nycklad med md5. True eller false. Kopplad till checkbox.
export let fileIndex     = writable({}) // Mappar index till filer/urlar som används vid länkning.
export let settings      = writable({case:false, all:false})

	// $Home, ursprungliga listan med sju element, skapad av Pythonkoden:
	// {[sw,sh,bs,bw,bh,md5,timestamp]}
	// 0 sw Small Width i pixlar
	// 1 sh Small Height i pixlar
	// 2 bs Big Size i pixlar
	// 3 bw Big Width i pixlar
	// 4 bh Big Height i pixlar
	// 5 md5 32 hexadecimala tecken  (0123456789abcdef0123456789abcdef)
	// 6 timestamp '2023-01-24 12:34:00' Anger när bilden togs

	// $Home (objekt), listan utökad till nio element och omvandlad till objekt.
	// {md5:{sw,sh,bs,bw,bh,md5,timestamp,path,filename}}

	// $images Innehåller de utvalda bilderna. Aktuell katalog + träff på söksträng
	// [{letters,x,y,md5}]
	// .letters t ex AB A B osv från sökningen. A motsvarar första ordet, B andra.
	// .x (swimlane position in pixels)
	// .y
	// (.index (visas i card))

	// $selected
	// {md5 : true/false} Bunden till checkbox