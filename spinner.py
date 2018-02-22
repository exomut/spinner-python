from scene import *
import Image
import sound
import random
import math
import helper
A = Action


class Board (SpriteNode):
	def __init__(self, *args, **kwargs):
		super(Board, self).__init__(*args, **kwargs)
		self.textures = ['./images/board_four.png', './images/board_six.png', './images/board_ten.png']
		self.current_board = 0
		self.set_board_texture()
		
	def change_board(self):
		if (self.current_board < len(self.textures)-1):
			self.current_board += 1
		else:
			self.current_board = 0
		self.set_board_texture()
			
	def set_board_texture(self):
		self.texture = Texture(self.textures[self.current_board])


class Spinner (SpriteNode):
	def __init__(self, *args, **kwargs):
		super(Spinner, self).__init__(*args, **kwargs)
		self.textures = ['./images/spinner1.png', './images/spinner2.png']
		self.current_spinner = 0
		self.set_spinner_texture()
	
	def spin(self):
		self.run_action(Action.rotate_by(random.randint(1,10)+100, 3, TIMING_EASE_OUT))
		
	def change_spinner(self):
		if (self.current_spinner < len(self.textures)-1):
			self.current_spinner += 1
		else:
			self.current_spinner = 0
		self.set_spinner_texture()
			
	def set_spinner_texture(self):
		self.texture = Texture(self.textures[self.current_spinner])
		

class Button (SpriteNode):
	def __init__(self, texture_released, texture_pressed, position, parent):
		super(Button, self).__init__(texture_released, parent=parent)
		self.texture_released = texture_released
		self.texture_pressed = texture_pressed
		self.position = position
		self.anchor_point = (0, 0)
		self.texture = Texture(self.texture_released)
		
	def release_button(self):
		self.texture = Texture(self.texture_released)
		
	def press_button(self):
		self.texture = Texture(self.texture_pressed)
		
	def run_on_touch(self, touch):
		if(helper.is_in_rectangle(touch, self)):
			self.press_button()
			return True
		return False


class Game (Scene):
	def setup(self):
		# Setup up that shader for cool effects
		self.effect_node = EffectNode(parent=self)
		with open('filters.fsh') as f:
			self.effect_node.shader = Shader(f.read())
		self.effect_node.crop_rect = self.bounds
		self.effect_node.shader.set_uniform('u_style', 0)
		
		self.background = SpriteNode(
			'./images/background.png', parent=self.effect_node)
		self.background.anchor_point = (0, 0)
		
		self.board = Board(parent=self.background)
		self.board.scale = 1
		self.board.position = (self.size.w/2, self.size.h/2)
		self.spinner = Spinner(parent=self.board)
		
		# Menu Buttons
		self.change_spinner = Button(
			'./images/change_spinner_up.png',
			'./images/change_spinner_down.png', (0, 0), parent=self
			)
		self.change_board = Button(
			'./images/change_board_up.png',
			'./images/change_board_down.png', (800, 0), parent=self
			)

	def did_change_size(self):
		pass
	
	def update(self):
		pass
	
	def touch_began(self, touch):
		if (self.change_spinner.run_on_touch(touch)):
			self.spinner.change_spinner()
		elif (self.change_board.run_on_touch(touch)):
			self.board.change_board()
		else:
			self.spinner.spin()
			sound.play_effect('game:Woosh_2')
			
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		self.change_spinner.release_button()
		self.change_board.release_button()
		self.spinner.spin_speed = 0

if __name__ == '__main__':
	run(Game(), show_fps=True)
