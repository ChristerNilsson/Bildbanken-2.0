<script>
	import { saveAs } from 'file-saver'
	import {log} from './lib/utils.js'
	import _ from 'lodash'

	export let sokruta
	export let text0
	export let text1
	export let stack
	export let WIDTH
	export let GAP
	export let spreadWidth
	export let path
	export let is_jpg
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

	let hash = {}
	const letters = "+!§()0123456789_,.-¤"
	const stoppord = []
	// $rowsSearch = ((sokruta.split(" ").length <= 3) && (sokruta.length > 0)) ? 5 : 4

	function flatWords(node) {
		for (const key of _.keys(node)) {
			let words = key
			for (const letter of letters) {
				words = words.replaceAll(letter," ")
			}
			for (const word of words.split(' ')) {
				const wordLower = word.toLowerCase()
				if (word.length > 1 && wordLower == word) {
					hash[word] = word in hash ? hash[word]+1 : 1
				}
			}
			if (! is_jpg(key)) flatWords(node[key])
		}
	}

	function convert(hash) {
		let arr = []
		for (const key of _.keys(hash)) {
			if (! stoppord.includes(key)) {
				arr.push([key,hash[key]])
			}
		}
		arr.sort()
		return arr
	}

	function keywords() {
		hash = {}
		flatWords(_.last(path))
		const keys = convert(hash)
		const res = []
		for (const [key,antal] of keys) res.push(key + ': ' + antal)
		const blob = new Blob([res.join("\n")], {type: "text/plain;charset=utf-8;"})
		saveAs(blob, `${_.last(stack)}_${res.length}_keywords.txt`)
	}

	function help() {
		window.open("https://github.com/ChristerNilsson/2022-014-Bildbanken2#readme")
	}

</script>

<input autocomplete="off" id="search" bind:value={sokruta} placeholder='Search' style="width:{WIDTH-2*GAP}px">
<div class="center" style="width:{WIDTH}px">
	{text1}
</div>

<div style="width:{WIDTH}px; height:34px">
	{#if _.last(stack) == "Home"}
		<button style="left:0px;width:{spreadWidth(1/4,WIDTH)}px" on:click = {pop} disabled >Up</button>
	{:else}
		<button style="left:0px;width:{spreadWidth(1/4,WIDTH)}px" on:click = {pop} >Up</button>
	{/if}
	<button on:click={clear} style="left:{1*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Clear</button>
	<button on:click={share} style="left:{2*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Share</button>
	<button on:click={help}  style="left:{3*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Help</button>
</div>

<div class="center" style="width:{WIDTH}px">
	{text0.startsWith(':') ? '' : text0}
</div>

<style>
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
