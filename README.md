# gptcli

Use ChatGPT in CLI.  
The main idea is to be able to ask terminal-related questions, and instantly get back terminal commands, which you can execute, and get help from AI on their output.  

## About AI correctness
It can sometimes be very dumb, provide broken or dangerous commands, or all at once. I do not take any responsibility about AI accidentally taking over the world.

## Before running
You need OpenAI api key to use this. It is free and can be obtained [here](https://platform.openai.com/account/api-keys)  
After obtaining it, add it to `OPENAI_API_KEY` environment variable. You can also add this to your ~/.bashrc or ~/.zshenv to make this permanent:
```sh
export OPENAI_API_KEY="your_key_here"
```

## Running
- Make a virtual environment (optional)  
	```sh
	python3 -m venv venv
	source venv/bin/activate
	```
- Install requirements
	```sh
	pip install -r requirements.txt
	```
- Run
	```sh
	./gptcli
	```
