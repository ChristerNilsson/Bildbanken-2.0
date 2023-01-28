<script>

	import _ from "lodash"
	import countapi from 'countapi-js'
	import { tick } from 'svelte'
	import Card from "./Card.svelte"
	import Download from "./Download.svelte"
	import Help from "./Help.svelte"
	import NavigationVertical from "./NavigationVertical.svelte"
	import NavigationHorisontal from "./NavigationHorisontal.svelte"
	import Search from "./Search.svelte"
	import BigPicture from "./BigPicture.svelte"
	import Play from "./Play.svelte"
	import Infinite from "./Infinite.svelte"
	import fileIndex from './json/file_index.json'
	import data from './json/bilder.json'
	import {Home,invHome,images,selected} from './lib/stores.js'
	import {assert,comp2,log,spaceShip} from './lib/utils.js'

	log('Skapad: 2023-01-24 15:30')

	$: setHome(data)

	function setHome(data) {
		$Home = data
		$invHome = invertHome($Home)
		path = [$Home]
		stack = ["Home"]
	}

	countapi.visits(':HOST:',':PATHNAME:').then((result) => {console.log('countapi',result.value)})

	const range = _.range

	const MAX_DOWNLOAD = 1000

  let cards = [] // Varje bild tillsammans med tre rader text utgör ett Card.
	let y = 0 // Anger var scrollern befinner sig just nu.
	let ymax = 0 // Anger var senast laddade bild befinner sig.
	let offset = 0
	let state = 'NORMAL' // NORMAL, PICTURE or PLAY

	$: { // infinite scroll
		// Om y + skärmens dubbla höjd överstiger senaste bilds underkant läses 20 nya bilder in.
		if (y + 2 * screen.height > ymax) {
			const n = cards.length

			cards = cards.concat($images.slice(n, n + 20))

			const latest = _.last(cards)
			if (n > 0) {
				ymax = latest.y + $invHome[latest.md5].sh // y + h
			}
		}
	}

	// let selected = []
	let skala = 1

	const fileWrapper = [fileIndex]
	
	let count = 0
	
	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	const SCROLLBAR = 0 // 12+3+1
	const GAP = 1
	$: WIDTH = calcWidth(innerWidth)
	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	let path=[] // = [$Home] // used for navigation
	let stack=[] //= ["Home"]
	
	// let res=[]
	let stat={}
	let total=0
	let buttons = false

	let sokruta = ""
	let big = {md5:""}
	
	let text0 = ""
	let text1 = ""
	// let images = [] // bilder i nuvarande katalogträd som uppfyller sökorden.
	let visibleKeys = {}

	// innehåller de kataloger söksträngen finns i. T ex {"2022":7,"2021":3} Innehåller antal bilder
	// $: visibleKeys = getVisibleKeys(_.last(path),path.length)

	const is_jpg = (file) => file.endsWith('.jpg') || file.endsWith('.JPG')
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)
	const spreadWidth = (share,WIDTH) => Math.floor((WIDTH-2*GAP*(1/share+1))*share) - 2

	function expand(imagedata,path,filename) { // converts 7-element array to object with 9 properties
		const bild = {}

		// data from json file:
		bild.sw        = imagedata[0] // small width
		bild.sh        = imagedata[1] // small height
		bild.bs        = imagedata[2] // big size
		bild.bw        = imagedata[3] // big width
		bild.bh        = imagedata[4] // big height
		bild.md5       = imagedata[5] // unique id based om md5
		bild.timestamp = imagedata[6] // 2023-01-24 12:34:56

		// added properties:
		bild.path = path         // the folder names only
		bild.filename = filename // filename with extension .jpg

		return bild
	}

	function invertHome(h) {
		const ih = {}
		function recurse (node,path) {
			for (const key in node) {
				if (is_jpg(key)) {
					node[key] = expand(node[key],path,key)
					ih[node[key].md5] = node[key]
				} else {
					recurse(node[key],path + '/'  +key)
				}
			}
		}
		recurse(h,'')
		return ih
	}

	function calcWidth(innerWidth) {
		let n = Math.floor(innerWidth/475)
		return Math.floor((innerWidth-(n+1)*GAP-SCROLLBAR-0)/n)
	}

	function consumeFolder(folder) {
		console.log(folder)
		sokruta = ""
		stack = folder.split("/")
		path.length = 0 // clear
		path.push($Home)
		let pointer = $Home
		for (const key of stack.slice(1)) {
			console.log(key)
			pointer = pointer[key]
			path.push(pointer)
		}
		path = path
		stack = stack 
	}

