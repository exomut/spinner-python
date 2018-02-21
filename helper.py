def is_in_rectangle(point, rectangle):
	"""
	Checks a touch point versus a scalable image rectangle
	accounting for scale as well.
	returns: True if the point is in the rectangles box. False if not.
	"""
	if (rectangle.position.x <= point.location.x <= rectangle.position.x + rectangle.size.width * rectangle.scale and
			rectangle.position.y <= point.location.y <= rectangle.position.y + rectangle.size.height * rectangle.scale):
				return True
	return False

