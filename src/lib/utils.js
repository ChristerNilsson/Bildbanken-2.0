import _ from 'lodash'

export const log = console.log

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

export const splitPath = (s) => s=='' ? [] : s.split('/')
assert(splitPath(''),     [] )
assert(splitPath('a'),    ['a'] )
assert(splitPath('a/a1'), ['a','a1'] )

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

export function assert(a,b,msg="") {
	if (!_.isEqual(a,b)) {
		log("Assert failed",msg)
		log(a)
		log(b)
		// debug.assert(!_.isEqual(a,b))
	}
}

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
