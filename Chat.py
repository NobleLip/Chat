import sqlite3
import hashlib
import time
import threading


# Reset
Color_Off="\033[0m"       # Text Reset

# Regular Colors
Black="\033[0;30m"        # Black
Red="\033[0;31m"          # Red
Green="\033[0;32m"        # Green
Yellow="\033[0;33m"       # Yellow
Blue="\033[0;34m"         # Blue
Purple="\033[0;35m"       # Purple
Cyan="\033[0;36m"         # Cyan
White="\033[0;37m"        # White


#----Data Base Connection
con = sqlite3.connect('Chat.db', check_same_thread=False)
cur = con.cursor()

#----Data Base Creation
try:
	cur.execute('''CREATE TABLE login
               (Username text UNIQUE, Password text)''')
	con.commit()
	print(Green+'[+] DataBase Created')
	print('[+] DataBase Connected'+Color_Off)
except:
	print(Green+'[+] DataBase Connected'+Color_Off)


print(Blue+'''
  ____ _           _   ____                           
 / ___| |__   __ _| |_/ ___|  ___ _ ____   _____ _ __ 
| |   | '_ \ / _` | __\___ \ / _ \ '__\ \ / / _ \ '__|
| |___| | | | (_| | |_ ___) |  __/ |   \ V /  __/ |   
 \____|_| |_|\__,_|\__|____/ \___|_|    \_/ \___|_|   
                                                      

'''+Color_Off)
#Done
def Login():
	User = input(Yellow + '[!] Insert Username!\n'+Color_Off+'[=] ')
	Pass = input(Yellow +'[!] Insert Password!\n'+Color_Off+'[=] ')
	Pass = hashlib.sha256(Pass.encode('utf-8')).hexdigest()
	Res = cur.execute('''SELECT * FROM login Where Username = ? AND Password = ?''', [User, Pass])
	if Res.fetchone() != None:
		print(Green+'[+] '+User+' Welcome !'+Color_Off)
		return User
	else:
		print(Red+'[-] Username Or Password Incorrect!'+Color_Off)
		return ''
#Done
def Regi():
	User = input(Yellow + '[!] Insert Username!\n'+Color_Off+'[=] ')
	Pass = input(Yellow +'[!] Insert Password!\n'+Color_Off+'[=] ')
	Passcheck = input(Yellow +'[!] Insert Password Again!\n'+Color_Off+'[=] ')
	if Pass != Passcheck:
		print(Red+'[-] Passwords Dont Match!'+Color_Off)
		return 0
	Pass = hashlib.sha256(Pass.encode('utf-8')).hexdigest()
	
	try:
		cur.execute('''INSERT INTO login VALUES (?,?)''', [User, Pass])
		con.commit()
		print(Green+'[+] Username Registered!'+Color_Off)
	except:
		print(Red+'[-] Username Already Used!'+Color_Off)

def ChoLogin():
	print('\n	\033[1;37m Login		\n'+Color_Off)
	Login_Username = ''	
	while Login_Username == '':
		Response = input(Yellow + '[!] Login - 0\n[!] Register - 1\n'+Color_Off+'[=] ')
		if int(Response) == 0:
			Login_Username = Login()
		elif int(Response) == 1:
			Regi()
		else:
			print(Red + '[-] Select Valid Option!\n'+Color_Off)
	return Login_Username
#----------------------------------------Login Done------------------------------------------

def Create_Chat():
	Chat_Name = input(Yellow + '[!] Insert Chat Name!\n'+Color_Off+'[=] ')
	#Try Create DATABASE, if it exists gives error
	try:
		cur.execute('CREATE TABLE '+Chat_Name+' (Username text, Message text)')
		con.commit()
		print(Green+'[+] '+ Chat_Name +' Registered, Ready to use!'+Color_Off)
		return Chat_Name
	except:
		print(Red + '[-] Chat Already Exists , Choose another Name!\n'+Color_Off)
		return ''

def Enter_Chat():
	Chat_Name = input(Yellow + '[!] Insert Chat Name!\n'+Color_Off+'[=] ')
	try:
		Res = cur.execute('SELECT * FROM '+ Chat_Name)
		print(Green+'[+] Welcome To '+ Chat_Name +'!'+Color_Off)
		return Chat_Name
	except:
		print(Red + '[-] Chat Does Not Exist!\n'+Color_Off)
		return ''
def ChoChat():
	print('\n	\033[1;37m Choose Chat		\n'+Color_Off)
	Actual_Chat = ''
	while Actual_Chat == '':
		Response = input(Yellow + '[!] Create Chat - 0\n[!] Enter Chat - 1\n'+Color_Off+'[=] ')
		if int(Response) == 0:
			Actual_Chat = Create_Chat()
		elif int(Response) == 1:
			Actual_Chat = Enter_Chat()
		else:
			print(Red + '[-] Select Valid Option!\n'+Color_Off)
	return Actual_Chat


#---------------------------------Enter On Chat Done-------------------------------------------
Login_User = ChoLogin()
Entered_ChatName = ChoChat()

def CheckChatThread(Actual):
	while 1:
		Res = cur.execute('SELECT * FROM '+Entered_ChatName)
		Lenght = 0
		for i in Res:
			Lenght = Lenght + 1
			if Lenght > Actual:
				print(str(i[0]),':',str(i[1]))
		Actual = Lenght
		time.sleep(1)

def CheckChat(Actual):
	Res = cur.execute('SELECT * FROM '+Entered_ChatName)
	Lenght = 0
	for i in Res:
		Lenght = Lenght + 1
		if Lenght > Actual:
			print(str(i[0]),':',str(i[1]))
	return Lenght


def FirstPrint():
	Length = 0
	Res = cur.execute('SELECT * FROM '+Entered_ChatName)
	for i in Res:
		print(i[0],':',i[1])
		Length = Length + 1
	return Length

def SendMess(Message):
	cur.execute('INSERT INTO '+Entered_ChatName+' VALUES (?,?)', [Login_User, Message])
	con.commit()

print('\n	\033[1;37m '+Entered_ChatName+'		\n'+Color_Off)

Actual_Length = FirstPrint()

#Tread was my main idea , but im strugling it print outputs
#TreadChatControl = threading.Thread(target=CheckChatThread, args=[Actual_Length])
#TreadChatControl.start()

while 1:
	Mess =	input("New Message: ")
	SendMess(Mess)
	Actual_Length = CheckChat(Actual_Length)


TreadChatControl.join()




























