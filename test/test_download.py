import os
import json
from llamapy.llamacpp import LlamaCpp

class LLamaCppMock(LlamaCpp):
	def __init__(self):
		super().__init__()
	
	def fetch_github_releases(self):
		return json.loads(open("test/fixtures/releases.json").read())

def test_download():
	llamacpp = LLamaCppMock()
	llamacpp.download()