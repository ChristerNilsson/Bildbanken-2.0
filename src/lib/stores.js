import {writable} from 'svelte/store'

export let    Home  = writable({}) // json-strukturen. Objekt i objekt. Pekar på utökad lista
export let invHome  = writable({}) // objekt med md5 som nyckel. Pekar på utökad lista, gemensam med Home
export let images   = writable([]) // lista över framsökta md5 i aktuell folder.
export let selected = writable({}) // Objekt nycklad med md5. True eller false. Kopplad till checkbox.

	// json (array), ursprungliga listan med sex element:
	// 0 sw Small Width
	// 1 sh Small Height
	// 2 bs Big Size
	// 3 bw Big Width
	// 4 bh Big Height
	// 5 md5 32 hexadecimala tecken

	// Expanderad json (objekt), listan utökad till 13 element och omvandlad till objekt.
	// .sw
	// .sh
	// .bs
	// .bw
	// .bh
	// .md5 (t ex 0123456789abcdef0123456789abcdef)

	// .letterCount A => 1, AB => 2 osv
	// .letters t ex AB A B osv
	// .path
	// .filename
	// .x (swimlane)
	// .y
	// .index (visas i card)