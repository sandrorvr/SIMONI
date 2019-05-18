from pynput.keyboard import Key, Listener


class Keyload():
	def __init__(self):
		self.chave = 1
		with Listener(on_release=self.on_release) as listener:
			listener.join()

	def on_release(self,key):
		if key == Key.esc:
			self.chave=key
			return False

