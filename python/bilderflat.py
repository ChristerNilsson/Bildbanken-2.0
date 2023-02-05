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
import yaml
from os import scandir, mkdir,rename
from os.path import exists, getsize,getmtime
from datetime import datetime
from PIL import Image
import hashlib
import shutil
import re
import codecs
from dateutil import parser

ALFABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'

QUALITY = 95
WIDTH = 475
YEAR = datetime.today().year

ROOT = "C:/github/2022-014-Bildbanken2/"
#ROOT = "C:/github/2022-014-Bildbanken2/experiment/"
#ROOT = "D:/"
Original = ROOT + "Original"       # cirka 2.000.000 bytes per bild (Readonly)
Home     = ROOT + "public/Home"    # cirka 2.000.000 bytes per bild
small    = ROOT + "public/small"   # cirka 	  25.000 bytes per bild
#JSON     = ROOT + "public/json/"  # cirka       120 bytes per bild (bilder.json)
JSON     = ROOT + "public/json/"   # cirka       120 bytes per bild (bilder.json)
MD5      = ROOT + 'MD5.json'       # cirka        65 bytes per bild
FILE_INDEX = JSON + 'file_index.txt'
PUBLIC    = ROOT + "public/"

def ass(a,b):
	if a == b: return
	print('assert failure')
	print('  ',a)
	print('  ',b)
	# assert(a==b)


def is_jpg(key): return key.endswith('.jpg') or key.endswith('.JPG')
def is_tif(key): return key.endswith('.tif') or key.endswith('.TIF')

def dumpjson(data,f):
	start = time.time()
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
	s = s.replace("],","],\n") # Varje key (katalog,fil) på egen rad.
	s = s.replace(":{",":\n{")
	s = s.replace('},"','},\n"')
	# s = s.replace('","','",\n"')
	f.write(s)
	print('json',time.time()-start)

def dumpyaml(data,f):
	start = time.time()
	s = yaml.dump(data)
	# s = s.replace(": {",":\n{")
	# s = s.replace('[\n','[')
	f.write(s)
	print('yaml',time.time()-start)

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

# def makeSmall(Original,Home,small,name):
#
# 	with open(Original+name,"rb") as f:
# 		data = f.read()
# 		md5hash = hashlib.md5(data).hexdigest()
#
# 	filename = "/" + md5hash + ".jpg"
# 	if md5hash in md5Register and exists(Home + filename) and exists(small + filename):
# 		lst = md5Register[md5hash]
# 		patch(cache, name, lst)
# 		return lst
#
# 	bigImg = Image.open(Original+name)
# 	bigSize = getsize(Original+name)
#
# 	if bigImg.width <= 2048:
# 		shutil.copyfile(Original + name, Home + "/" + md5hash + '.jpg')
# 	else:
# 		bigImg = bigImg.resize((2048, round(2048 * bigImg.height / bigImg.width)))
# 		bigImg.save(Home + "/" + md5hash + '.jpg',quality=QUALITY)
#
# 	smallImg = bigImg.resize((WIDTH, round(WIDTH*bigImg.height/bigImg.width)))
# 	smallImg.save(small + "/" + md5hash + '.jpg',quality=QUALITY)
# 	lst = [smallImg.width, smallImg.height, bigSize, bigImg.width, bigImg.height, md5hash, getTimestamp(name)]
# 	md5Register[md5hash] = lst
# 	patch(cache, name, lst)
# 	return lst

def makeSmall(Original,Home,small,name):

	with open(Original+name,"rb") as f:
		data = f.read()

	md5hash = hashlib.md5(data).hexdigest()
	# md5hash = md5hash[0:10]
	md5hash = codecs.encode(codecs.decode(md5hash, 'hex'), 'base64')
	md5hash = md5hash.decode("utf-8")
	md5hash = md5hash[0:6]
	md5hash = md5hash.replace('+','-').replace('/','_')

	ts = getTimestamp(Original+name).replace('-',' ').replace(':',' ').split(' ')
	pt = packedTime(ts[0],ts[1],ts[2],ts[3],ts[4],ts[5])

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

def fixMisspellings(root, path, namn,doit=False):

	namn1 = re.sub(".jpg", "", namn)
	namn1 = re.sub(".JPG", "", namn1)
	namn0 = namn1
	namn1 = re.sub("___", "__", namn1)
	namn1 = re.sub("__", "_", namn1)
	namn1 = re.sub("_ ","_",namn1)
	namn1 = re.sub(" _","_",namn1)
	namn1 = re.sub("  "," ",namn1)
	namn1 = re.sub("_Von_","_von_",namn1)

	if namn0 == namn1: return namn

	path1 = root + path + "/"
	counter = ""
	if exists(path1 + namn1 + '.jpg'):
		counter = 1
		while exists(path1 + namn1 + "-" + str(counter) + '.jpg'):
			counter += 1
	print("")
	print(path1 + namn)
	if counter == "":
		print(path1 + namn1 + '.jpg')
		if doit: rename(path1 + namn, path1 + namn1 + '.jpg')
	else:
		print(path1 + namn1 + "-" + str(counter) + '.jpg')
		if doit: rename(path1 + namn, path1 + namn1 + "-" + str(counter) + '.jpg')
	return namn1 + '.jpg'

def flat(root, res={}, path=""):
	ensurePath(root, path)
	for name in [f for f in scandir(root + "/" + path)]:
		namn = name.name
		path1 = path + "/" + namn
		# path1 = path1.replace(' ','_')
		if name.is_dir():
			res[path1] = ""
			flat(root, res, path1)
		elif is_jpg(namn):
			res[path1] = ""
		else:
			print("*** Ignored file:", "public/Home" + path1)
	return res

