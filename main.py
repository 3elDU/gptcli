#! /usr/bin/env python3

import os
import subprocess
import openai
import argparse

tokens_consumed: int = 0

def main(args):
  global tokens_consumed

  message_history = [
    {"role": "user", "content": "Convert natural language into commands in terminal\nPrefix all runnable commands by '!' sybmol, and print them on separate line\nBe short and concise"},
    # {"role": "user", "content": "Convert natural language into terminal commands, and describe their output."},
    {"role": "user", "content": "What system am I running on?"},
    {"role": "assistant", "content": "This command will print the kernel you're running:\n!uname -a"},
    {"role": "system", "content": "Linux ebk1040g3 6.2.1-arch1-1 #1 SMP PREEMPT_DYNAMIC Sun, 26 Feb 2023 03:39:23 +0000 x86_64 GNU/Linux"},
    {"role": "assistant", "content": "Your computer is running Arch GNU/Linux 6.2.1"},
    # {"role": "user", "content": args.prompt},
  ]

  while True:
    prompt = input("prompt: ")
    message_history.append({"role": "user", "content": prompt})

    # 1st stage ( AI parsing natural language, converting it into shell command )
    completion = openai.ChatCompletion.create(
      model=args.model,
      temperature=args.temperature,
      messages=message_history
    )
    print(completion.choices[0].message.content)
    tokens_consumed += completion.usage.completion_tokens

    commands_to_run: list[str] = []
    lines: list[str] = completion.choices[0].message.content.split("\n")
    for line in lines:
      if not line.startswith("!"):
        continue

      command = line[1:]
      commands_to_run.append(command)

    print(commands_to_run)

    # for i, command in enumerate(commands_to_run):
    #   print(f"{i}; {command}")
    answer = input("Is it ok to run those commands? y/n/s: ")

    if answer.lower() == 's':
      continue
    if answer.lower() != 'y':
      exit()

    message_history.append(completion.choices[0].message)

    for command in commands_to_run:
      # 2nd stage ( running the command )
      output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
      # print(output)
      message_history.append({
        "role": "system",
        "content": output
      })
      print(output)

    # 3rd stage ( AI parsing the command output )
    completion = openai.ChatCompletion.create(
      model=args.model,
      temperature=args.temperature,
      messages=message_history
    )
    tokens_consumed += completion.usage.completion_tokens

    print(completion.choices[0].message.content)

  # for choice in completion.choices:
  #   print(choice.message.content, '\n\n')

  # print("tokens consumed:", tokens_consumed)

if __name__ == '__main__':
  openai.api_key = os.getenv("OPENAI_API_KEY")

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--temperature', help="How random the answer should be. Values from 0 to 2", type=float, default=0)
  parser.add_argument('-m', '--model', help="Model to use", default="gpt-3.5-turbo")
  # parser.add_argument('prompt')

  args = parser.parse_args()
  try:
    main(args)
  except KeyboardInterrupt:
    print("\n", tokens_consumed)
