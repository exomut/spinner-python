from scene import *
import Image
import sound
import random
import math
import helper
A = Action


class Spinner (SpriteNode):
	def __init__(self, *args, **kwargs):
		super(Spinner, self).__init__(*args, **kwargs)
		self.spin_speed = 0
		self.texture = Texture('./images/spinner2.png')
	
	def spin(self):
		self.rotation += self.spin_speed
		

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
		self.board = SpriteNode('./images/board_ten.png', parent=self.background)
		self.board.scale = 1.5
		self.board.position = (self.size.w/2, self.size.h/2)
		self.spinner = Spinner(parent=self.board)
		
		# Menu Buttons
		self.change_spinner = Button('./images/change_spinner_up.png', './images/change_spinner_down.png', (100, 100), parent=self)

	def did_change_size(self):
		pass
	
	def update(self):
		self.spinner.spin()
	
	def touch_began(self, touch):
		sound.play_effect('game:Woosh_2')
		self.spinner.spin_speed = 1
		self.change_spinner.run_on_touch(touch)
			
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		self.change_spinner.release_button()
		self.spinner.spin_speed = 0

if __name__ == '__main__':
	run(Game(), show_fps=True)
