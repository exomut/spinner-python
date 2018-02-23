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
		self.textures = [
			'./images/board_four.png',
			'./images/board_six.png',
			'./images/board_ten.png'
			]
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
		sound.play_effect('game:Woosh_1')
		self.run_action(Action.sequence(
										Action.rotate_by(random.randint(100,300), 3, TIMING_EASE_OUT),
										Action.call(self.finish_spin)
										))
										
	def finish_spin(self):
		sound.play_effect('ui:switch2')
		
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
		
	def touch_check(self, touch):
		if(helper.is_in_rectangle(touch, self)):
			self.press_button()
			sound.play_effect('8ve:8ve-tap-warm')
			return True
		return False


class Game (Scene):
	def setup(self):
		
		# Setup up that shader for cool effects
		self.effect_node = EffectNode(parent=self)
		with open('filters.fsh') as f:
			self.effect_node.shader = Shader(f.read())
		self.effect_node.crop_rect = self.bounds
		# Set 'u_style' to '0' for no effects. 1 - 4 for effects
		self.effect_node.shader.set_uniform('u_style', 0)
		
		# Background image and scaling to match the screen in landscape mode
		self.background = SpriteNode(
			'./images/background.png', parent=self.effect_node)
		self.background.anchor_point = (0, 0)
		self.background.scale = self.size.w / self.background.size.w
		
		# Board and spinner setup and scaling
		self.board = Board(parent=self.effect_node)
		self.board.position = (self.size.w/2, self.size.h/2)
		self.board.scale = self.size.h / self.board.size.h
		
		self.spinner = Spinner(parent=self.board)
		
		# Menu Buttons
		self.change_spinner = Button(
			'./images/change_spinner_up.png',
			'./images/change_spinner_down.png', (0, 0), parent=self
			)
		self.change_board = Button(
			'./images/change_board_up.png',
			'./images/change_board_down.png', (self.size.w-100, 0), parent=self
			)

	def did_change_size(self):
		pass
	
	def update(self):
		pass
	
	def touch_began(self, touch):
		if (self.change_spinner.touch_check(touch)):
			self.spinner.change_spinner()
		elif (self.change_board.touch_check(touch)):
			self.board.change_board()
		else:
			self.spinner.spin()
			
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		self.change_spinner.release_button()
		self.change_board.release_button()

if __name__ == '__main__':
	run(Game(), show_fps=False, orientation=LANDSCAPE)
