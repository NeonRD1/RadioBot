import time

import radiobot

def main():
    
    #create a list of bots to spawn and add each bot
    bot_list = []
    bot_list.append(radiobot.PlaylistBot("listentothis"))
    #bot_list.append(radiobot.PlaylistBot("music"))
    #bot_list.append(radiobot.PlaylistBot("youtube"))
    #bot_list.append(radiobot.PlaylistBot("test"))    
    
    #main program loop - checks to see if each bot is running, if it's not, it runs the bot, then this thread sleeps 30 seconds
    while True:
        for bot in bot_list:
            if bot.running == False:
                bot.launch()
            time.sleep(30)

#because this is not indented this is the first code run at launch
#this tests to see if this main.py is the script that was run (as opposed to being called from another script)
#if so it runs the main() method which is above and catches any errors in an error file                    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("error", 'w') as f:
            f.write(repr(e))
