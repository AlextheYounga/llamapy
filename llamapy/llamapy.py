import os
import platform
import subprocess
import socket
from pathlib import Path
from openai import OpenAI
import threading

class LlamaPy(OpenAI):
	def __init__(self, api_key="llamapy", base_url=None, port=42424, *args):
		self.api_key = api_key
		self.port = port
		self.base_url = base_url or f"http://localhost:{port}/v1"
		self.platform = platform.system().lower()
		self.bindir = Path.home() / "localllm" / ("build/bin/" if self.platform != "win32" else "")
		os.environ.OPENAI_BASE_URL=self.base_url
		os.environ.OPENAI_API_KEY=self.api_key
		super().__init__(api_key=self.api_key, base_url=self.base_url, *args)


	def load(self, model_path: str):
		self.model = model_path
		server = threading.Thread(target=self.run_llamacpp_server)
		server.start()
		return self

	def run_llamacpp_server(self):
		# Check if the server is already running
		if self.server_already_running(self.port): 
			print(f"Server already running on port {self.port}")
			return
		
		# Ensure the file has the correct permissions to execute
		os.chmod(f"{self.bindir}/llama-server", 0o755)

		# Call the llama-server binary with the model path and port
		with open("logs/llamapy.log", "w") as log_file:
			print(f"Starting llamacpp server on port {self.port}")
			subprocess.call([f"{self.bindir}/llama-server", "-m", self.model, "--port", f"{self.port}"], stdout=log_file, stderr=log_file)

	def server_already_running(self, port: int):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			return s.connect_ex(("localhost", port)) == 0