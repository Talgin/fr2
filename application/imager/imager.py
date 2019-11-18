import cv2

class imViewer:
	def __init__(self, rect_dimension, color):
		self.rect_dimension = rect_dimension
		self.color = color

	def drawRect(self, img, rect_x, rect_y, width, height, border):
		if self.color == 0:
			color = (255,0,0)
		elif self.color == 1:
			color = (0,255,0)
		else:
			color = (0,0,255)
		cv2.rectangle(img, (rect_x, rect_y), (rect_x + width, rect_y + height), color, border)

		return img