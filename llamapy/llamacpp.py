import platform
import requests
import re
import os
import GPUtil
from fake_useragent import UserAgent
from pathlib import Path
import tqdm
import zipfile

# Ensures that the llama.cpp binary is downloaded and ready to use
# Checks to see if the binary is already downloaded, if not, downloads it
# https://github.com/ggerganov/llama.cpp

class LlamaCpp:
	def __init__(self):
		self.homedir = Path.home() / "localllm"
		self.url = "https://api.github.com/repos/ggerganov/llama.cpp/releases/latest"
	
	def fetch_github_releases(self):
		response = requests.get(self.url)
		response.raise_for_status()  # Ensure we handle HTTP errors
		return response.json()
	
	def releases(self):
		current_platform = platform.system().lower()
		current_arch = platform.machine().lower()
		current_gpu = self.get_gpu()

		response = self.fetch_github_releases()		
		assets = response.get('assets', [])
		releases = [self.extract_info(asset) for asset in assets]

		match = self.search_releases(releases, {
			'platform': current_platform,
			'arch': current_arch,
			'gpu': current_gpu
		})

		return match

	def extract_info(self, asset):
		url = asset.get('browser_download_url', '')
		info = {'url': url}

		info['platform'] = self.extract_platform(url)
		info['arch'] = self.extract_arch(url)
		info['gpu'] = self.extract_gpu(url, info.get('arch'))

		return info

	def extract_platform(self, url):
		if re.search(r'macos', url, re.IGNORECASE):
			return 'darwin'
		elif re.search(r'win', url, re.IGNORECASE):
			return 'win32'
		elif re.search(r'ubuntu', url, re.IGNORECASE):
			return 'linux'
		return None

	def extract_arch(self, url):
		if re.search(r'arm64', url, re.IGNORECASE):
			return 'arm64'
		elif re.search(r'x64', url, re.IGNORECASE):
			return 'x64'
		return None

	def extract_gpu(self, url, arch):
		if re.search(r'-cuda-', url, re.IGNORECASE):
			return 'nvidia'
		elif arch == 'arm64':
			return 'apple'
		return None

	def search_releases(self, releases, machine):
		for release in releases:
			if all(release.get(key) == value for key, value in machine.items()):
				return release
		return None

	def get_gpu(self):
		gpus = GPUtil.getGPUs()
		if not gpus:
			return "apple"

		for gpu in gpus:
			if re.search(r'nvidia', gpu.name, re.IGNORECASE):
				return "nvidia"
			elif re.search(r'amd|advanced micro devices', gpu.name, re.IGNORECASE):
				return "amd"
			elif re.search(r'apple', gpu.name, re.IGNORECASE):
				return "apple"

		return gpus[0].name if gpus else None
	
	def download(self):
		zip_path = self.homedir / "llamacpp.zip"
		if os.path.exists(zip_path):
			return
		
		release = self.releases()
		if not release: 
			raise Exception("no valid release")

		url = release['url']
		# user_agent = UserAgent()

		print(f"Downloading {url}")
		response = requests.get(url, stream=True)
		if response.status_code != 200:
			raise Exception(f"Download Error: {response.status_code}")
				
		total_size = int(response.headers.get('content-length', 0)) # Get the total file size from the 'content-length' header				
		chunk_size = 1024 # Define the chunk size (in bytes) for each iteration of the loop
		
		with open(zip_path, 'wb') as f:
			for data in tqdm.tqdm(response.iter_content(chunk_size=chunk_size), total=total_size//chunk_size, unit='KB'):
				f.write(data)

		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(self.homedir)