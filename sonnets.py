import re
import json
from collections import defaultdict


with open('cmudict_abbr_js.json', 'r') as f:
	cmudict = json.load(f)

sonnet_text = open('pg1041.txt', encoding='utf-8').read()
sonnets = re.split(r'\n\s+[XVCIL]+\n', sonnet_text, flags=re.X)
sonnet_dict = {key:value for key, value in enumerate(sonnets)}

class Sonnet:
	
	def __init__(self, num):
		self.num = num
		self.text = sonnet_dict[num]
		self.fix_punct()
		self.get_lines()
		self.rhyme_dict = defaultdict(list)
		self.start_dict = defaultdict(list)
		self.show_rhymes_and_allit()
		self.label_rhymes_and_allit()
		
	
	def fix_punct(self):
		sonnet = self.text
		sonnet_no_punct = re.sub(r" '|'$", '', sonnet)
		sonnet_no_punct = re.sub(r"[,\.;!:?]", '', sonnet_no_punct)
		sonnet_no_punct = re.sub(r"'st", '', sonnet_no_punct)
		sonnet_no_punct = re.sub(r"'d", 'ed', sonnet_no_punct)
		self.sonnet_no_punct = sonnet_no_punct
		
	def get_lines(self):
		# self.lines = [Line(l.strip()) for l in self.text.split('\n') if re.search('\w', l)]
		self.lines_clean = [l.strip() for l in self.text.split('\n') if re.search('\w', l)]
		self.lines = [Line(l.strip()) for l in self.sonnet_no_punct.split('\n') if re.search('\w', l)]
		for line in self.lines[-2:]:
			line.final_couplet = True
	
	# def get_words(self):
	# 	self.words = [[w for w in l.text.split(' ')] for l in self.lines]
	# 	self.words_clean = [[Word(w.upper()) for w in l.text.split(' ')] for l in self.lines_clean]
		
	# def get_arp(self):
	# 	self.arp = [[cmudict[w] if w in cmudict else '**' + w for w in l] for l in self.words_clean]
	# 	print(self.arp)
		
	# def get_stresses(self, arp_word):
	# 	return [int(s) for s in re.findall('\d', arp_word)]
	
	# def get_stress_list(self):
	# 	self.stresses = [[self.get_stresses(w) for w in l] for l in self.arp]
	
	# def end_rhyme(self, arp_word):
	# 	try:
	# 		return re.search(r'\w+\d\D+$|\w+\d$', arp_word).group()
	# 	except:
	# 		return ''
	#
	# def start_sound(self, arp_word):
	# 	try:
	# 		return arp_word.split(' ')[0]
	# 	except:
	# 		return ''
		
	# def show_rhymes_and_allit(self):
	# 	for i in range(len(self.words)):
	# 		words = self.words[i]
	# 		for j in range(len(self.words[i])):
	# 			word = self.words[i][j]
	# 			arp = self.arp[i][j]
	# 			rhyme = self.end_rhyme(arp)
	# 			start = self.start_sound(arp)
	# 			self.rhyme_dict[rhyme].append([word, (i, j)])
	# 			self.start_dict[start].append([word, (i, j)])
	# 	print(*self.rhyme_dict.items(), sep='\n')
	# 	print(*self.start_dict.items(), sep='\n')
		
	def show_rhymes_and_allit(self):
		for i, l in enumerate(self.lines):
			for j, w in enumerate(l.words):
				self.rhyme_dict[w.end_rhyme].append([w, (i, j)])
				self.start_dict[w.start].append([w, (i, j)])
	
	def label_rhymes_and_allit(self):
		rhymes = sorted([x for x in self.rhyme_dict.items() if len(set([str(w[0]) for w in x[1]]))>1 if x[0]],
		             key=lambda x: len(x[1]))[::-1]
		for n, rhyme in enumerate(rhymes):
			rhyme_num = n + 1
			for w in rhyme[1]:
				w[0].rhyme_num = rhyme_num
				# print(w, w[0].rhyme_num)
			
	def return_word_objects(self):
		return [[(w, w.text, w.stress_count, w.rhyme_num) for w in l.words] for l in self.lines]
		
		
		
		

