from botClass import ChitraguptClient
from botCredentials import TOKEN
# from os import getenv

# token = getenv('DISCORD_TOKEN')

runningInstance = ChitraguptClient()

try:
    runningInstance.run(TOKEN,bot=True,reconnect = True)

except Exception as runtimeException:
    print("runtimeException, Type - {} : {} ".format(runtimeException.__class__.__name__,runtimeException))
