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
	import {Home,invHome,images,selected} from './lib/stores.js'
	import {assert,comp2,log,multiSort,spaceShip} from './lib/utils.js'

	window.onresize = resize

	log('Skapad: 2023-01-23 17:28')

	countapi.visits(':HOST:',':PATHNAME:').then((result) => {console.log('countapi',result.value)})

	// let Home

	async function getJSON() {
		let response = await fetch("./json/bilder.json")
		return await response.json()
	}
	const promise = getJSON()

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

			// cards = cards.concat($images.slice(n, n + 20))
			for (const md5 of $images.slice(n, n + 20)) {
				cards.push($invHome[md5])
			}
			cards = cards

			const latest = _.last(cards)
			if (n > 0) {
				ymax = latest.y + latest.sh // y + h
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
	$: visibleKeys = getVisibleKeys($images,path.length)

	const is_jpg = (file) => file.endsWith('.jpg') || file.endsWith('.JPG')
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)
	const spreadWidth = (share,WIDTH) => Math.floor((WIDTH-2*GAP*(1/share+1))*share) - 2

	function expand(imagedata,path,filename) { // converts 6-element array to object with 14 properties
		const bild = {}

		// data from json file:
		bild.sw  = imagedata[0] // small width
		bild.sh  = imagedata[1] // small height
		bild.bs  = imagedata[2] // big size
		bild.bw  = imagedata[3] // big width
		bild.bh  = imagedata[4] // big height
		bild.md5 = imagedata[5] // unique id based om md5

		// added properties:
		bild.path = path         // the folder names only
		bild.filename = filename // filename with extension .jpg

		// dynamic properties:
		bild.letterCount = 0 // created when searching
		bild.letters = ''
		bild.x = 0 // swimlane position
		bild.y = 0
		bild.index = 0 
		// bild.selected = false // checkbox

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

	consumeParameters()

	function consumeParameters() {
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

		// if (urlParams.has("md5")) {
		// 	visaBig(urlParams.get("bs"), urlParams.get("bw"), urlParams.get("bh"), urlParams.get("md5"),urlParams.get("path"),urlParams.get("filename"))
		// } else if (urlParams.has("ids")) {

		// } else {
		// }
	}

	$: [text0,text1,$images] = search(_.last(path), sokruta, stack.join('/'), $Home)
	// $: log('images',$images.length)

	$: placera($images,visibleKeys)

	function resize() {
		WIDTH = calcWidth(innerWidth)
		placera($images,visibleKeys)
	}


	function f(skala,left,x,width) {return Math.round((1-skala) * (x-left))} //         
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

	function visaBig(card) { //bs, bw, bh, md5, path, filename
		// console.log('visaBig',md5)
		document.body.style = "overflow:hidden"

		big.exifState = 0
		big.mouseState = 0

		big.bs = card.bs
		big.bw = card.bw
		big.bh = card.bh

		big.skala = Math.min(innerHeight/big.bh, innerWidth/big.bw)
		big.width = big.bw * big.skala
		big.height = big.bh * big.skala
		big.left = (innerWidth-big.width)/2
		big.top = (innerHeight-big.height)/2

		big.md5 = card.md5
		big.path = card.path
		big.filename = card.filename
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

	// Gå igenom listan, plocka ut de knappar som ska synas.
	function getVisibleKeys(images,level) {
		const result = {}
		// log('images.length',images.length,{level})
		for (const md5 of images) {
			const data = $invHome[md5]
			const arr = data.path.split("/")
			if (level >= arr.length) break
			const key = arr[level]
			result[key] ||= 0
			result[key] += 1
		}
		return result
	}

	function search(node,words,path) {
		// log('search')
		const result = []
 
		// rekursiv pga varierande djup i trädet
		function recursiveSearch (node,words,path,levels) { // node är nuvarande katalog. words är de sökta orden
			tick()
			if (levels==0) return
			for (const key in node) {
				const newPath = path + "/" + key
				if (is_jpg(key)) {
					total += 1
					let s = ''
					const newpath = newPath //.toLowerCase()
					for (const i in range(words.length)) {
						const word = words[i]
						if (word.length == 0) continue
						count += 1
						if (newpath.slice(10).includes(word)) s += ALFABET[i]
					}
					if (s.length > 0 || words.length == 0) {
						node[key].letters = s
						node[key].letterCount = s.length
						result.push(node[key].md5)
						stat[s] = (stat[s] || 0) + 1
					}
				} else {
					recursiveSearch(node[key], words, newPath, levels - 1)
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

		const levels = 99
		recursiveSearch(node, words, path, levels)

		result.sort((a,b) => multiSort($invHome[a],$invHome[b],'letterCount letters path filename','letterCount path'))

		const keys = Object.keys(stat)
		keys.sort(comp2) 
		const st = []
		let antal = 0
		for (const key of keys) {
			st.push(`${key}:${stat[key]}`) 
			antal += stat[key]
		}
		// if (result.length < 150) log({result})
		return [st.join(' '),`found ${antal} of ${total} images in ${new Date() - start} ms`,result]
	}

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images,visibleKeys) {
		const rows = sokruta=="" ? 4 : 5
		let antal = rows + 1 + _.size(visibleKeys)
		if (stack.length==2) antal+=1
		if (stack.length!=2 && buttons) antal+=1

		offset = 34 * antal // 30 + 2 * margin=2

		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)

		const cols = [offset]
		for (const i in range(COLS)) cols.push(0)
		const textHeights = 50-2 //43
		for (const i in range(images.length)) {
			tick()
			const md5 = images[i]
			const bild = $invHome[md5]
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			bild.x = (GAP + WIDTH)*index
			bild.y = cols[index]
			bild.index = i
			cols[index] += Math.round(WIDTH*bild.sh/bild.sw) + textHeights // h/w
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

	function setHome(data) {
		$Home = data
		$invHome = invertHome($Home)
		path = [$Home]
		stack = ["Home"]
		return ""
	}

</script>

<svelte:window bind:scrollY={y}/>

{#await promise }
	<p>Loading...</p>
{:then data}
	{setHome(data)}
	{#if state == 'NORMAL'}
		<Search bind:sokruta {text0} {text1} {stack} {WIDTH} {GAP} {spreadWidth} {path} {_} {is_jpg} bind:state {MAX_DOWNLOAD} />
		<Download {WIDTH} {spreadWidth} {MAX_DOWNLOAD} {stack} {pop}/>
		<NavigationHorisontal {stack} {WIDTH} />
		<NavigationVertical bind:buttons {visibleKeys} {push} {is_jpg} {WIDTH} {spaceShip} {stack} />
		<Infinite bind:state {WIDTH} {cards} {round} {fileWrapper} {prettyFilename} {visaBig}/>
	{:else}
		{#if state == 'PICTURE'}
			<BigPicture bind:state {big} {prettyFilename} />
		{:else}
			<Play bind:state />
		{/if}
	{/if}
{/await}
