<script>

	import _ from "lodash"
	import countapi from 'countapi-js'
	import Card from "./Card.svelte"
	import Download from "./Download.svelte"
	import Help from "./Help.svelte"
	import NavigationVertical from "./NavigationVertical.svelte"
	import NavigationHorisontal from "./NavigationHorisontal.svelte"
	import Search from "./Search.svelte"
	import BigPicture from "./BigPicture.svelte"
	import Play from "./Play.svelte"
	import Tree from "./Tree.svelte"
	import {fileIndex,Home,invHome,images,selected,settings} from './lib/stores.js'
	import {assert,comp2,is_jpg,log,range,spaceShip,unpack} from './lib/utils.js'

	const version = '2023-04-25 19:30'

	let md5

	// Förberett för att använda flera json-filer.
	const p1 = fetch('./json/bilder.json').then(r => r.json())
	const p2 = fetch('./json/file_index.json').then(r => r.json())
	const promise = Promise.all([p1,p2])

	function handleJSON(arrJSON) {
		$Home      = arrJSON[0]
		$fileIndex = arrJSON[1]
		$invHome = invertHome($Home)
		path = [$Home]
		stack = ["Home"]
		return ''
	}

	// countapi.visits(':HOST:',':PATHNAME:').then((result) => {console.log('countapi',result.value)})

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

	let skala = 1

	const ALFABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	const SCROLLBAR = 0 // 12+3+1
	const GAP = 1
	$: WIDTH = calcWidth(innerWidth)
	$: COLS = Math.floor((innerWidth-SCROLLBAR-GAP)/WIDTH)

	let path=[] // = [$Home] // used for navigation
	let stack=[] //= ["Home"]
	
	let stat={}
	let total=0
	let buttons = false

	let sokruta = ""
	
	let text0 = ""
	let text1 = ""
	let visibleKeys = {} // innehåller antal bilder per katalog söksträngen finns i. T ex {"2022":7,"2021":3}

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

		// added properties:
		bild.path = path         // the folder names only
		bild.filename = filename // filename with extension .jpg
		bild.timestamp = unpack(bild.md5.slice(0,6)) // abcXYZ => 2023-01-24 12:34:56

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
					recurse(node[key],path + '/' + key)
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
			const ids = urlParams.get("ids").split('|')
			for (const md5 of ids) $selected[md5] = true
			state = 'PLAY'
		}
		if (urlParams.has("md5")) {
			md5 = urlParams.get("md5")
			state = 'PICTURE'
		}
		if (urlParams.has("tree")) {
			state = 'TREE'
		}
	}

	$: [text0, text1, $images,visibleKeys] = search(_.last(path), sokruta, stack.join('/'), $settings, $Home)

	$: placera($images,innerWidth,antal)
	$: WIDTH = calcWidth(innerWidth)

	function resize() {
		cards = []
		ymax = 0
		WIDTH = calcWidth(innerWidth)
		placera($images,innerWidth,antal)
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

	function search(node,words,path,settings) {

		if (!settings.case) words = words.toLowerCase()
		const result = []
		let visibleKeys = {}
		ymax = 0 // Viktigt! Annars syns inte nya bilder.
		cards = []
		words = words.length == 0 ? [] : words.split(" ")
		if (!settings.all) words = _.map(words, (word) => '_' + word) // beginning
		path = path.replaceAll(' ','_').replaceAll('.','_').replaceAll('/','_')
		if (!settings.case) path = path.toLowerCase()
		stat = {}

		const start = new Date()
		const x = 0
		const y = 0
 
		function recursiveSearch (node, sPath0='', accKey0='') { 
			// node är nuvarande delträd.
			// sPath0 = '2022' osv
			// accKey används för att ackumulera antal bilder i närmast underliggande noder.
			for (const key0 in node) {
				const accKey1 = accKey0=='' ? key0 : accKey0
				let key1 = key0.replaceAll(' ','_').replaceAll('.','_')
				if (!settings.case) key1 = key1.toLowerCase()
				const sPath1 = sPath0 + '_' + key1
				if (is_jpg(key0)) {
					const md5 = node[key0].md5
					let letters = ''
					if (words.length==0) {
						result.push({md5, letters, x, y})
						stat[letters] ||= 0
						stat[letters] += 1
						if (!is_jpg(accKey1)) {
							visibleKeys[accKey1] ||= 0
							visibleKeys[accKey1] += 1
						}
					} else {
						const timestamp = node[key0].timestamp
						const sPath2 = sPath1 + '_' + md5 + '_' + timestamp.replace(' ','_')
						for (const i in range(words.length)) {
							let word = words[i]
							if (word.length == 0) continue
							// log({sPath2,word},sPath2.includes(word))
							if (sPath2.includes(word)) letters += ALFABET[i]
						}
						if (letters.length > 0) {
							result.push({md5, letters, x, y})
							stat[letters] ||= 0
							stat[letters] += 1
							visibleKeys[accKey1] ||= 0
							visibleKeys[accKey1] += 1
						}
					}
				} else {
					recursiveSearch(node[key0],sPath1,accKey1)
				}
			}
		}

		recursiveSearch(node,path) // Slower, but root..curr folder searchable
		// recursiveSearch(node) // Quicker, but root..curr folder not searchable

		function g(a,b) {
			const al = a.letters
			const bl = b.letters
			return spaceShip(bl.length,al.length) || spaceShip(al,bl) || spaceShip(b.md5,a.md5)
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

		log(visibleKeys)
		return [st.join(' '),`found ${antal} images in ${new Date() - start} ms`,result,visibleKeys]
	}

$: antal = 7 + _.size(visibleKeys)

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images,innerWidth,antal) {
		offset = 34 * antal
		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)
		const cols = _.map(range(COLS), (element) => 0)
		cols[0] = offset
		const textHeights = 49 // borde vara 49 för iOS och 44 för Windows
		for (const i in range(images.length)) {
			const image = images[i]
			const ih = $invHome[image.md5]
			let index = 0 // sök fram index för minsta kolumnen
			for (const j in range(COLS)) {
				if (cols[j] < cols[index]) index = j
			}
			image.x = (GAP + WIDTH)*index
			image.y = cols[index]
			image.index = i
			cols[index] += Math.round(WIDTH*ih.sh/ih.sw + textHeights)
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

</script>

<svelte:window bind:scrollY={y}/>

{#await promise}
	<p>&nbsp;{version}</p>
{:then arrJSON}
	{handleJSON(arrJSON)}
	{#if state == 'NORMAL'}
		<Search bind:sokruta {text0} {text1} {stack} {WIDTH} {GAP} {spreadWidth} {pop} />
		<Download {WIDTH} {spreadWidth} {MAX_DOWNLOAD} />
		<NavigationHorisontal {stack} {WIDTH} />
		<NavigationVertical bind:buttons {visibleKeys} {push} {WIDTH} {spaceShip} {stack} />
		{#each cards as card}
			<Card {WIDTH} {card} />
		{/each}
	{/if}
	{#if state == 'PICTURE'}
		<BigPicture {md5} />
	{/if}
	{#if state == 'PLAY'}
		<Play bind:state />
	{/if}
	{#if state == 'TREE'}
		<Tree/>
	{/if}
{/await}