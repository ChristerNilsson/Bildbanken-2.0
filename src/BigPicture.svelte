<script>
	import _ from "lodash"
	import {log,prettyFilename,round} from './lib/utils.js'
	import {invHome} from './lib/stores.js'
	import { saveAs } from "file-saver"

	export let md5

	const INCR = 0.08
	let exif = null

	let big = makeBig($invHome[md5])
	let filename = big.filename
	let path = big.path.replaceAll("_"," ").replace('.jpg','').replaceAll("/",' • ')

	function makeBig(ih) {
		const skala = Math.min(innerHeight/ih.bh, innerWidth/ih.bw)
		const width = ih.bw * skala
		const height = ih.bh * skala
		return {
			md5: ih.md5,
			path: ih.path,
			filename: ih.filename,
			timestamp: ih.timestamp,
			bs: ih.bs,
			bw: ih.bw,
			bh: ih.bh,
			skala : skala,
			width : width,
			height : height,
			left : (innerWidth-width)/2,
			top : (innerHeight-height)/2,
			mouseState: 0,
			exifState: 0,
		}
	}

	function getExif() {
		const img = document.getElementById("picture")
		big.bw = img.naturalWidth
		big.bh = img.naturalHeight
		big.exifState = 1
		EXIF.getData(img, function() {
			exif = EXIF.getAllTags(this)
			if (exif.ExifVersion) {
				big.exifState = 2
			}
		})
	}

	window.onscroll = (e)=> {
		e.preventDefault()
		e.stopPropagation()
		return false 
	}

	function wheel(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()
		big.mouseState = 0
		const x = e.x // musens position
		const y = e.y
		const f = (skala,left,x) => (1-skala) * (x-left)
		let faktor = 1 + INCR
		if (e.deltaY > 0) faktor = 1/faktor
		big.left += f(faktor,big.left,x)
		big.top  += f(faktor,big.top,y)
		big.skala *= faktor
		big.width  = big.skala * big.bw
		big.height = big.skala * big.bh
		return false
	}

	function mousedown(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()
		big.mouseState = 1
		big.startX = e.x
		big.startY = e.y
	}

	function mousemove(e) {
		if (e.button==0 && big.mouseState==1) {
			big.left += e.x - big.startX
			big.top += e.y - big.startY
			big.startX = e.x
			big.startY = e.y
		} else {
			big.mousestate=0
		}
	}

	function mouseup(e) {big.mouseState = 0}
	function share () {navigator.clipboard.writeText(location.origin + location.pathname.replace('index.html','') + "Home/" + big.md5 + '.jpg')}
	function downloadOne() {saveAs("Home/" + big.md5 + ".jpg", big.filename)}
	document.onmousemove = mousemove
	document.title = prettyFilename(big.filename,false)

</script>

<button on:click={share}> Share </button>
<button on:click={downloadOne}> Download </button>

<span style="top:8%">{big.filename}</span>
<span style="top:12%">{path}</span>
<span style="top:20%"> {round(big.bw * big.bh/1024/1024,1)} MP • {big.bw} x {big.bh} • {round(big.bs/1024)} kB </span>
<span style="top:16%;"> {big.timestamp.replace(" "," • ")} </span>
{#if exif && exif.Model}
	<span style="top:24%;"> {exif.Model} • f/{exif.FNumber} • 1/{1/exif.ExposureTime} • {exif.FocalLength} mm • ISO {exif.ISOSpeedRatings} </span>
	<span style="top:28%;"> © {exif.Copyright} </span>
{/if}

<img 
	id='picture'
	src={"Home/" + big.md5 + ".jpg"}
	alt=""
	on:wheel={wheel}
	on:mousedown={mousedown}
	on:mouseup={mouseup}
	on:blur={blur}
	width = {big.width}
	style = "position:absolute; left:{big.left}px; top:{big.top}px;"
>

<style>
	button {
		margin:1%
	}
	span {
		position:absolute;
		left:1%;
	}
</style>

