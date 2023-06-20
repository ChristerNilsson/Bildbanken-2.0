# Behövs rutin som rensar bort filer i Home och small utgående från bilder.json vid behov.
# MD5 behövs inte på webben, används bara för att hålla reda på listan med bredder och höjder.
# MD5 är bättre än löpnummer. T ex om man bytt namn på en bild, kan man hitta bilden mha MD5.
# Användaren initierar alla ändringar via Originalkatalogen. Pythonprogrammet ändrar EJ i Originalkatalogen.
# Dessa uppdaterar bilder.json, som kan minska eller öka i storlek.
# Bilder hamnar alltid i Home och small. Dessa kataloger växer hela tiden. Parametrar sparas i MD5.json
# Update = YES innebär att Home, small, bilder.json, MD5.json kan uppdateras.

# För total omstart rekommenderas:
#   Flytta bilder.json
#   Flytta MD5.json
#   (Flytta small)

# OBSERVERA: Javascript anv noll-baserad månad. Python använder ettbaserad månad.

import time
import json
from os import scandir, mkdir, rename
from os.path import exists, getsize, getmtime
from datetime import datetime
from PIL import Image
import hashlib
import shutil
import re
import codecs

ALFABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxy' # 60-based

QUALITY = 95
WIDTH = 475
YEAR = datetime.today().year

#ROOT = "C:/github/2022-014-Bildbanken2/"
ROOT = ""

Original = ROOT + "Original"       # cirka 2.000.000 bytes per bild (Readonly)
Home     = ROOT + "public/Home"    # cirka 2.000.000 bytes per bild
small    = ROOT + "public/small"   # cirka 	  25.000 bytes per bild
JSON     = ROOT + "public/json/"   # cirka       120 bytes per bild (bilder.json)
MD5      = ROOT + 'MD5.json'       # cirka        65 bytes per bild
FILE_INDEX = JSON + 'file_index.txt'
PUBLIC     = ROOT + "public/"
TREE       = ROOT + 'tree.txt'

def ass(a,b):
	if a == b: return
	print('assert failure')
	print('  ',a)
	print('  ',b)
	# assert(a==b)

def is_jpg(key): return key.endswith('.jpg') or key.endswith('.JPG')

def dumpjson(data,f):
	start = time.time()
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
	s = s.replace("],","],\n") # Varje key (katalog,fil) på egen rad.
	s = s.replace(":{",":\n{")
	s = s.replace('},"','},\n"')
	f.write(s)
	print('json',time.time()-start)

def loadJSON(path):
	if not exists(path): return {}
	with open(path, 'r', encoding="utf8") as f:
		return json.loads(f.read())

def ensurePath(root,path):
	arr = path.split("/")
	for i in range(len(arr)):
		p = root + "/" + "/".join(arr[0:i])
		if not exists(p): mkdir(p)

def patch(tree,path,data):
	arr = path.split("/")
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
	md5hash = codecs.encode(codecs.decode(md5hash, 'hex'), 'base64')
	md5hash = md5hash.decode("utf-8")
	md5hash = md5hash[0:4]
	md5hash = md5hash.replace('+','-').replace('/','_')

	ts = getTimestamp(Original+name).replace('-',' ').replace(':',' ').split(' ')
	pt = packedTime(ts)

	md5hash = pt + md5hash

	filename = "/" + md5hash + ".jpg"
	if md5hash in md5Register and exists(Home + filename) and exists(small + filename):
		lst = md5Register[md5hash]
		patch(cache, name, lst)
		return lst

	bigImg = Image.open(Original+name)
	bigSize = getsize(Original+name)

	if bigImg.width <= 2048:
		shutil.copyfile(Original + name, Home + "/" + md5hash + '.jpg')
	else:
		bigImg = bigImg.resize((2048, round(2048 * bigImg.height / bigImg.width)))
		bigImg.save(Home + "/" + md5hash + '.jpg',quality=QUALITY)

	smallImg = bigImg.resize((WIDTH, round(WIDTH*bigImg.height/bigImg.width)))
	smallImg.save(small + "/" + md5hash + '.jpg',quality=QUALITY)
	lst = [smallImg.width, smallImg.height, bigSize, bigImg.width, bigImg.height, md5hash] # , timestamp]
	md5Register[md5hash] = lst
	patch(cache, name, lst)
	return lst

