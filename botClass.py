import discord
from botCredentials import botPrefix,OWNER_ID
from datetime import timezone,datetime,time
from time import sleep
from dateParse import dateParse
from random import randint
from json import dumps,loads

class ChitraguptClient(discord.Client):

    eventProcessRunning = False
    eventStep = 1
    botActivity = discord.Game("ch.help | v 0.1")
    descriptionLength = 1600
    eventDict = {}
    restartBot = False
    tagUserTemplateString = "<@{0}>"
    eventAcceptEmoji = "👍"

    async def on_ready(self):
        try:
            with open("eventLog.txt") as eventLog:
                eventDict = loads(eventLog.read())

            print('Logged on as {0}!'.format(self.user))
            await self.change_presence(activity=self.botActivity)

        except Exception as startupException:
            print("startupException, Type - {} : {}".format(startupException.__class__.__name__,startupException))

    ######## MESSAGE PARSING ########

    async def on_message(self, message):
        try:
            # or not (prefixMentioned or botMentioned):
            if message.author == self.user or message.author.bot:
                return

            messageContent = message.content.lower()
            ###### PREFIX AND MENTION PROCESSING ######

            # Check for prefix or bot mentions
            prefixMentioned = bool(messageContent.startswith(botPrefix))
            botMentioned = bool(messageContent.startswith(
                "<@!{0}>".format(self.user.id)))

            messageContent = messageContent.replace(botPrefix, "")
            messageContent = messageContent.replace(
                "<@!{0}>".format(self.user.id), "")
            messageContent = messageContent.strip()

            if (prefixMentioned or botMentioned) and str(message.channel.type) != "private":

                #### HELP #####
                if messageContent.startswith("help"):
                    await message.channel.send("Here to help!!")

                #### EVENT #####
                elif messageContent.startswith('event'):
                    self.eventProcessRunning = True
                    self.eventChannel = message.channel
                    self.eventEmbed = eventEmbedTemplate()
                    await self.createEvent(message.author)
                    await message.delete()


                # elif messageContent == "restart" and str(message.author.id) == OWNER_ID:
                #     await message.channel.send("Restarting <@{}>".format(self.user.id))
                #     sleep(1)
                #     await self.close()

                elif messageContent == "shutdown" and str(message.author.id) == OWNER_ID:
                    await message.channel.send("Shutting Down <@{}>".format(self.user.id))
                    sleep(1)
                    await self.close()
                    # raise KeyboardInterrupt
                    # signal.raise_signal(SIGTERM)


            ####### EVENT PROCESSING #######
            elif self.eventProcessRunning and str(message.channel.type) == "private":
                try:
                    if self.eventStep == 1:
                        self.eventEmbed.setTitle(message.content)
                        self.eventStep += 1

                    elif self.eventStep == 2:
                        if len(message.content) > self.descriptionLength:
                            await message.author.send("OVERKILL! Description should have maximum {} characters.".format(self.descriptionLength))
                        else:
                            self.eventEmbed.setDescription(message.content)
                            self.eventStep += 1

                    elif self.eventStep == 3:
                        flag = self.eventEmbed.setEventTime(message.content)
                        
                        if flag: 
                            self.eventStep = 1
                            self.eventProcessRunning = False
                            embedMessage = await self.eventChannel.send(embed=self.eventEmbed)
                            await embedMessage.add_reaction(emoji = self.eventAcceptEmoji)
                            self.eventDict[str(embedMessage.id)] = self.eventEmbed.to_dict()
                            
                            with open("eventLog.txt","w") as eventLog:
                                eventLog.write(dumps(self.eventDict))

                        else:
                            await message.author.send("Invalid date or time format")

                    await self.createEvent(message.author)

                except Exception as eventParsingError:
                    print("eventParsingError, Type - {} : {} ".format(eventParsingError.__class__.__name__,eventParsingError))

            # else:
            #     print("{0}  sent to  {1}".format(
            #         message.content, message.channel))

        except Exception as onMessageException:
            print("messageHandlingException, Type - {} : {}".format(onMessageException.__class__.__name__,onMessageException))

    async def createEvent(self, user):
        try:
            assert self.eventProcessRunning
            if self.eventStep == 1:
                await user.send("Give title of the event")

            elif self.eventStep == 2:
                await user.send("Give Description (max {} characters) ".format(self.descriptionLength))

            elif self.eventStep == 3:
                await user.send("Give time of the event. Accepted formats:\n1.YYYY-MM-DD 9:00 PM/ 21:00\n2.Weekday at 9:00 PM/21:00\n3.Today/Tomorrow at 9:00 PM\n4.Now\n5.After/In x h and/or min")

        except AssertionError:
            pass

        except Exception as eventCreationException:
            print("eventCreationException, Type - {} : {} ".format(eventCreationException.__class__.__name__,eventCreationException))

    # async def createEventChannel(self,guild,category=None):
        
    async def on_raw_reaction_add(self,context):
        if context.user == self.user:
            return

        try:
            self.eventEmbed = eventEmbedTemplate.from_dict(self.eventDict[str(context.message_id)])
            self.eventEmbed.participants = self.eventDict[str(context.message_id)]["fields"][0]["value"]
            
            if self.eventEmbed.participants == "None":
                self.eventEmbed.participants = self.tagUserTemplateString.format(context.user.id) + "\n"
            else:
                self.eventEmbed.participants += self.tagUserTemplateString.format(context.user.id) + "\n"

            self.eventEmbed.set_field_at(index = 0, name="Participants",value=self.eventEmbed.participants)
            self.eventDict[str(context.message.id)] = self.eventEmbed.to_dict()

            with open("eventLog.txt","w") as eventLog:
                eventLog.write(dumps(self.eventDict))

            await context.remove(context.user)
            await context.message.edit(embed = self.eventEmbed)

        except KeyError:
            pass

        except Exception as eventAddParticipantReactionException:
            print("eventAddParticipantReactionException, Type - {} : {}".format(eventAddParticipantReactionException.__class__.__name__,eventAddParticipantReactionException))

    async def on_disconnect(self):
        print("Successfully disconnected {0} !".format(self.user))

class eventEmbedTemplate(discord.Embed):

    participants = ""
    
    def __init__(self, url=discord.Embed.Empty, type="rich"):
        self.url = url
        self.type = type
        self.title = "Event Title"
        self.description = "Event Description"
        self.color = discord.Color(value=randint(0,0xffffff))
        self.set_footer(text= "Event Footer")
        self.add_field(name="Particpants", value=None)

    
    def setTitle(self, title):
        self.title = title

    def setDescription(self, description):
        self.description = description

    def setEventTime(self, time):
        self.eventTime = dateParse(time)
        if self.eventTime is None:
            return False
        self.eventTime += " (IST +5:30)"
        self.set_footer(text = self.eventTime)
        return True
