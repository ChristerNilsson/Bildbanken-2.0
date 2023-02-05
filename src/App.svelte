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
	import {fileIndex,Home,invHome,images,selected} from './lib/stores.js'
	import {assert,comp2,log,spaceShip} from './lib/utils.js'

	const version = '2023-02-02 11:20'

	const ALFABET64 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'

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

	let skala = 1

	// $: fileWrapper = [$fileIndex]
		
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

	const is_jpg = (file) => file.endsWith('.jpg') || file.endsWith('.JPG')
	const round = (x,n) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)
	const spreadWidth = (share,WIDTH) => Math.floor((WIDTH-2*GAP*(1/share+1))*share) - 2

	const pp = (x) => x < 10 ? '0' + x : x

	function unpack(packed) { 
		let unix = 0 // Detta är ej unixtid, pga bugg och DST
		for (const ch of packed) unix = unix * 64 + ALFABET64.indexOf(ch)
		const res = []
		for (const factor of [60,60,24,31,12,9999]) {
			res.unshift(unix % factor)
			unix = Math.floor(unix / factor)
		}
		res[0] += 1970
		res[1] += 1
		res[2] += 1
		return res[0] + '-' + pp(res[1]) + '-' +pp(res[2]) +' ' + pp(res[3])+ ':' + pp(res[4])+ ':' + pp(res[5])

	}
	assert(unpack("000000"),"1970-01-01 00-00-00")
	assert(unpack("100000"),"2003-05-28 13-37-04")
	assert(unpack("200000"),"2036-10-25 03-14-08")
	assert(unpack("Z00000"),"4007-11-08 14-41-04")
	assert(unpack("-00000"),"4041-04-05 04-18-08")
	assert(unpack("_00000"),"4074-09-01 17-55-12")
	assert(unpack("______"),"4108-01-29 07-32-15")

	// function unpack(packed) { 
	// 	let unix = 0
	// 	for (const ch of packed) unix = unix * 64 + alfabet.indexOf(ch)
	// 	const second = unix % 60
	// 	unix -= second
	// 	unix = unix / 60
	// 	const minute = unix % 60
	// 	unix -= minute
	// 	unix = unix / 60
	// 	const hour = unix % 24
	// 	unix -= hour
	// 	unix = unix / 24
	// 	let day = unix % 31
	// 	unix -= day
	// 	unix = unix / 31
	// 	let month = unix % 12
	// 	unix -= month
	// 	unix = unix / 12
	// 	const year = 1970 + unix
	// 	day+=1
	// 	month+=1
	// 	return year + '-' + pp(month) + '-' +pp(day) +' ' + pp(hour)+ ':' + pp(minute)+ ':' + pp(second)
	// }

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
	}

	$: [text0, text1, $images,visibleKeys] = search(_.last(path), sokruta, stack.join('/'), $Home)

	$: placera($images,visibleKeys,innerWidth,antal)
	$: WIDTH = calcWidth(innerWidth)

	function resize() {
		cards = []
		ymax = 0
		WIDTH = calcWidth(innerWidth)
		placera($images,visibleKeys,innerWidth,antal)
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

	// function visaBig(md5,ih) {
	// 	document.body.style = "overflow:hidden"

	// 	big.exifState = 0
	// 	big.mouseState = 0

	// 	big.bs = ih.bs
	// 	big.bw = ih.bw
	// 	big.bh = ih.bh

	// 	big.skala = Math.min(innerHeight/big.bh, innerWidth/big.bw)
	// 	big.width = big.bw * big.skala
	// 	big.height = big.bh * big.skala
	// 	big.left = (innerWidth-big.width)/2
	// 	big.top = (innerHeight-big.height)/2

	// 	big.md5 = md5
	// 	big.path = ih.path
	// 	big.filename = ih.filename
	// 	big.timestamp = ih.timestamp
	// 	big = big
	// }

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
		let visibleKeys = {}

		ymax = 0 // Viktigt! Annars syns inte nya bilder.
		cards = []

		words = words.length == 0 ? [] : words.split(" ")

		stat = {}
		total = 0

		const start = new Date()

		const arr = path.split('/')
		const level = arr.length
		const x = 0
		const y = 0
 
		// rekursiv pga varierande djup i trädet
		function recursiveSearch (node,arrPath0) { // node är nuvarande delträd. arrPath0=['Home','2022'] osv.
			for (const key in node) {
				const md5 = node[key].md5
				const arrPath1 = arrPath0.concat(key)
				const accKey = arrPath1[level]
				if (is_jpg(key)) {
					total += 1
					let letters = ''
					// ["Home","2023"] removed
					const sPath = arrPath1.slice(2).join('/').replaceAll(' ','_') // .toLowerCase()
					for (const i in range(words.length)) {
						const word = words[i]
						if (word.length == 0) continue
						if (sPath.includes(word)) letters += ALFABET[i]
					}
					if (letters.length > 0 || words.length == 0) {
						result.push({md5, letters, x, y})
						stat[letters] ||= 0
						stat[letters] += 1
						if (! is_jpg(accKey)) {
							visibleKeys[accKey] ||= 0
							visibleKeys[accKey] += 1
						}
					}
				} else {
					recursiveSearch(node[key], arrPath1)
				}
			}
		}

		recursiveSearch(node, arr)

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
		// visibleKeys = visibleKeys
		return [st.join(' '),`found ${antal} of ${total} images in ${new Date() - start} ms`,result,visibleKeys]
	}

$: antal = 7 + _.size(visibleKeys)

	// Räknar ut vilken swimlane som är lämpligast.
	// Uppdaterar x och y för varje bild
	// Uppdaterar listan cols som håller reda på nästa lediga koordinat för varje kolumn
	function placera(images,visibleKeys,innerWidth,antal) {
		offset = 34 * antal
		COLS = Math.floor((window.innerWidth-SCROLLBAR-GAP)/WIDTH)
		const cols = _.map(range(COLS), (element) => 0)
		// log('placera',{COLS,WIDTH,cols})
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

{#await promise}
	<p>&nbsp;{version}</p>
{:then arrJSON}
	{handleJSON(arrJSON)}
	{#if state == 'NORMAL'}
		<Search bind:sokruta {text0} {text1} {stack} {WIDTH} {GAP} {spreadWidth} {pop} />
		<Download {WIDTH} {spreadWidth} {MAX_DOWNLOAD} />
		<NavigationHorisontal {stack} {WIDTH} />
		<NavigationVertical bind:buttons {visibleKeys} {push} {is_jpg} {WIDTH} {spaceShip} {stack} />
		<Infinite {WIDTH} {cards} {prettyFilename} />
	{:else}
		{#if state == 'PICTURE'}
			<BigPicture {md5} {prettyFilename} />
		{:else}
			<Play bind:state />
		{/if}
	{/if}
{/await}