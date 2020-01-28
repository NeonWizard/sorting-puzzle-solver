class Action:
	def __init__(self, vial, vialDest):
		self.vial = vial
		self.vialDest = vialDest

	def __str__(self):
		return "Pop vial #{}, place in vial #{}".format(self.vial+1, self.vialDest+1)