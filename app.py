from flask import Flask, render_template, request
from sonnets import *

app = Flask(__name__)

colors = '''#f0f0f0 #17becf #dbdb8d #bcbd22 #c7c7c7 #7f7f7f #f7b6d2 #e377c2 #c49c94 #8c564b #c5b0d5 #9467bd #ff9896 #d62728 #98df8a #2ca02c #ffbb78 #ff7f0e #aec7e8 #1f77b4'''.split(' ')

color_dict = {n: color for n, color in enumerate(colors)}

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
	sonnet_num = 20
	if request.method == "POST":
		sonnet_num = request.form['sonnet_num']
		print(sonnet_num)
	snt_obj = Sonnet(int(sonnet_num))
	wobs = [[(w, w.text, w.stress_count, color_dict[w.rhyme_num]) for w in l.words] for l in snt_obj.lines]
	print(wobs)
	return render_template('index.html', words=wobs)

if __name__ == '__main__':
	app.debug = True
	app.run()
	
	#
	# def __init__(self, text):
	# 	self.text = text
	# 	self.arp_word = cmudict[text] if text in cmudict else '**'
	# 	self.stresses = [int(s) for s in re.findall('\d', self.arp_word)]
	# 	self.stress_count = len(self.stresses)
	# 	self.end_rhyme = self.end_rhyme()
	# 	self.start = self.start_sound()
	# 	self.line_start = False
	# 	self.line_end = False
	# 	self.rhyme_num = 0