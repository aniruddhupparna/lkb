from requests import post
import os

# API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def chat_with_hf_model(message):
	token = os.getenv('HF_TOKEN')
	headers = {"Authorization": f"Bearer {token}"}
	response = post(API_URL, headers=headers, json={"inputs": message})
	result_json =  response.json()
	if result_json:
		response_text =  result_json[0].get('generated_text', "An error occurred! Please contact lkb's developer")
		return response_text
	return "No response from server"