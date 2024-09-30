import os
import platform
import subprocess
import socket
from pathlib import Path
from openai import OpenAI
import threading

class LlamaPy(OpenAI):
	def __init__(self, *args):
		super().__init__(api_key="llamapy", *args)
		self.platform = platform.system().lower()
		self.bindir = Path.home() / "localllm" / ("build/bin/" if self.platform != "win32" else "")
		self.model = None
		self.port = None

	def load(self, model_path: str, port: int = 42424):
		self.model = model_path
		self.port = port
		server = threading.Thread(target=self.run_llamacpp_server)
		server.start()

	def run_llamacpp_server(self):
		# Check if the server is already running
		if self.server_already_running(self.port): 
			print(f"Server already running on port {self.port}")
			return
		
		# Ensure the file has the correct permissions to execute
		os.chmod(f"{self.bindir}/llama-server", 0o755)

		# TODO: Find a way to redirect the output to a log file
		# Call the llama-server binary with the model path and port
		with open("logs/server.log", "w") as log_file:
			print(f"Starting llamacpp server on port {self.port}")
			subprocess.call([f"{self.bindir}/llama-server", "-m", self.model, "--port", f"{self.port}"], stdout=log_file)

	def server_already_running(self, port: int):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			return s.connect_ex(("localhost", port)) == 0
