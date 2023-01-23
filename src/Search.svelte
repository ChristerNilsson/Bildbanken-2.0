<script>
	import { saveAs } from 'file-saver'
	import {selected} from './lib/stores.js'
	import {log} from './lib/utils.js'

	export let sokruta
	export let text0
	export let text1
	export let stack
	export let WIDTH
	export let GAP
	export let spreadWidth
	export let path
	export let _
	export let is_jpg
	export let state

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

	function play() {
		log($selected)
		if (_.size($selected) > 0) state = 'PLAY'
		// window.open("/play/?ids=0a0bd65aef49942c7fad7560b4bb4b91_fff86a56ee65ec30a8e7feca0a9c04f2")
	}

	function help() {
		window.open("https://github.com/ChristerNilsson/2022-014-Bildbanken2#readme")
	}

	// window.onload = () => document.getElementById("search").focus()

</script>

<input autocomplete="off" id="search" bind:value={sokruta} placeholder='Search' style="width:{WIDTH-2*GAP}px">
<div class="center" style="width:{WIDTH}px">
	{text1}
</div>

<div style="width:{WIDTH}px; height:34px">
	<button on:click={clear}       style="left:{0}px;         width:{spreadWidth(1/4,WIDTH)}px">Clear</button>
	<button on:click={share}       style="left:{WIDTH/4}px;   width:{spreadWidth(1/4,WIDTH)}px">Share</button>
	<button on:click={play}        style="left:{2*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Play</button>
	<button on:click={help}        style="left:{3*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Help</button>
	<!-- <button on:click={keywords}    style="left:{2*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Keywords</button> -->
</div>

{#if (sokruta.split(" ").length <= 3) && (sokruta.length > 0)}
	<div class="center" style="width:{WIDTH}px">
		{text0}
	</div>
{/if}

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
