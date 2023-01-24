import {writable} from 'svelte/store'

export let    Home  = writable({}) // json-strukturen. Objekt i objekt. Pekar på utökad lista
export let invHome  = writable({}) // objekt med md5 som nyckel. Pekar på utökad lista, gemensam med Home
export let images   = writable([]) // lista över framsökta md5 i aktuell folder.
export let selected = writable({}) // Objekt nycklad med md5. True eller false. Kopplad till checkbox.

	// $Home, ursprungliga listan med sex element:
	// {[sw,sh,bs,bw,bh,md5]}
	// 0 sw Small Width
	// 1 sh Small Height
	// 2 bs Big Size
	// 3 bw Big Width
	// 4 bh Big Height
	// 5 md5 32 hexadecimala tecken

	// $Home (objekt), listan utökad till åtta element och omvandlad till objekt.
	// {md5:{sw,sh,bs,bw,bh,md5,path,filename}}

	// $images
	// [{letters,timestamp,x,y,md5}]
	// .letters t ex AB A B osv
	// .timestamp tidpunkt när bilden togs. "yyyy-mm-dd hh:mm:ss"
	// .x (swimlane position)
	// .y
	// (.index (visas i card))

	// $selected
	// {md5 : true/false}