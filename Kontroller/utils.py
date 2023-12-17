import queue
import socket
import platform
import subprocess as sp
from threading import Thread
from typing import Any
import cv2
from win10toast import ToastNotifier
from win11toast import toast

"""
UUUUUUUU     UUUUUUUUTTTTTTTTTTTTTTTTTTTTTTTIIIIIIIIIILLLLLLLLLLL                SSSSSSSSSSSSSSS
U::::::U     U::::::UT:::::::::::::::::::::TI::::::::IL:::::::::L              SS:::::::::::::::S
U::::::U     U::::::UT:::::::::::::::::::::TI::::::::IL:::::::::L             S:::::SSSSSS::::::S
UU:::::U     U:::::UUT:::::TT:::::::TT:::::TII::::::IILL:::::::LL             S:::::S     SSSSSSS
 U:::::U     U:::::U TTTTTT  T:::::T  TTTTTT  I::::I    L:::::L               S:::::S
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L               S:::::S
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L                S::::SSSS
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L                 SS::::::SSSSS
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L                   SSS::::::::SS
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L                      SSSSSS::::S
 U:::::D     D:::::U         T:::::T          I::::I    L:::::L                           S:::::S
 U::::::U   U::::::U         T:::::T          I::::I    L:::::L         LLLLLL            S:::::S
 U:::::::UUU:::::::U       TT:::::::TT      II::::::IILL:::::::LLLLLLLLL:::::LSSSSSSS     S:::::S
  UU:::::::::::::UU        T:::::::::T      I::::::::IL::::::::::::::::::::::LS::::::SSSSSS:::::S
    UU:::::::::UU          T:::::::::T      I::::::::IL::::::::::::::::::::::LS:::::::::::::::SS
      UUUUUUUUU            TTTTTTTTTTT      IIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLLL SSSSSSSSSSSSSSS
"""

def calling_xml():
    xml = """
<toast launch="action=answer&amp;callId=938163" scenario="incomingCall">

  <visual>
    <binding template="ToastGeneric">
      <text>Andrew Bares</text>
      <text>Incoming Call - Mobile</text>
      <image hint-crop="circle" src="https://unsplash.it/100?image=883"/>
    </binding>
  </visual>

  <actions>

    <action
      content="Text reply"
      imageUri="Assets/Icons/message.png"
      activationType="foreground"
      arguments="action=textReply&amp;callId=938163"/>

    <action
      content="Reminder"
      imageUri="Assets/Icons/reminder.png"
      activationType="background"
      arguments="action=reminder&amp;callId=938163"/>

    <action
      content="Ignore"
      imageUri="Assets/Icons/cancel.png"
      activationType="background"
      arguments="action=ignore&amp;callId=938163"/>

    <action
      content="Answer"
      imageUri="Assets/Icons/telephone.png"
      arguments="action=answer&amp;callId=938163"/>

  </actions>

</toast>"""
    return xml


def start_new_thread(target, args=None):
    if args is None:
        Thread(target=target).start()
    else:
        Thread(target=target, args=args).start()


def simple_notify(title, msg, icon=r"Assets\icon.ico", duration=10):
    try:
        toast = ToastNotifier()
        if platform.system() == "Windows":
            toast.show_toast(title=title, 
                             msg=msg, 
                             icon_path=icon, 
                             duration=duration)
        else:
            return 0
    except Exception as e:
        print(f"\n\n{e}\n")

    
def execute_cmd(cmd):
    run = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    if run.returncode:
        return run.stderr
    else:
        return run.stdout


class ThreadWithReturnValue(object):
    def __init__(self, target=None, args=(), **kwargs):
        self._que = queue.Queue()
        self._t = Thread(target=lambda q,arg1,kwargs1: q.put(target(*arg1, **kwargs1)) ,
                args=(self._que, args, kwargs), )
        self._t.start()

    def join(self):
        self._t.join()
        return self._que.get()
    


def NewThread(com, Returning: bool, *arguments) -> Any:
    """
    Will create a new thread for a function/command.

    :param com: Command to be Executed
    :param arguments: Arguments to be sent to Command
    :param Returning: True/False Will this command need to return anything
    """
    class NewThreadWorker(Thread):
        def __init__(self, group = None, target = None, name = None, args = (), kwargs = None, *,
                     daemon = None):
            Thread.__init__(self, group, target, name, args, kwargs, daemon = daemon)
            
            self._return = None
        
        def run(self):
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)
        
        def join(self):
            Thread.join(self)
            return self._return
    
    ntw = NewThreadWorker(target = com, args = (*arguments,))
    ntw.start()
    if Returning:
        return ntw.join()
    

if __name__ == "__main__":
    #print(str(toast(app_id="test", title="Title", body="Nigga", buttons=["1","2"], duration="short")[0]) == "2")
    #toast(xml=calling_xml())
    pass