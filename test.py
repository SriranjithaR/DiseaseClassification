import re
#create a class ; needed later
class PhraseObj(object):
	def __init__(self, phrase=None, distype=None) :
		self.phrase = phrase
		self.distype = distype

#Read all lines in the abstract
text = ''.join(open('labeled_abstracts.txt').readlines())
sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

#Collect sentences with cure,prevent and side effect information
#and write to new file
rts = open('relaventTaggedSentences.txt','w+')
for sentence in sentences:
	if ("<DIS>" in sentence and "<TREAT>" in sentence ) :
		print >> rts, sentence + "** CURE ** \n"
	if  ("<DIS_PREV>" in sentence and "<TREAT_PREV>" in sentence):
		print >> rts, sentence + "** PREVENT ** \n"
	if ("<DIS_SIDE_EFF>" in sentence and "<TREAT_SIDE_EFF>" in sentence):
		print >> rts, sentence + "** SIDE_EFFECT ** \n"

#Get the phrases within the tags alone
text = ''.join(open('relaventTaggedSentences.txt').readlines())
sentences = text.split("\n")
p = re.compile(r'<DIS.*>.*</DIS.*>')
phrases = []
for sentence in sentences:
	if "** CURE **" in sentence:
		diseaseType = "CURE"
	elif "** PREVENT **" in sentence:
		diseaseType = "PREVENT"
	else:
		diseaseType = "SIDE_EFFECT"

	wordsWithinTags = p.findall(sentence)
	for word in wordsWithinTags:
		word = word.replace("<DIS>"," ")
		word = word.replace("<TREAT>"," ")
		word = word.replace("<DIS_PREV>"," ")
		word = word.replace("<TREAT_PREV>"," ")
		word = word.replace("<DIS_SIDE_EFF>"," ")
		word = word.replace("<TREAT_SIDE_EFF>"," ")
		word = word.replace("</DIS>"," ")
		word = word.replace("</TREAT>"," ")
		word = word.replace("</DIS_PREV>"," ")
		word = word.replace("</TREAT_PREV>"," ")
		word = word.replace("</DIS_SIDE_EFF>"," ")
		word = word.replace("</TREAT_SIDE_EFF>"," ")
		word = re.sub(r'<(/)?DIS.*>'," ",word)
		word = re.sub(r'<(/)?YES>'," ",word)
		phrases.append(PhraseObj(word,diseaseType))

allPhrases = []
for phrase in phrases:
	print phrase.phrase + ":" + phrase.distype
	allPhrases.append(phrase.phrase)

#Create a dict : a bag of words contained in the sentences
dict = {}
for phrase in allPhrases:
	for word in phrase.split(' '):
		word = word.replace(",","")
		word = word.replace("(","")
		word = word.replace(")","")
		if re.match(r'^([a-zA-Z](\')?)+$',word):
			if dict.has_key(word.lower()):
				dict[word.lower()] = dict[word.lower()] + 1
			else :
				dict[word.lower()] = 1

print len(dict)

#Read stop words file - stop words are common english words of no use to clinical mining
stopWords = ''.join(open('StopWords.txt').readlines())
stopWords = stopWords.split("\n")

#Eliminate words indict that are stop words
for key in dict.keys():
	if (key in stopWords):
		del dict[key]
	elif dict[key]<2 or len(key)<4:
		del dict[key]

print len(dict)


#Alphabestically sort the keys
allKeys = dict.keys()
allKeys.sort()
for key in allKeys:
	print key+" : "+str(dict[key])


#Creating feature vector
fv = open("feature_vector.csv","w")

fstr = ""
for key in allKeys:
	key = key.replace("'","")
	print key
	fstr = fstr + key +","
fstr = fstr +"distype"
print >> fv,fstr

for i in range(len(phrases)):
	ph = phrases[i].phrase
	fstr = ""
	for key in allKeys:
		if key in ph:
			fstr = fstr + "1,"
		else:
			fstr = fstr + "0,"
	fstr = fstr + phrases[i].distype
	print >> fv,fstr
