import _ from 'lodash'

export const log = console.log

const ALFABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX'

// $: log(menu)

// export function assert (msg,a,b) {
// 	if (!_.isEqual(a,b)) {
// 		log('Assert',msg, 'failed')
// 		log('  a:',a)
// 		log('  b:',b)
// 	} else {
// 		// log('Assert',msg,'ok')
// 	}
// }

export function assert(a,b,msg="") {
	if (!_.isEqual(a,b)) {
		log("Assert failed",msg)
		log(a)
		log(b)
		// debug.assert(!_.isEqual(a,b))
	}
}

export const is_jpg = (file) => file.endsWith('.jpg') || file.endsWith('.JPG')

const pp = (x) => x < 10 ? '0' + x : x

export function unpack(packed) {
	const t = _.map(packed, ch => ALFABET.indexOf(ch))
	const ym = t[0] * 60 + t[1]
	return `${1970 + Math.floor(ym/12)}-${pp(1 + ym%12)}-${pp(t[2]+1)} ${pp(t[3])}:${pp(t[4])}:${pp(t[5])}`
}
assert(unpack("000000"),"1970-01-01 00:00:00")
assert(unpack('aAik80'),"2023-01-19 20:08:00")
assert(unpack('aB1byU'),"2023-02-02 11:34:56")
assert(unpack('aB1byV'),"2023-02-02 11:34:57")
assert(unpack('q00000'),"2100-01-01 00:00:00")
assert(unpack('K00000'),"2200-01-01 00:00:00")
assert(unpack("XXunXX"),"2269-12-31 23:59:59")


// export function unpack(packed) { 
// 	let unix = 0 // Detta är ej unixtid, pga bugg och DST
// 	for (const ch of packed) unix = unix * 64 + ALFABET64.indexOf(ch)
// 	const res = []
// 	for (const factor of [60,60,24,31,12,9999]) {
// 		res.unshift(unix % factor)
// 		unix = Math.floor(unix / factor)
// 	}
// 	res[0] += 1970
// 	res[1] += 1
// 	res[2] += 1
// 	return res[0] + '-' + pp(res[1]) + '-' +pp(res[2]) +' ' + pp(res[3])+ ':' + pp(res[4])+ ':' + pp(res[5])

// }
// assert(unpack("000000"),"1970-01-01 00-00-00")
// assert(unpack("100000"),"2003-05-28 13-37-04")
// assert(unpack("200000"),"2036-10-25 03-14-08")
// assert(unpack("Z00000"),"4007-11-08 14-41-04")
// assert(unpack("-00000"),"4041-04-05 04-18-08")
// assert(unpack("_00000"),"4074-09-01 17-55-12")
// assert(unpack("______"),"4108-01-29 07-32-15")


export const splitPath = (s) => s=='' ? [] : s.split('/')
assert(splitPath(''),     [] )
assert(splitPath('a'),    ['a'] )
assert(splitPath('a/a1'), ['a','a1'] )

export const round = (x,n=0) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)

export function getChildren(curr,path) {
	if (_.size(curr)==0) return []
	for (const item of splitPath(path)) curr = curr[item]
	return _.keys(curr)
}
// assert(getChildren(menu,''), ['a','b'])
// assert(getChildren(menu,'a'), ['a1', 'a2', 'a3'])
// assert(getChildren(menu,'a/a1'), ['a11','a12'])

// Söker upp en bild från roten, givet path
export function fetchSubTree(curr,path) {
	// log('fetchSubTree in',{curr},{path})
	if (_.size(curr)==0) return curr
	for (const item of splitPath(path)) curr = curr[item]
	// log('fetchSubTree out',{curr})
	return curr
}

// export function getObject(curr,path) {
// 	curr = fetchSubTree(curr,path)
// }

// Hämtar det tillplattade subträdet. 
// Returnerar en lista av [sw,sh,bs,bw,md5,path,key]
// ej filtrerat på söksträngen
export function selectImages(curr,path,sokruta) {
	const selected = []
	// const folders = []
	function recurse(curr,path,key) {
		// log('recurse',{curr,path,key})
		if (path.toLowerCase().endsWith('.jpg')) {
			if (path.includes(sokruta)) {
				// log({curr})
				if (path.startsWith('/')) {
					selected.push(curr.concat(path.slice(1)))
				} else {
					selected.push(curr.concat(path))
				}
			}
		} else {
			for (const k of _.keys(curr)) {
				// if (!k.toLowerCase().endsWith('.jpg')) log(path + '/' + k)
				recurse(curr[k],path + '/' + k,k)
			}
		}
	}
	// log('folders',folders)
	log(path)
	recurse(curr,path)
	log({selected})
	return selected
}

