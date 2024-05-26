class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		"""
        Initialize the Button object.

        :param image: The image to be displayed on the button. If None, the text will be used as the button.
        :param pos: A tuple (x, y) representing the position of the button's center.
        :param text_input: The text to be displayed on the button.
        :param font: The font used to render the text.
        :param base_color: The base color of the text.
        :param hovering_color: The color of the text when the button is hovered over.
        """
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		"""
        Update the button's appearance on the screen.

        :param screen: The screen surface to draw the button on.
        """
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		"""
        Check if the button is being clicked based on the mouse position.

        :param position: A tuple (x, y) representing the mouse position.
        :return: True if the button is clicked, False otherwise.
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		"""
        Change the color of the button text when hovered over.

        :param position: A tuple (x, y) representing the mouse position.
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)