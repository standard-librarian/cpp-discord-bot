import os
import sys
from io import StringIO
import discord


def main():
  client = discord.Client()

  @client.event
  async def on_ready():
    print("C++ bot is alive")
  
  @client.event
  async def on_message(message):

    if message.author == client.user:
      return 
    
    if message.content.startswith("!hello"):
      await message.channel.send(f"hello")
    
    if message.content.startswith("!runPython"):
      # remove the command and 
      message.content = message.content[len("!runPython")+1:]
      code = '\n'.join(message.content.split('\n'))
      save_stdout = sys.stdout
      output = StringIO()
      sys.stdout = output
      exec(code)
      await message.channel.send(output.getvalue())
      sys.stdout = save_stdout
      print(output.getvalue())
    
    if message.content.startswith("!runC++"):
      message.content = message.content[len("!runC++")+1:]
      code = '\n'.join(message.content.split('\n'))
      # write the code in the code.cpp
      with open('code.cpp', 'w') as f:
        f.write(code)
      # use terminal commands to compile and run it
      os.system('clang++-7 -pthread -std=c++17 -o out code.cpp')
      os.system('./out > out.txt')
      #return the output 
      with open('out.txt', 'r') as f:
        output = f.read()
      await message.channel.send(output)



  client.run(TOKEN)



if __name__ == "__main__":
  main()