class Line:
	def __init__(self, text):
		self.text = text
		self.get_words()
		self.final_couplet = False
		self.stress_pattern = [w.stresses for w in self.words]
		self.guess_stress()
	
	def get_words(self):
		self.words = [Word(w.upper()) for w in self.text.split(' ')]
		self.words[-1].line_end = True
	
	def guess_stress(self):
		
		wild = 10 - sum([len(sp) for sp in self.stress_pattern])
		unmatched = [w for w in self.words if w.arp_word == '**']
		if len(unmatched) > 0:
			guess = wild / len(unmatched)
			for w in unmatched:
				w.stress_count = guess
	

class Word:
	
	def __init__(self, text):
		self.text = text
		self.arp_word = cmudict[text] if text in cmudict else '**'
		self.stresses = [int(s) for s in re.findall('\d', self.arp_word)]
		self.stress_count = len(self.stresses)
		self.end_rhyme = self.end_rhyme()
		self.start = self.start_sound()
		self.line_start = False
		self.line_end = False
		self.rhyme_num = 0
	
	def __repr__(self):
		return self.text
		
	def end_rhyme(self):
		try:
			return re.search(r'\w+\d\D+$|\w+\d$', self.arp_word).group()
		except:
			return ''
	
	def start_sound(self):
		try:
			return self.arp_word.split(' ')[0]
		except:
			return ''
	pass



	
	
	
		
		
# n = 102
# print(sonnet_dict[n])

# sonnet = sonnet_dict[n]
#
# sonnet_no_punct = re.sub(r" '|'$", '', sonnet)
# sonnet_no_punct = re.sub(r"[,\.;!:?]", '', sonnet_no_punct)
# sonnet_no_punct = re.sub(r"'st", '', sonnet_no_punct)
# sonnet_no_punct = re.sub(r"'d", 'ed', sonnet_no_punct)
#
# lines = [l.strip() for l in sonnet_no_punct.split('\n') if re.search('\w',l)]
#
# words = [[w.upper() for w in l.split(' ')] for l in lines]
#
# arp = [[cmudict[w] if w in cmudict else '**'+w for w in l] for l in words]
#
# def stress_list_int(arp_word_string):
# 	'''takes arp_word as single string and returns list of stresses'''
# 	return [int(s) for s in re.findall('\d', arp_word_string)]
#
# for l in arp:
# 	print(l)
# 	stresses = [stress_list_int(w) for w in l]
# 	print(stresses)
# 	print(len([x for y in stresses for x in y]))

snt = Sonnet(103)
# snt.show_rhymes_and_allit()
# print(*snt.rhyme_dict.items(), sep='\n')
# print(snt.sonnet_no_punct)
# snt.label_rhymes_and_allit()
print(snt.return_word_objects())
# print(*[x for x in snt.rhyme_dict.items() if len(x[1])>1 and x[0]], sep='\n')
# print(*sorted([x for x in snt.rhyme_dict.items() if len(set([str(w[0]) for w in x[1]]))>1 if x[0]], key=lambda x: len(x[
# 	                                                                                                                  1])),
#       sep='\n')

# print(snt.sonnet_no_punct)
# for x in snt.rhyme_dict.items():
# 	print([w[0] for w in x[1]], set([str(w[0]) for w in x[1]]))
# print(*snt.stresses, sep='\n')
# print(cmudict['HAPPY'])
# print(*snt.arp, sep='\n')
# print(snt.get_end_rhymes())
# print(list(zip(snt.arp, snt.words)))
# snt.show_rhymes_and_allit()
# print([w.arp_word for l in snt.lines for w in l.words])
# for snt_num in sonnet_dict:
# 	Snt = Sonnet(snt_num)
# 	for line in Snt.lines:
# 		print(line.stress_pattern)
# 		if line.final_couplet == True:
# 			print(line.text)

# wobs = [[(w, w.text, w.stress_count, w.rhyme_num) for w in l.words] for l in snt.lines]
# print(wobs)