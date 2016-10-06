
import logging

import euphoria as eu

class PlaylistBot(eu.ping_room.PingRoom, eu.standard_room.StandardRoom, eu.nick_room.NickRoom):
    """
    Bot that allows the user to interface with the notice board easily
    """

    def __init__(self, roomname, password=None):
        self.logger = logging.getLogger(roomname)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler("./logs/{}.log".format(roomname))
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.info("Initializing bot...")
        
        #this calls the inherited __init__ for PingRoom and StandardRoom giving us basic functionality
        super().__init__(roomname, password)
        
        self.nickname = "📻|RadioBot"
        self.nickreference = "@" + self.nickname
        self.paused = False

               
        #load help file and create short help text from the first line
        with open("data/help.txt", 'r') as f:
            self.help_text = f.read()
        self.short_help_text = self.help_text.split('\n')[0] + " Use !help {} for more detailed help.".format(self.nickreference)
        self.logger.info("Loaded help file")
         
   
    #method to handle the !kill command       
    def handle_kill(self, killed_by):
        self.logger.info("Shutting down bot. Killed by: {}".format(killed_by))
        self.send_chat("/me was killed by " + killed_by)
        self.connection.close()
        self.quit()
     
    def handle_chat(self, message):
        self.logger.debug("Received Chat Message...")
        
        #grab the chat contents from the chat message
        content = message["content"]
        reply = message["id"]

        #if the contents are empty (after stripping leading and trailing whitespace then abort (return)
        if len(content.strip()) == 0:
            return
        arguments = content.split()
        command = arguments.pop(0)
        
        
        #this catches !kill command and sends it to the handle_kill method (works anytime, paused or unpaused)
        if command.startswith("!kill") and self.nickreference in arguments:
                self.logger.debug("Kill Message...")
                self.handle_kill(message["sender"]["name"])
        elif command.startswith("!antighost"):
                self.change_nick(self.nickname)
                        
        #the following commands are only one if the bot is paused
        elif self.paused == True: 
            self.logger.debug("Bot is paused so only resume messaged will be recognized and accepted")
            if command.startswith("!resume") and self.nickreference in arguments:
                self.logger.info("!resume command used by: {}".format(message["sender"]["name"]))
                self.paused = False
                self.send_chat("/me resumed by {}".format(message["sender"]["name"]))
                
                
        #the following commands are only done if the bot is not paused       
        elif self.paused == False:
            if command.startswith("!radio"):
                 #dostuff on !radio command
                pass
                    
            elif command == "!pause" and self.nickreference in arguments:
                self.logger.info("!pause command used by: {}".format(message["sender"]["name"]))
                self.paused = True
                self.send_chat("/me paused by " + message["sender"]["name"])
