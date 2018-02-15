from scene import *
import Image
import sound
import random
import math
A = Action


class Game (Scene):
	def setup(self):
		self.board = SpriteNode('./images/board_ten.png', parent=self)
		self.board.scale = 1.5
		self.board.position = (self.size.w/2, self.size.h/2)
		
		self.spinner = SpriteNode('./images/spinner1.png', parent=self.board)
		# self.spinner.scale = self.board.scale
	
	def did_change_size(self):
		pass
	
	def update(self):
		self.spinner.rotation += 1
	
	def touch_began(self, touch):
		pass
			
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

if __name__ == '__main__':
	run(Game(), show_fps=True)
