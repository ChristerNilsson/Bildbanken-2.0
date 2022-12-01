# Om bilder eller kataloger saknas i Small, skapas dessa och Cache uppdateras

import time
import json
from os import scandir, mkdir, remove, rmdir
from os.path import exists, getsize
from PIL import Image
import hashlib
import shutil

WIDTH = 475

ROOT = "C:\\github\\2022-014-Bildbanken2\\"
Original = ROOT + "public\\Original"
Home = ROOT + "public\\Home"
small = ROOT + "public\\small"
JSON = ROOT + "public\\json\\"

def is_jpg(key): return key.endswith('.jpg') or key.endswith('.JPG')


def is_tif(key): return key.endswith('.tif') or key.endswith('.TIF')


def frekvens(s):
	for letter in '-,[]{}.;_"0123456789':
		s = s.replace(letter,' ')
	words = s.split(' ')
	hash = {}
	for word in words:
		if word in hash:
			hash[word] += 1
		else:
			hash[word] = 1
	keys = list(hash.keys())
	keys.sort()
	for word in keys:
		if hash[word] == 1:
			print(word)


def dumpjson(data,f):
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
	s = s.replace("],","],\n") # Varje key (katalog,fil) på egen rad.
	s = s.replace(":{",":\n{")
	s = s.replace(']},"',']},\n"')
	# frekvens(s)
	f.write(s)

# def pop(path):
# 	arr = path.split('\\')
# 	arr.pop()
# 	return "\\".join(arr)

# def dump(a):
# 	for key in a:
# 		print(key,a[key])


def loadJSON(path):
	if not exists(path): return {}
	with open(path, 'r', encoding="utf8") as f:
		return json.loads(f.read())


# def pruneCache():
# 	antal = {'files':0, 'folders':0}
# 	keys = list(c.keys())
# 	keys = reversed(keys)
# 	for key in keys:
# 		if key not in a:
# 			if is_jpg(key):
# 				antal['files'] += 1
# 			else:
# 				antal['folders'] += 1
# 			patch(cache, key, None)
# 	return antal


def ensurePath(root,path):
	arr = path.split("\\")
	for i in range(len(arr)):
		p = root + "\\" + "\\".join(arr[0:i])
		if not exists(p): mkdir(p)


def patch(tree,path,data):
	arr = path.split("\\")
	ptr = tree
	for key in arr[1:len(arr)]:
		if key not in ptr: ptr[key] = {}
		if key != arr[-1]: ptr = ptr[key]
	if data:
		ptr[key] = data
	else:
		del ptr[key]


def makeSmall(Original,Home,small,name):

	with open(Original+name,"rb") as f:
		data = f.read()
		md5hash = hashlib.md5(data).hexdigest()

	filename = "\\" + md5hash + ".jpg"
	if md5hash in md5Register and exists(Home + filename) and exists(small + filename):
		lst = md5Register[md5hash]
		patch(cache, name, lst)
		return lst
	else:
		print('.', end="")

	bigImg = Image.open(Original+name)
	bigSize = getsize(Original+name)

	# bigImg.save(Home + "\\" + md5hash + '.jpg')
	shutil.copyfile(Original + name, Home + "\\" + md5hash + '.jpg')

	smallImg = bigImg.resize((WIDTH, round(WIDTH*bigImg.height/bigImg.width)))
	# ensurePath(b,name)
	smallImg.save(small + "\\" + md5hash + '.jpg')
	lst = [smallImg.width, smallImg.height, bigSize, bigImg.width, bigImg.height, md5hash]
	md5Register[md5hash] = lst
	patch(cache, name, lst)
	return lst


# utöka Home, Small och Cache
def expand(a,d):
	antal = {'files':0, 'folders':0}
	for key in a.keys():
		if key not in d:
			if is_jpg(key):
				antal['files'] += 1
				d[key] = makeSmall(Original,Home,small,key)
			else:
				print('D', end="")
				antal['folders'] += 1
	print()
	return antal


# minska Cache  # utifrån jmf mellan Original och Cache
def shrink(d,a):
	antal = {'files':0, 'folders':0, 'keys':0}
	keys = list(d.keys())
	keys = reversed(keys)
	for key in keys:
		if key not in a: # Original
			patch(cache, key, None)
			# md5Key = "\\" + d[key][5]+".jpg"
			# filename = Home + md5Key
			# if exists(filename):
			# 	remove(filename)
			# filename = small + md5Key
			# if exists(filename):
			# 	remove(filename)
			if is_jpg(key):
				antal['files'] += 1
			else:
				antal['folders'] += 1
	return antal

# def getInfo(path):
# 	info = Image.open(path)
# 	size = getsize(path)
# 	return [info.width, info.height, size]


def flat(root, res={}, path=""):
	ensurePath(root, path)
	for name in [f for f in scandir(root + "\\" + path)]:
		namn = name.name
		path1 = path + "\\" + namn
		if name.is_dir():
			res[path1] = ""
			flat(root, res, path1)
		elif is_jpg(namn):
			res[path1] = ""
		else:
			print("*** Ignored file:", "public\\Home" + path1)
	return res


def flatten(node, res={}, path=''):
	for key in node:
		path1 = path + "\\" + key
		if is_jpg(key):
			res[path1] = node[key]
			md5Key = res[path1][5]
			#md5Register[md5Key] = res[path1]
		else:
			res[path1] = ""
		if not type(node[key]) is list:
			flatten(node[key],res, path1)
	return res


def compare(a,b,message):
	res = {}
	cfiles = 0
	cfolders = 0
	for path in a:
		if path not in b:
			if is_jpg(path):
				if cfiles == 0: res[path] = 0
				cfiles += 1
			else:
				res[path] = 0
				cfolders += 1
	if cfolders > 0 or cfiles > 0:
		print(message, cfolders, 'folders +', cfiles, 'files')
	return res