def expand(a,d):
	antal = {'images':0, 'folders':0}
	i = 0
	for key in a.keys():
		if key not in d:
			if is_jpg(key):
				start = time.perf_counter()
				d[key] = makeSmall(Original, Home, small, key)
				print(f'{i:6.0f} {1000 * (time.perf_counter() - start):6.0f}', key)
				i += 1
			else:
				antal['folders'] += 1

	print()
	antal['images'] = i
	return antal

def shrink(d,a):
	antal = {'images':0, 'folders':0, 'keys':0}
	keys = list(d.keys())
	keys = reversed(keys)
	for key in keys:
		if key not in a: # Original
			patch(cache, key, None)
			if is_jpg(key):
				antal['images'] += 1
			else:
				antal['folders'] += 1
	return antal

def flat(root, res={}, path=""):
	ensurePath(root, path)
	for name in [f for f in scandir(root + "/" + path)]:
		namn = name.name
		path1 = path + "/" + namn
		if name.is_dir():
			res[path1] = ""
			flat(root, res, path1)
		elif is_jpg(namn):
			res[path1] = ""
		else:
			print("*** Ignored file:", "public/Home" + path1)
	return res

def flatten(node, res={}, path=''):
	for key in node:
		path1 = path + "/" + key
		if is_jpg(key):
			res[path1] = node[key]
		else:
			res[path1] = ""
			match = re.search(r'_[GLIRF]\d\d\d\d\d', key)
			if match:
				z = match.regs
				(p, q) = z[0]
				hit = key[p:q][2:]
				if hit not in fileIndex:
					print('Missing index',hit,'in',key)

		if not type(node[key]) is list:
			flatten(node[key],res, path1)
	return res

def compare(a,b,message):
	res = {}
	cimages = 0
	cfolders = 0
	for path in a:
		if path not in b:
			if is_jpg(path):
				res[path] = 0
				cimages += 1
			else:
				res[path] = 0
				cfolders += 1
	if cfolders > 0 or cimages > 0:
		print(message, cimages, 'images +', cfolders, 'folders')
	return res

def compare2(x,y):
	res = {}
	res['missing'] = compare(x, y, 'Missing:')
	res['surplus'] = compare(y, x, 'Surplus:')
	return res

def countFolders(arr):
	antal = 0
	for key in arr:
		if not is_jpg(key): antal += 1
	return antal

def flatWords(node):
	for key in node:
		words = key
		for letter in letters:
			words = words.replace(letter," ")
		for word in words.split(' '):
			wordLower = word
			if len(word) > 1 and wordLower == word:
				hash[word] = hash[word]+1 if word in hash else 1
		if type(node[key]) is dict: flatWords(node[key])

def findMatch(rex,path):
	match = re.search(rex,path)
	if match:
		z = match.regs
		(p,q) = z[0]
		date = path[p:q]
		if date:
			if path[p-1] in 'XM': return None
			if len(date) in [8,10]: return date
			if len(date) == 6: # kolla om datum existerar
				y = 2000 + int(date[0:2])
				m = int(date[2:4])
				d = int(date[4:6])
				if y <= YEAR+1 and m <= 12 and d <= 31: return date
	return None

def getFileDate(path):
	date = findMatch(r'\d\d\d\d-\d\d-\d\d',path) or findMatch(r'\d\d\d\d\d\d\d\d',path) or findMatch(r'\d\d\d\d\d\d',path)
	if date:
		if len(date) == 6: date = "20" + date[0:2] + "-" + date[2:4] + "-" + date[4:6]
		if len(date) == 8: date = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
		return date
	return None

