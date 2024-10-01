from llamapy.llamapy import LlamaPy
from pathlib import Path

def test_chat():
	lpy = LlamaPy()
	llm_dir = Path.home() / "localllm"
	model = f'{llm_dir}/models/microsoft/Phi-3-mini-4k-instruct-q4.gguf'
	client = lpy.load(model)

	messages = [
			{ "role": "system", "content": "You are a helpful assistant." },
			{ "role": "user", "content": "Hello!" }
		]

	completion = client.chat.completions.create(
		model="Phi-3-mini-4k-instruct-q4.gguf",
		messages=messages
		)

	print(completion.choices)