// export function selectImages(curr,path,sokruta) {
// 	const selected = []
// 	// const folders = []
// 	function recurse(curr,path,key) {
// 		log('recurse',{curr,path,key})
// 		if (path.toLowerCase().endsWith('.jpg')) {
// 			// if (path.toLowerCase().endsWith('.jpg') && path.includes(sokruta)) {
// 				// const data = curr[key]
// 			// log({data})
// 			if (path.startsWith('/')) {
// 				selected.push(path.slice(1))
// 			} else {
// 				selected.push(path)
// 			}
// 		} else {
// 			for (const k of _.keys(curr)) {
// 				// if (!k.toLowerCase().endsWith('.jpg')) log(path + '/' + k)
// 				recurse(curr[key],path + '/' + k,k)
// 			}
// 		}
// 	}
// 	// log('folders',folders)
// 	log(path)
// 	recurse(fetchSubTree(curr,path),path,"")
// 	log({selected})
// 	return selected
// }

export function clean(a,b) {
	if (!a.startsWith('/')) a = '/' + a
	return a.endsWith('/') || b.startsWith('/') ? a + b : a + '/' + b
}
assert(clean('/','2011'),'/2011')
assert(clean('/2022', '2022--2023 Allsvenskan Division III_T10438'),'/2022/2022--2023 Allsvenskan Division III_T10438')
assert(clean('/2022/2022-07-02_Schack-SM Uppsala_I10044',"Weekend-2"), "/2022/2022-07-02_Schack-SM Uppsala_I10044/Weekend-2")

// assert(0,'Ab'.toLowerCase(), 'ab')
// assert(1,'Ab'.toUpperCase(), 'AB')
// for (const item in "ab") log(item) 0,1
// for (const item of "ab") log(item) a,b

// keyword|for (item in IN)|for item in IN:|a,b|a,b
// keyword|for (item of IN)|for item in range(len(IN)):|a,b|0,1
// keyword|for (item in IN)|for item in IN:|a:3,b:4|a,b
// keyword|for (item in IN)|for item in range(len(IN)):|a:3,b:4|3,4

export function spaceShip (a,b,desc=1) {
	if (a < b) return -desc
	else if (a == b) return 0
	return desc
}
assert(spaceShip(1,2),-1)
assert(spaceShip(1,1),0)
assert(spaceShip(1,0),1)

assert(spaceShip(1,2,-1),1)
assert(spaceShip(1,1,-1),0)
assert(spaceShip(1,0,-1),-1)

assert(_.range(3),[0,1,2])

export function comp (a,b) { if (a[0] == b[0]) {return spaceShip(a[1], b[1])} else {return spaceShip(a[0], b[0])}}

// export function multiSort (a,b,keys,desc=" ") { // det som sorteras är objekt
// 	keys = keys.split(' ')
// 	desc = desc.split(' ')
// 	for (const key of keys) {
// 		let result = spaceShip(a[key],b[key], (desc.includes(key) ? -1 : 1))
// 		if (result != 0) return result
// 	}
// }
// assert(false,''.split(' ').includes(' '),'XX')
// assert(true,'A'.split(' ').includes('A'),'YY')
// assert(false,'A'.split(' ').includes('B'),'ZZ')

// assert([{y:18,n:'A'}, {y:13,n:'B'}], [{y:18,n:'A'}, {y:13,n:'B'}].sort((a,b) =>  multiSort(a,b,'y n','y')), 'AA')
// assert([{y:13,n:'B'}, {y:18,n:'A'}], [{y:18,n:'A'}, {y:13,n:'B'}].sort((a,b) =>  multiSort(a,b,'y n')) ,    'BB')
// assert([{y:13,n:'B'}, {y:18,n:'A'}], [{y:18,n:'A'}, {y:13,n:'B'}].sort((a,b) =>  multiSort(a,b,'n y','n')), 'CC')
// assert([{y:18,n:'A'}, {y:13,n:'B'}], [{y:18,n:'A'}, {y:13,n:'B'}].sort((a,b) =>  multiSort(a,b,'n y')) ,    'DD')

export function comp2(a,b) { if (a.length == b.length) {return spaceShip(a,b)} else {return -spaceShip(a.length,b.length)}}
assert(comp2("A","B"),-1)
assert(comp2("AB","AB"),0)
assert(comp2("B","A"),1)
assert(comp2("BC","A"),-1)

export function prettyFilename(path) { // Tag bort eventuella M och V-nummer
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
	//s = s.replace(/ T\d\d\d\d\d/,'')
	s = s.replaceAll('_',' ')
	return s
}