def compare2(message,x,y):
	res = {}
	res['missing'] = compare(x, y, 'Original vs ' + message + ': missing')
	res['surplus'] = compare(y, x, 'Original vs ' + message + ': surplus')
	return res


def countFolders(arr):
	antal = 0
	for key in arr:
		if not is_jpg(key): antal += 1
	return antal


hash = {}
letters = list("+!§()0123456789_,.-¤")
stoppord = 'aasen adepterr adersson jpg lowres och på adrian allan alsamarrai amalie amen analyse anmästearen anzambi autografskrvning ble blixte calm campo cat ceremonie coh dah dax deltagran do during ea edvin eisler ellen enricsson entre exteriöre frisys fö föräldrarl fötäldrar galleriet ggr gm hampus hanna hasselbacken his hurry huvudnonader idar ingertz interiiör interiö interiöri intervjuvar intrvjuas istället jadoube joakim jonathan jouni jubileuml junioer juniotturneringen jöberg kafeet kafffet kankse khalili klari koentatorsrummet kollar kollekt kommentatorr kommentatorrummet kommentatorsrummeti kommentatro kommenttorsrummet kommpisar kompisarpg lagdledare lagledate larsson lennart lexander linnea linus livesändningl livesåndning lokander lottnig lågstadet lögdahl mallanstadiet malmö mediaansvari miniior morellr mourad muntean mästartklassen näringsllivet oc ocb ocg ochh ocj oh olk ollefsén ostafiev ove pannka pch pettersson prisutdelnineng prisutdelningl prisutdelningr prize producenr profiiler publiparti qi radd raden resultatapportering resultatrapporteing reultatrapportering reultatredovisning rmorgondagens rondpausl rånby santiago sara schackinstruktio schackyouga seo severingen sgnerer simultanspell sk slutforsering snabbschacksdm solemn solomia some spealre spelaregistrering speling spellokaleni spleare sponsorerrond steinitz stromästarna stsningsgruppen ter the thordur tran trino triumvirat truskavetska träder tuomainen utanföt vallatorpsskolan vatn vede ver veteranallmän vilolaäge waeli wedberg wernberg with wweb xunming xxxxx åskådarei åskådarer åsådare af amassadör emanuel exteriörr klaas klas kolobok line livesädningen lottnib ooch prisutdelnigen pågåender shah sllutspel stasik to träbingsparti årfest års årsjubileum rondl tränongsparti vt it problemlösnings ron xuanming la mter and bokförsälning rrond highres cafeét veterner avlutningen of ans gr an'.split(' ')

def flatWords(node):
	for key in node:
		words = key
		for letter in letters:
			words = words.replace(letter," ")
		for word in words.split(' '):
			wordLower = word.lower()
			if len(word) > 1 and wordLower == word:
				hash[word] = hash[word]+1 if word in hash else 1
		if type(node[key]) is dict: flatWords(node[key])

def convert(hash):
	arr = []
	for key in hash.keys():
		if key not in stoppord:
			arr.append([hash[key],key])
	arr = sorted(arr)
	return arr

######################

md5Register = loadJSON(JSON + 'MD5.json') # givet md5key får man listan med sex element
cache = loadJSON(JSON + 'bilder.json')

# start = time.time()
# flatWords(cache)
# keys = convert(hash)
# print(len(keys),'words in', round(time.time()-start,3),'seconds')
# print()
# for [count,key] in keys:
# 	print(key + ':' + str(count))

a = flat(Original, {}) # Readonly!
b = flat(Home)   # Används bara för räkning
c = flat(small)  # Används bara för räkning
d = flatten(cache, {})

print()
ca = countFolders(a)
cb = countFolders(b)
cc = countFolders(c)
cd = countFolders(d)

print('Original:', ca, 'folders +', len(a) - ca,'files')
print('Home:    ', cb, 'folders +', len(b) - cb,'files')
print('Small:   ', cc, 'folders +', len(c) - cc,'files')
print('Cache:   ', cd, 'folders +', len(d) - cd,'files')

print()
resCache = compare2('Cache',a,d)
#resCache = compare2('Cache',a,c)

print()
for key in resCache['missing'].keys(): print('Cache missing:', key)
print()
for key in resCache['surplus'].keys(): print('Cache surplus:', key)
# print()
# for key in resCache['missing'].keys(): print('Cache missing:', key)
# print()
# for key in resCache['surplus'].keys(): print('Cache surplus:', key)

print()
update = input('Update? (NO/Yes) ').upper()
update = update.startswith('Y')

if update:

	start = time.time()
	print()
	antal = expand(a,d)
	print()
	if antal['files'] > 0: print('Cache: Added', antal['files'], 'files')

	antal = shrink(d,a)
	if antal['files'] > 0: print('Cache: Deleted', antal['files'], 'files')

	# antal = shrink(d,a,small)
	# if antal['files'] > 0: print('Small: Deleted', antal['files'], 'files')

	if antal['keys'] > 0: print('Cache: Deleted', antal['keys'], 'keys')

#	antal = pruneCache()
#	if antal['folders'] > 0 or antal['files'] > 0: print('Cache: Pruned',  antal['folders'], 'folders and', antal['files'], 'files')

	with open(JSON + 'bilder.json', 'w', encoding="utf8") as f: dumpjson(cache,f)
	with open(JSON + 'MD5.json', 'w', encoding="utf8") as f: dumpjson(md5Register,f)
	print()
	print(round(time.time() - start,3),'seconds')