$: consumeParameters($invHome)

	function consumeParameters(ih) {
		const queryString = window.location.search
		const urlParams = new URLSearchParams(queryString)
		if (urlParams.has("folder")) consumeFolder(urlParams.get("folder"))
		if (urlParams.has("query")) sokruta = urlParams.get("query")
		if (urlParams.has("ids")) {
			const ids = urlParams.get("ids").split('_')
			for (const md5 of ids) {
				$selected[md5] = true
				state = 'PLAY'
			}
		}
		if (urlParams.has("md5")) {
			visaBig(urlParams.get("md5"))
			state = 'PICTURE'
		}

	}

	$: [text0, text1, $images,visibleKeys] = search(_.last(path), sokruta, stack.join('/'), $Home)

	$: placera($images,visibleKeys,innerWidth)
	$: WIDTH = calcWidth(innerWidth)

	function resize() {
		cards = []
		ymax = 0
		WIDTH = calcWidth(innerWidth)
		placera($images,visibleKeys,innerWidth)
	}

	window.onresize = resize

	const f= (skala,left,x,width) => Math.round((1-skala) * (x-left))
	//           skala left x   width
	assert(  0,f(1.1,  200, 200,400))
	assert(-20,f(1.1,  200, 400,400))
	assert(-40,f(1.1,  200, 600,400))
	assert(  0,f(1.1,    0,   0,400))
	assert(-20,f(1.1,    0, 200,400))
	assert(-40,f(1.1,    0, 400,400))

	function getPath(path,dir="small") {
		if (dir.length > 0) path = path.replace("Home",dir)
		return path
	}

	function visaBig(md5) {
		document.body.style = "overflow:hidden"

		const ih = $invHome[md5]

		big.exifState = 0
		big.mouseState = 0

		big.bs = ih.bs
		big.bw = ih.bw
		big.bh = ih.bh

		big.skala = Math.min(innerHeight/big.bh, innerWidth/big.bw)
		big.width = big.bw * big.skala
		big.height = big.bh * big.skala
		big.left = (innerWidth-big.width)/2
		big.top = (innerHeight-big.height)/2

		big.md5 = md5
		big.path = ih.path
		big.filename = ih.filename
		big.timestamp = ih.timestamp
		big = big
	}

	function push(key) {
		if (!is_jpg(key)) {
			path.push(_.last(path)[key])
			stack.push(key)
			path = path
			stack = stack
		}
	}

	function pop() {
		path.pop()
		stack.pop()
		path = path
		stack = stack
	}

	// Gå igenom knapplistan, räkna antalet träffar.
	// function getVisibleKeys(node,level) {
		
	// 	const result = {}
	// 	// log('images.length',images.length,{level})
	// 	for (const image of images) {
	// 		const ih = $invHome[image.md5]
	// 		const arr = ih.path.split("/")
	// 		if (level >= arr.length) break
	// 		const key = arr[level]
	// 		result[key] ||= 0
	// 		result[key] += 1
	// 	}
	// 	log(result)
	// 	return result
	// }

	function search(node,words,path) {
		const result = []
		const visibleKeys = {}
 
		// rekursiv pga varierande djup i trädet
		function recursiveSearch (node,words,arrPath0,level) { // node är nuvarande katalog. words är de sökta orden
			// tick()
			// if (levels==0) return
			for (const key in node) {
				const arrPath1 = arrPath0.concat(key)
				if (is_jpg(key)) {
					// if (arrPath1.length<3) log({arrPath1})
					const accKey = arrPath1[level]
					visibleKeys[accKey] ||= 0
					visibleKeys[accKey] += 1
					total += 1
					let s = ''
					// const newpath = newPath.replaceAll(' ','_') 
					// Home/2022/ removed
					const sPath = arrPath1.slice(2).join('/').replaceAll(' ','_') // .toLowerCase()
					// log({sPath})
					for (const i in range(words.length)) {
						const word = words[i]
						if (word.length == 0) continue
						count += 1
						if (sPath.includes(word)) s += ALFABET[i] // slice(10)
					}
					if (s.length > 0 || words.length == 0) {
						result.push({md5:node[key].md5, letters:s,x:0,y:0})
						stat[s] = (stat[s] || 0) + 1
					}
				} else {
					recursiveSearch(node[key], words, arrPath1, level)
				}
			}
		}

		ymax = 0 // Viktigt! Annars syns inte nya bilder.
		cards = []
		count = 0

		words = words.length == 0 ? [] : words.split(" ")

		stat = {}
		total = 0

		const start = new Date()

		// const levels = 99
		const arr = path.split('/')
		// log({arr})
		recursiveSearch(node, words, arr, arr.length)
		// log({visibleKeys})

		function g(a,b) {
			const iha = $invHome[a.md5]
			const ihb = $invHome[b.md5]
			const al = a.letters
			const bl = b.letters
			return spaceShip(bl.length,al.length) || spaceShip(al,bl) || spaceShip(ihb.timestamp,iha.timestamp)
		}

		result.sort(g)

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		return [st.join(' '),`found ${antal} of ${total} images in ${new Date() - start} ms`,result,visibleKeys]
	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images,visibleKeys,innerWidth) {
		const rows = sokruta=="" ? 4 : 5
		let antal = rows + 1 + _.size(visibleKeys)
		if (stack.length==2) antal+=1
		if (stack.length!=2 && buttons) antal+=1

		offset = 34 * antal // 30 + 2 * margin=2

		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)

		const cols = [offset]
		for (const i in range(COLS)) cols.push(0)
		const textHeights = 43
		// log('placera',{images,innerWidth,rows,antal,offset,COLS,GAP,WIDTH})
		for (const i in range(images.length)) {
			// tick()
			const image = images[i]
			const ih = $invHome[image.md5]
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			image.x = (GAP + WIDTH)*index
			image.y = cols[index]
			image.index = i
			cols[index] += Math.round(WIDTH*ih.sh/ih.sw) + textHeights // h/w
		}
	}

	function countDirs(path) {
		let result = 0
		for (const name in path) {
			console.log('countDirs',name)
			if (! is_jpg(name)) {
				result += 1
			}
		}
		return result
	}

	function prettyFilename(path) { // Tag bort eventuella M och V-nummer
		let i = path.lastIndexOf('/')
		let s = path.slice(i+1)
		path = path.slice(0,i)

		if (s.startsWith('Vy-')) s = s.slice(1+s.indexOf('_'))
		if (s.startsWith('Vy-')) s = s.slice(1+s.indexOf(' '))

		const p = s.search(/\d{4}-\d{2}-\d{2}/)
		if (p >= 0) {
			const datum = s.slice(p,p+10)
			if (path.includes(datum)) s = s.slice(0,p-1)
		}
		s = s.replace('Pristagare ','')
		s = s.replace(/[kK]lass [A-Z]+/,'')

		s = s.replace('.jpg','')
		s = s.replace('.JPG','')
		s = s.replace(/_M\d+/,'')
		s = s.replace(/_V\d+/,'')
		s = s.replace(/_F\d+/,'')
		s = s.replaceAll('_',' ')
		return s
	}

</script>

<svelte:window bind:scrollY={y}/>

{#if state == 'NORMAL'}
	<Search bind:sokruta {text0} {text1} {stack} {WIDTH} {GAP} {spreadWidth} {path} {is_jpg} {pop} />
	<Download {WIDTH} {spreadWidth} {MAX_DOWNLOAD} {stack} {pop}/>
	<NavigationHorisontal {stack} {WIDTH} />
	<NavigationVertical bind:buttons {visibleKeys} {push} {is_jpg} {WIDTH} {spaceShip} {stack} />
	<Infinite {WIDTH} {cards} {round} {fileWrapper} {prettyFilename} />
{:else}
	{#if state == 'PICTURE'}
		<BigPicture {big} {prettyFilename} />
	{:else}
		<Play bind:state />
	{/if}
{/if}
