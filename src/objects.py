class Token:
	def __init__(self) -> None:
		self.id = 0
		self.form = "_"
		self.lemma = "_"
		self.upos = "_"
		self.feats = {}
		self.head = 0
		self.deprel = 0
		self.misc = {}

class Sentence:
	def __init__(self) -> None:
		self.metadata = {}
		self.tokenslist = []
		self.cur_id = 1

	def add_token(self, token) -> None:
		token.id = self.cur_id
		self.tokenslist.append(token)
		self.cur_id += 1