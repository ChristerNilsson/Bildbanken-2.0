<script>
	import _ from "lodash"
	import {log} from "./lib/utils.js"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"
	import {Home,invHome,images,selected} from './lib/stores.js' // object with md5 as keys

	export let WIDTH
	export let spreadWidth
	export let MAX_DOWNLOAD

	function countSelection(selected,invHome) {
		let count = 0
		for (const key in selected) {
			if (selected[key]) count+=1
		}
		return count
	}

	$: n = countSelection($selected,$invHome)

	function download(item) { return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)}) }
	let zip = null

	function all() { // in this folder
		for (const image of $images) $selected[image.md5] = true
		$selected=$selected
	}
	function none() { // in this folder
		for (const image of $images) $selected[image.md5] = false
		$selected=$selected
	}
	function zero() { 
		$selected = {}
	}

	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const key of _.keys($selected).slice(0,MAX_DOWNLOAD)) {
			const sel = $selected[key]
			if (!sel) continue
			let path = $invHome[key].path + '/' + $invHome[key].filename
			path = path.replaceAll('/','__') // Flat fil önskad av Hedlund
			fileArr.push({name:path, url:"Home/" + key + ".jpg"})
		}
		n = fileArr.length
		if (n == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, `Bildbanken ${fileArr.length} .zip`) })})
			.catch((err) => {console.log(err)})
	}

	function play() {
		const host = location.origin + location.pathname
		const ids = _.filter(_.keys($selected), (key) => $selected[key]).slice(0,MAX_DOWNLOAD).join('|')
		log("ids",ids)
		if (ids.length == 0) return
		window.open(host + "?ids=" + ids)
	}

</script>

<div style="width:{WIDTH}px; height:34px">

	<button title="Unselect images in the current folder" style="left:{0.0*WIDTH}px; width:{spreadWidth(0.2,WIDTH)}px" on:click = {none}>       Del</button>
	<button title="Unselect all images" style="left:{0.2*WIDTH}px; width:{spreadWidth(0.2,WIDTH)}px; background-color:white" on:click = {zero}  >{n}</button>
	<button title="Select images in the current folder" style="left:{0.4*WIDTH}px; width:{spreadWidth(0.2,WIDTH)}px" on:click = {all}>        Add</button>
	<button title="Show selected images in a slide show" style="left:{0.6*WIDTH}px; width:{spreadWidth(0.2,WIDTH)}px" on:click = {play} >      Play</button>
	<button title="Download selected images" style="left:{0.8*WIDTH}px; width:{spreadWidth(0.2,WIDTH)}px" on:click = {downloadAll}>Download</button>

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
