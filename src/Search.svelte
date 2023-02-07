<script>
	import { saveAs } from 'file-saver'
	import { log } from './lib/utils.js'
	import { settings } from './lib/stores.js'

	import _ from 'lodash'

	export let sokruta
	export let text0
	export let text1
	export let stack
	export let WIDTH
	export let GAP
	export let spreadWidth
	export let pop

	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
	}

	function share () {
		const q1 = stack.length <= 1 ? "" : "folder=" + stack.join("/") 
		const q2 = sokruta == "" ? "" : "query=" + sokruta		
		const q = q1=="" && q2=="" ? "" : "?"
		const a = q1!="" && q2!="" ? "&" : ""
		navigator.clipboard.writeText(location.origin + location.pathname + q + q1 + a + q2)
	}

	// let hash = {}
	// const letters = "+!§()0123456789_,.-¤"
	// const stoppord = []
	// $rowsSearch = ((sokruta.split(" ").length <= 3) && (sokruta.length > 0)) ? 5 : 4

	// function flatWords(node) {
	// 	for (const key of _.keys(node)) {
	// 		let words = key
	// 		for (const letter of letters) {
	// 			words = words.replaceAll(letter," ")
	// 		}
	// 		for (const word of words.split(' ')) {
	// 			const wordLower = word.toLowerCase()
	// 			if (word.length > 1 && wordLower == word) {
	// 				hash[word] = word in hash ? hash[word]+1 : 1
	// 			}
	// 		}
	// 		if (! is_jpg(key)) flatWords(node[key])
	// 	}
	// }

	// function convert(hash) {
	// 	let arr = []
	// 	for (const key of _.keys(hash)) {
	// 		if (! stoppord.includes(key)) {
	// 			arr.push([key,hash[key]])
	// 		}
	// 	}
	// 	arr.sort()
	// 	return arr
	// }

	// function keywords() {
	// 	hash = {}
	// 	flatWords(_.last(path))
	// 	const keys = convert(hash)
	// 	const res = []
	// 	for (const [key,antal] of keys) res.push(key + ': ' + antal)
	// 	const blob = new Blob([res.join("\n")], {type: "text/plain;charset=utf-8;"})
	// 	saveAs(blob, `${_.last(stack)}_${res.length}_keywords.txt`)
	// }

	function help() {
		window.open("https://github.com/ChristerNilsson/2022-014-Bildbanken2#readme")
	}

	function keydown(event) {
		if (event.key == "Enter") {
			if (sokruta.startsWith('@')) {
				event.preventDefault()
				event.stopPropagation()
				const cmd = sokruta.substring(1)
				let success= true
				// if (cmd == 'CT') {
				// 	$settings.case = true
				// } else if (cmd == 'CF') {
				// 	$settings.case = false
				// } else if (cmd == 'SB') {
				// 	$settings.all = false // beginning
				// } else if (cmd == 'SA') {
				// 	$settings.all = true // anywhere
				// } else {
				// 	success = false
				// 	log('Unknown command: ' + cmd)
				// }
				// if (success) {
				// 	sokruta = ""
				// 	document.getElementById("search").focus()
				// }
			}
		}
	}

</script>

<input autocomplete="off" id="search" bind:value={sokruta} placeholder='Search' style="width:{WIDTH-2*GAP}px" on:keydown={keydown}>
<div class="center" style="width:{WIDTH}px">
	{text1}
</div>

<div style="width:{WIDTH}px; height:34px">
	{#if _.last(stack) == "Home"}
		<button title="This is Home folder" style="left:0px;width:{spreadWidth(1/5,WIDTH)}px" on:click = {pop} disabled >Up</button>
	{:else}
		<button title="Go to parent folder" style="left:0px;width:{spreadWidth(1/5,WIDTH)}px" on:click = {pop} >Up</button>
	{/if}
	<button title="Clear Search Text" on:click={clear} style="left:{1*WIDTH/5}px; width:{spreadWidth(1/5,WIDTH)}px">Clear</button>

	<div style="position:absolute; left:{2*WIDTH/5+40}px; top:70px">Case</div>
	<input class="largerCheckbox" type="checkbox" style="left:{2*WIDTH/5+20}px; top:70px" bind:checked={$settings.case} />
	<div style="position:absolute; left:{2*WIDTH/5+40}px; top:85px">All</div>
	<input class="largerCheckbox" type="checkbox" style="left:{2*WIDTH/5+20}px; top:85px" bind:checked={$settings.all}  />

	<button title="Save the URL on the clipboard" on:click={share} style="left:{3*WIDTH/5}px; width:{spreadWidth(1/5,WIDTH)}px">Share</button>
	<button title="View Help Page" on:click={help} style="left:{4*WIDTH/5}px; width:{spreadWidth(1/5,WIDTH)}px">Help</button>
</div>

<div class="center" style="width:{WIDTH}px">
	{text0.startsWith(':') ? '' : text0}
</div>

<style>
	input.largerCheckbox {
		position:absolute;
		width: 12px;
		height: 12px;
	}
	.center {
		margin-top:7px;
		text-align:center;
		height:27px
	}
	div {
		margin:0px;
	}
	button {
		position:absolute;
		margin:2px;
		height:30px;
	}
	input {
		margin:2px;
		height:30px;
	}
	::placeholder {
		color: lightgray;
		opacity: 1;
	} 
</style>
