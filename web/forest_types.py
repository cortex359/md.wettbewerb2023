class Tree:
	name: str = ""
	radius: float = 0.0
	index: int = 0
	counter: int = 0

	def __init__(self, name: str, radius: float, index: int = 0):
		self.name = name
		self.radius = radius

	def count(self):
		self.counter += 1

	def __str__(self):
		return f'{self.name:15s} {self.radius:4.1f} {self.counter:8d}'