def packedTime(lst): # Klarar timestamp < 2270-01-01 00:00:00 med sekund-upplösning (300 år)
	lst = [int(item) for item in lst]
	ym = (lst[0]-1970) * 12 + lst[1] - 1
	res = [ym//60, ym%60, lst[2]-1, lst[3], lst[4], lst[5]]
	return ''.join([ALFABET[i] for i in res])
ass(packedTime([1970, 1, 1, 0, 0, 0]), '000000')
ass(packedTime([2023, 1,19,20, 8, 0]), 'AbIK80')
ass(packedTime([2023, 2, 2,11,34,56]), 'Ac1BYv')
ass(packedTime([2023, 2, 2,11,34,57]), 'Ac1BYw')
ass(packedTime([2100, 1, 1, 0, 0, 0]), 'Q00000')
ass(packedTime([2200, 1, 1, 0, 0, 0]), 'l00000')
ass(packedTime([2269,12,31,23,59,59]), 'yyUNyy')

def getTimestamp(path):
	bigImg = Image.open(path)
	obj = bigImg._getexif()
	exifdate = None
	if obj:
		if 36867 in obj: exifdate = obj[36867] # milliseconds in obj[37521]
		if exifdate:
			arr = exifdate.split(" ")
			arr[0] = arr[0].replace(':','-')
			exifdate = ' '.join(arr)
	mdate = str(datetime.fromtimestamp(int(getmtime(path))))
	p = path.rindex('/')
	folderDate = getFileDate(path[0:p])
	fileDate = getFileDate(path[p:])
	if exifdate: return exifdate
	if fileDate: return fileDate + ' 00:00:00'
	if folderDate and folderDate <= mdate: return folderDate + ' 00:00:00'
	return mdate

def readFileIndex():
	with open(FILE_INDEX, 'r', encoding="utf8") as f:
		lines = f.readlines()
	res = {}
	for line in lines:
		line = line.strip()
		arr = line.split(' : ')
		res[arr[0]] = arr[1]
		if arr[1].startswith('files/') and not exists(PUBLIC + arr[1]):
			print('Missing file:',arr[1])
	return res

def tree(d,f):
	for path in d:
		if not is_jpg(path):
			f.write(path.replace('/',' • ')[3:] + '\n')

######################

start = time.time()

hash = {}
letters = list("+!§()0123456789_,.-¤")

md5Register = loadJSON(MD5) # givet md5key får man listan med sex element
cache = loadJSON(JSON + 'bilder.json')
fileIndex = readFileIndex()

a = flat(Original, {}) # Readonly!           Skickas INTE till GCS
b = flat(Home)   # Används bara för räkning. Skickas dock till GCS
c = flat(small)  # Används bara för räkning. Skickas dock till GCS
d = flatten(cache, {}) #                     Skickas till GCS

print()
ca = countFolders(a)
cb = countFolders(b)
cc = countFolders(c)
cd = countFolders(d)

print('Original:', len(a) - ca, 'images +', ca, 'folders')
print('Cache:   ', len(d) - cd, 'images +', cd, 'folders', )
print()
print('Home:    ', len(b),      'images')
print('Small:   ', len(c),      'images')

print()
resCache = compare2(a,d)

print()
for key in resCache['surplus'].keys(): print('Will delete:', key)
print()
for key in resCache['missing'].keys(): print('Will add:', key)

print('Readonly:', round(time.time()-start,3),'seconds')
print()
update = input('Update? (NO/Yes) ').upper()
update = update.startswith('Y')

if update:

	start = time.time()
	print()
	antal = expand(a,d)
	print()
	if antal['images'] > 0: print('Added:', antal['images'], 'images')

	antal = shrink(d,a)
	if antal['images'] > 0: print('Deleted:', antal['images'], 'images')

	if antal['keys'] > 0: print('Deleted:', antal['keys'], 'keys')

	with open(JSON + 'bilder.json',     'w', encoding="utf8") as f: dumpjson(cache,f)
	with open(JSON + 'file_index.json', 'w', encoding="utf8") as f: dumpjson(fileIndex,f)
	with open(MD5,                      'w', encoding="utf8") as f: dumpjson(md5Register,f)
	d = flatten(cache, {})  # Skickas till GCS
	with open(TREE,                     'w', encoding="utf8") as f:	tree(d, f)

	print()
	print(round(time.time() - start,3),'seconds')
