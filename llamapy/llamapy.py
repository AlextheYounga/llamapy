from openai import OpenAI
import subprocess
import socket
from pathlib import Path

class LlamaPy(OpenAI):
	def __init__(self, *args):
		super().__init__(*args)
		self.bindir = Path.home() / "localllm" / ("build/bin" if self.platform != "win32" else "")

	def run(self, model_path: str, port: int = 42424):
		if self.server_already_running(port):
			return
		subprocess.run(["llama-server", "-m", model_path, "--port", port])

	def server_already_running(self, port: int):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			try:
				s.bind(("0.0.0.0", port))
			except socket.error:
				return True
		return False
