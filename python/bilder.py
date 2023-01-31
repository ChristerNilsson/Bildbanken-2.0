# Om small eller bilder.js saknas produceras små bilder i den katalogen och dimension uppdateras
# Därefter sammanställs bilder.js som omfattar ALLA kataloger, i variabeln Home.

import json
import time
from os import scandir,mkdir
from os.path import exists,getsize
from PIL import Image # Pillow

USE_CACHE = False

WIDTH = 475
ROOT = "C:\\github\\2022-011-Bildbanken-svelte\\public\\"

antal = 0

def dumpjson(data,f):
	json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

def pop(path):
	arr = path.split('\\')
	arr.pop()
	return "\\".join(arr)

def makeSmall(entry):
	#print('.',end="")
	big = Image.open(entry.path)
	bigSize = getsize(entry.path)
	small = big.resize((WIDTH, round(WIDTH*big.height/big.width)))
	p = pop(entry.path)
	if not exists(p):	mkdir(p)
	small.save(pop(entry.path).replace("Home","small") + '\\' + entry.name)
	return [small.width, small.height, bigSize, big.width, big.height]

def readrecurs(parent,level):
	global antal
	res = {}

	if not exists(ROOT + "\\small\\"+parent): mkdir(ROOT + "\\small\\"+parent)

	if USE_CACHE and exists(ROOT + "\\small" + parent +  "\\bilder.js"):
		with open(ROOT + "\\small" + parent + '\\bilder.js', 'r', encoding="utf8") as f:
			js = json.loads(f.read())
			antal += len(js)

	else:
		names = [f for f in scandir(ROOT + "Home" + parent)]
		for name in names:
			if name.name == 'bilder.js': continue
			# print("  " * level,name)
			if name.is_dir():
				#res[name.name] = readrecurs(parent + "\\" + name.name,level+1) # path
				readrecurs(parent + "\\" + name.name,level+1) # path
			else: # .jpg
				res[name.name] = makeSmall(name)
		if len(res) > 0:
			print('\n',len(res),'thumbnails written for',parent)
			with open(ROOT + '\\small' + parent + '\\bilder.js', 'w', encoding="utf8") as f:
				dumpjson(res,f)
	return res

start = time.time()
Home = readrecurs("\\",0)

with open(ROOT + "bilder.js", 'w', encoding="utf8") as f:
	f.write('Home=')
	dumpjson(Home, f)

print(antal)
print(round(time.time() - start,3),'seconds')







#from PyPDF2 import PdfReader
# def read_pdf() :
# 	#reader = PdfReader("Swade_PhD.pdf")
# 	reader = PdfReader("SSF.pdf")
# 	hash = {}
# 	for page in reader.pages:
# 		words = page.extract_text()
# 		words = words.replace("(", " ")
# 		words = words.replace(")", " ")
# 		words = words.replace("[", " ")
# 		words = words.replace("]", " ")
# 		words = words.replace(".", " ")
# 		words = words.replace(",", " ")
# 		words = words.replace("'", " ")
# 		words = words.replace("-", " ")
#
# 		words = words.replace("/", " ")
# 		words = words.replace('"', " ")
# 		words = words.replace("`", " ")
# 		words = words.replace(":", " ")
# 		words = words.replace("?", " ")
# 		words = words.replace("!", " ")
#
# 		words = words.lower()
#
# 		for word in words.split():
# 			if word in hash:
# 				hash[word] = hash[word]+1
# 			else:
# 				hash[word] = 1
#
#
# 	print(len(hash))
# 	print(hash)
# 	s =""
# 	for key in hash:
# 		s += ' ' + key
#
# 	print(len(s))
# 	print(s)

# read_pdf()
