from llamapy.llamapy import LlamaPy
from pathlib import Path

def test_server():
	lpy = LlamaPy()
	llm_dir = Path.home() / "localllm"
	model = f'{llm_dir}/models/microsoft/Phi-3-mini-4k-instruct-q4.gguf'
	lpy.load(model)