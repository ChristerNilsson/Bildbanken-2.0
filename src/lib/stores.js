import {writable} from 'svelte/store'
// export let stack = writable([])
export let    Home  = writable({}) // json-strukturen
export let invHome  = writable({}) // objekt med md5 som nyckel.
export let images   = writable([]) // lista över framsökta md5.
export let selected = writable({}) // true or false
