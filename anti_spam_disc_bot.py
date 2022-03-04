import discord
import time
import os
path=os.path.abspath(os.getcwd())+'/'
#path='/home/pi/Projects/anti_spam/'
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

guild = discord.Guild
channel_id_dms = 867747379138265150 # channel to report

def clear_history():
    timer = open(path+"time.txt", "w")
    timer.write(str(time.time()))
    timer.close()
    f = open(path+"history.txt", "w")
    f.write('first message##+##69')
    f.close()
    return
    
max_messages_in_clearing_time=9
clearing_time=120
timer = open(path+"time.txt", "w")
timer.write(str(time.time()))
timer.close()
f = open(path+"history.txt", "w")
f.write('first message##+##69')
f.close()
closed_channels=[]
@client.event
async def on_message(message):
    
    if (str(message.channel.id) in closed_channels) or (str(message.channel) in closed_channels):
        await message.delete()
        
    
    list_of_roles_names=[]
    for i in message.author.roles:
        list_of_roles_names.append(i.name)
    if 'Admin' in list_of_roles_names:
        admin=True
    else:
        admin=False
        
    if 'spammer' in list_of_roles_names:
        await message.delete()
        print("deleted spammer's message")
        return
        
    if message.author == client.user:
        return

    if not message.guild:

        return

    timer = open(path+"time.txt")
    last_clear=float(timer.read())
    timer.close()
    if time.time()-last_clear>=clearing_time:
        clear_history()

    msg = message.content
    if msg.split(' ')[0]=='$close' and admin==True:
        closed_channels.append(msg.split(' ')[1])
        print('closed channel with id={}'.format(msg.split(' ')[1]))
        print(closed_channels)
    if msg.split(' ')[0]=='$open' and admin==True:
        closed_channels.remove(msg.split(' ')[1])
        
        

    f = open(path+"history.txt", "a")
    f.write(str(msg)+"##+##"+str(message.author.id)+'\n')
    f.close()
    f = open(path+"history.txt")
    counter=0
    data=str(f.read())
    for i in data.split('\n'):
        if '##+##' in i:
            if i.split('##+##')[1]==str(message.author.id):
                counter=counter+1
    print(counter)
    if counter>=max_messages_in_clearing_time or (('http' in msg) and ('https://www.mediafire.com/' not in msg) and ('Admin' not in list_of_roles_names) ):
        if counter<max_messages_in_clearing_time:
            #await message.channel.send('{}, you have been soft-banned for spamming/breaking a rule. All further messages will be deleted . Contact an admin for help .'.format(str(message.author)) )
            #await message.delete()
            #await client.get_channel(867747379138265150).send('''deleted message from  user '{}' for sending link\n user wrote :{}'''.format(str(message.author)+' '+str(message.author.id),msg))
            
            f.close()
            return
            
        print('spammer detected :'+str(message.author)+'__'+str(message.author.id))
        guild = message.author.guild
        role = discord.utils.get(guild.roles, name="spammer") 
        if role is not None: # makes sure role exists
            await message.author.add_roles(role)
            f = open(path+"shadowbans.txt", "a")
            f.write(str(message.author)+':'+str(message.author.id)+'\n')
            f.close()
            await message.delete()
            await message.channel.send('{}, you have been soft-banned for spamming/breaking a rule. All further messages will be deleted . Contact an admin for help .'.format(str(message.author)) )
            await client.get_channel(867747379138265150).send('''softabanned user '{}' for spamming/breaking a rule\n user wrote :{}'''.format(str(message.author)+' '+str(message.author.id),msg))
            
            print("deleted spammer's message")
            print("and banned him")
            print("____")
            print("he said '{}' ".format(msg))
            #await message.delete()
        else:
            print('error getting role')

    f.close()
            
        


client.run('###insert_api_token_here')