# sizes = []

def flatten(node, res={}, path=''):
	# global sizes
	for key in node:
		path1 = path + "/" + key
		if is_jpg(key):

			# sizes.append([node[key][2],path1])
			# if len(node[key]) == 5:
			# 	node[key].append(key)
			# getTimestamp(path1)

			res[path1] = node[key]
		else:
			res[path1] = ""
			match = re.search(r'_[LIR]\d\d\d\d\d', key)
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
#				if cimages == 0: res[path] = 0
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
			wordLower = word.lower()
			if len(word) > 1 and wordLower == word:
				hash[word] = hash[word]+1 if word in hash else 1
		if type(node[key]) is dict: flatWords(node[key])

def convert(hash):
	arr = []
	for key in hash.keys():
		arr.append([hash[key],key])
	arr = sorted(arr)
	return arr

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

def packedTime(*lst): # Klarar fram till 4108-01-29 07:32:15 med sekund-upplösning
	# Detta är EJ unix-tid. Pga av bugg i mktime relaterad till DST.
	lst = list(lst)
	lst[0] -= 1970
	lst[1] -= 1
	lst[2] -= 1
	unix = 0
	faktors = [9999,12,31,24,60,60]
	for i in range(6):
		unix = unix * faktors[i] + lst[i]
	res = ''
	for i in range(6):
		res = ALFABET[unix % 64] + res
		unix = unix // 64
	return res
ass(packedTime(1970, 1, 1, 0, 0, 0), '000000')
ass(packedTime(2023, 1,19,20, 8, 0), '1BEpMw')
ass(packedTime(2023, 2, 2,11,34,56), '1BIVzw')
ass(packedTime(2023, 2, 2,11,34,57), '1BIVzx')
ass(packedTime(2100, 1, 1, 0, 0, 0), '3V2ZM0')
ass(packedTime(2200, 1, 1, 0, 0, 0), '6UDJg0')
ass(packedTime(2300, 1, 1, 0, 0, 0), '9UcsM0')
ass(packedTime(2400, 1, 1, 0, 0, 0), 'cTNcg0')
ass(packedTime(3000, 1, 1, 0, 0, 0), 'uRdFg0')
ass(packedTime(3001, 1, 1, 0, 0, 0), 'uT8g80')
ass(packedTime(4000, 1, 1, 0, 0, 0), 'YMZ4g0')
ass(packedTime(4108, 1,29, 7,32,15), '______')

def unpack(packed):
	unix = 0
	for ch in packed : unix = unix * 64 + ALFABET.index(ch)
	res = []
	for x in [60,60,24,31,12,9999]:
		res.insert(0,unix % x)
		unix = unix // x
	res[0] += 1970
	res[1] += 1
	res[2] += 1
	return res
ass(unpack("000000"),[1970, 1, 1, 0, 0, 0])
ass(unpack("100000"),[2003, 5,28,13,37, 4])
ass(unpack("200000"),[2036,10,25, 3,14, 8])
ass(unpack("Z00000"),[4007,11, 8,14,41, 4])
ass(unpack("-00000"),[4041, 4, 5, 4,18, 8])
ass(unpack("_00000"),[4074, 9, 1,17,55,12])
ass(unpack("______"),[4108, 1,29, 7,32,15])

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


	# if exifdate and fileDate:
	# 	a = parser.parse(fileDate)
	# 	b = parser.parse(exifdate)
	# 	delta = (a-b).days
	# 	if abs(delta) > 1 :
	# 		print(delta, fileDate, exifdate, path)


	if exifdate: return exifdate
	if fileDate: return fileDate + ' 00:00:00'
	if folderDate and folderDate <= mdate: return folderDate + ' 00:00:00'
	# print(mdate,path)
	return mdate

def spaces2underscores(node,res={}):
	# if type(node) is list: return node
	for key in node:
		key1 = key.replace(' ','_')
		# res[key.replace(' ','_')] = spaces2underscores(node[key],res)
		if is_jpg(key1):
			res[key1] = node[key]
		else:
			res[key1] = {}
			res[key1]= spaces2underscores(node[key],res[key1])
	return res

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

def checkUniq(reg):
	hash = {}
	for key in reg:
		hash[key[0:9]] = 0 # uniq, but no margins
	return len(hash)

######################

start = time.time()

#getTimestamp('/2017/2017--2018 Allsvenskan/495_GM_Juan_Bellon_Lopez_2018-02-03.jpg')
#getTimestamp('/2022/2022-12-29 Stockholms Schackförbunds och Pia Cramlings tjejschacktävling i samband med Rilton/Vy-Rilton-tjejtävling_prisutdelning_6.Shira_Milikov_2022-12-29.jpg')

hash = {}
letters = list("+!§()0123456789_,.-¤")

md5Register = loadJSON(MD5) # givet md5key får man listan med sex element
#print(checkUniq(md5Register))
cache = loadJSON(JSON + 'bilder.json')
# cache = cache['root']
fileIndex = readFileIndex()

a = flat(Original, {}) # Readonly!           Skickas INTE till GCS
b = flat(Home)   # Används bara för räkning. Skickas dock till GCS
c = flat(small)  # Används bara för räkning. Skickas dock till GCS
d = flatten(cache, {}) #                     Skickas till GCS

# sizes.sort()
# for i in range(4000):
# 	print(sizes[i])

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
#for key in resCache['missing'].keys(): print('Missing:', key)
print()
#for key in resCache['surplus'].keys(): print('Surplus:', key)

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

	print()
	print(round(time.time() - start,3),'seconds')
