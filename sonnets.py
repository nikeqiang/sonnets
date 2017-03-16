import re
import json
from collections import defaultdict, Counter


with open('cmudict_abbr_js.json', 'r') as f:
	cmudict = json.load(f)

sonnet_text = open('pg1041.txt', encoding='utf-8').read()
sonnets = re.split(r'\n\s+[XVCIL]+\n', sonnet_text, flags=re.X)
sonnet_dict = {key:value for key, value in enumerate(sonnets) if key!=0}

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
		self.lines_clean = [l.strip() for l in self.text.split('\n') if re.search('\w', l)]
		self.lines = [Line(l.strip()) for l in self.sonnet_no_punct.split('\n') if re.search('\w', l)]
		for line in self.lines[-2:]:
			line.final_couplet = True
	

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
		
		allit = sorted([x for x in self.start_dict.items() if len(set([(str(w[0]), str(w[1][0])) for w in x[1]])) > 1
		                if x[
			0]],
		                key=lambda x: len(x[1]))[::-1]
		for n, allit in enumerate(allit):
			allit_num = n + 1
			for w in allit[1]:
				w[0].allit_num = allit_num
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
		self.get_syl_num()
	
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
	
	def get_syl_num(self):
		syl_num = 1
		for word in self.words:
			word.syl_number = int(syl_num)
			syl_num += word.stress_count
	

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
		self.allit_num = 0
		self.syl_number = 0
	
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





# rhyme_location = Counter()
#
# for s, sonn in sonnet_dict.items():
# 	print('Sonnet ', s)
# 	snt_obj = Sonnet(s)
# 	for n, l in enumerate(snt_obj.lines):
# 		for w in l.words:
# 			print(w.text, 'syle number: ',  w.syl_number)
# 			if w.rhyme_num != 0:
# 				rhyme_location[(n, w.syl_number)] += 1
#
# print(rhyme_location.items())
# print(sorted(rhyme_location.items(), key=lambda x: x[1]))
# print(sonnet_dict.items())

