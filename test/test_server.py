from llamapy.llamapy import LlamaPy


def test_server():
	lpy = LlamaPy()
	model = 'some_model/path'
	lpy.load(model)