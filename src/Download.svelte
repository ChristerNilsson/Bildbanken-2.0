<script>
	import _ from "lodash"
	import {log} from "./lib/utils.js"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"
	import {Home,invHome} from './lib/stores.js' // object with md5 as keys

	// export let selected

	export let images
	export let WIDTH
	export let spreadWidth
	export let MAX_DOWNLOAD
	export let stack
	export let pop

	function countSelection(invHome) {
		let count = 0 
		for (const key in invHome) {
			if (invHome[key][6]) count+=1
		}
		return count
	}

	$: n = countSelection($invHome)

	$: log(n)

	// function make(value) { selected = _.map(images, () => value) }

	function download(item) { return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)}) }

	let zip = null

	function all() { // in this folder
		for (const image of images) $invHome[image[13]][6] = true
		$invHome = $invHome
	}
	function none() { // in this folder
		for (const image of images) $invHome[image[13]][6] = false
		$invHome = $invHome
	}

	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const key in $invHome) {
			const sel = $invHome[key]
			if (sel[6] == false) continue
			let path = "TODO!" //sel[2] + "\\" + sel[12]
			path = path.replaceAll('\\','__') // Flat fil önskad av Hedlund
			fileArr.push({name:path, url:"Home\\" + sel[5] + ".jpg"})
		}
		n = fileArr.length
		if (fileArr.length == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, `Bildbanken ${fileArr.length} .zip`) })})
			.catch((err) => {console.log(err)})
	}

</script>

<div style="width:{WIDTH}px; height:34px">

	{#if _.last(stack) == "Home"}
		<button style="left:0px;          width:{spreadWidth(0.17,WIDTH)}px" on:click = {pop} disabled >Up</button>
	{:else}
		<button style="left:0px;          width:{spreadWidth(0.17,WIDTH)}px" on:click = {pop} >Up</button>
	{/if}

	<button style="left:{0.17*WIDTH}px; width:{spreadWidth(0.16,WIDTH)}px" on:click = {none}>None</button>
	<button style="left:{0.33*WIDTH}px; width:{spreadWidth(0.52,WIDTH)}px" on:click = {downloadAll}>Download {n} image(s)</button>
	<button style="left:{0.85*WIDTH}px; width:{spreadWidth(0.15,WIDTH)}px" on:click = {all}>All</button>
</div>

<style>
	button {
		position:absolute;
		height:30px;
		margin:2px;
	}
	div {
		margin:0px
	}
</style>
