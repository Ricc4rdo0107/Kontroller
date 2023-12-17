import cv2
import time
import pyautogui
import numpy as np

"""
IIIIIIIIII
I::::::::I
I::::::::I
II::::::II
  I::::I     mmmmmmm    mmmmmmm     aaaaaaaaaaaaa     ggggggggg   ggggg    eeeeeeeeeeee
  I::::I   mm:::::::m  m:::::::mm   a::::::::::::a   g:::::::::ggg::::g  ee::::::::::::ee
  I::::I  m::::::::::mm::::::::::m  aaaaaaaaa:::::a g:::::::::::::::::g e::::::eeeee:::::ee
  I::::I  m::::::::::::::::::::::m           a::::ag::::::ggggg::::::gge::::::e     e:::::e
  I::::I  m:::::mmm::::::mmm:::::m    aaaaaaa:::::ag:::::g     g:::::g e:::::::eeeee::::::e
  I::::I  m::::m   m::::m   m::::m  aa::::::::::::ag:::::g     g:::::g e:::::::::::::::::e
  I::::I  m::::m   m::::m   m::::m a::::aaaa::::::ag:::::g     g:::::g e::::::eeeeeeeeeee
  I::::I  m::::m   m::::m   m::::ma::::a    a:::::ag::::::g    g:::::g e:::::::e
II::::::IIm::::m   m::::m   m::::ma::::a    a:::::ag:::::::ggggg:::::g e::::::::e
I::::::::Im::::m   m::::m   m::::ma:::::aaaa::::::a g::::::::::::::::g  e::::::::eeeeeeee
I::::::::Im::::m   m::::m   m::::m a::::::::::aa:::a gg::::::::::::::g   ee:::::::::::::e
IIIIIIIIIImmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaa   gggggggg::::::g     eeeeeeeeeeeeee
                                                               g:::::g
                                                   gggggg      g:::::g
                                                   g:::::gg   gg:::::g
                                                    g::::::ggg:::::::g
                                                     gg:::::::::::::g
                                                       ggg::::::ggg
                                                          gggggg


UUUUUUUU     UUUUUUUU        tttt            iiii  lllllll
U::::::U     U::::::U     ttt:::t           i::::i l:::::l
U::::::U     U::::::U     t:::::t            iiii  l:::::l
UU:::::U     U:::::UU     t:::::t                  l:::::l
 U:::::U     U:::::Uttttttt:::::ttttttt    iiiiiii  l::::l     ssssssssss
 U:::::D     D:::::Ut:::::::::::::::::t    i:::::i  l::::l   ss::::::::::s
 U:::::D     D:::::Ut:::::::::::::::::t     i::::i  l::::l ss:::::::::::::s
 U:::::D     D:::::Utttttt:::::::tttttt     i::::i  l::::l s::::::ssss:::::s
 U:::::D     D:::::U      t:::::t           i::::i  l::::l  s:::::s  ssssss
 U:::::D     D:::::U      t:::::t           i::::i  l::::l    s::::::s
 U:::::D     D:::::U      t:::::t           i::::i  l::::l       s::::::s
 U::::::U   U::::::U      t:::::t    tttttt i::::i  l::::l ssssss   s:::::s
 U:::::::UUU:::::::U      t::::::tttt:::::ti::::::il::::::ls:::::ssss::::::s
  UU:::::::::::::UU       tt::::::::::::::ti::::::il::::::ls::::::::::::::s
    UU:::::::::UU           tt:::::::::::tti::::::il::::::l s:::::::::::ss
      UUUUUUUUU               ttttttttttt  iiiiiiiillllllll  sssssssssss

"""





def show_webcam(title, show=True):
    videocap = cv2.VideoCapture(0)
    return_value, image = videocap.read()
    if show:
        cv2.imshow("Test",image)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    return image

def record_webcam_and_screen(capture_duration):
    try:
        SCREEN_SIZE = tuple(pyautogui.size())
        resolution = (1920, 1080)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('tmp/output.mp4', fourcc, 20.0, (SCREEN_SIZE))
        webcam = cv2.VideoCapture(0)
    
        
        start_time = time.time()
        while( int(time.time() - start_time) < capture_duration ):
            img = pyautogui.screenshot()
        
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            _, frame = webcam.read()
            fr_height, fr_width, _ = frame.shape
        
            img[0:fr_height, 0: fr_width, :] = frame[0:fr_height, 0: fr_width, :]
        
            out.write(img)
        
        out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        return False
    else:
        return True


def record_screen(capture_duration):
    try:
        capture_duration+=capture_duration*0.3
        SCREEN_SIZE = tuple(pyautogui.size())
        resolution = (1920, 1080)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('tmp/output.mp4', fourcc, 20.0, (SCREEN_SIZE))
    
        
        start_time = time.time()
        while( int(time.time() - start_time) < capture_duration ):
            img = pyautogui.screenshot()
        
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
            out.write(img)
        
        out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        return False
    else:
        return True
    
if __name__ == "__main__":
    record_screen(5)


def record_webcam(capture_duration): # = 14 somehow
    try:
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('tmp/output.mp4',fourcc, 20.0, (640,480))
        
        start_time = time.time()
        while( int(time.time() - start_time) < capture_duration ):
            ret, frame = cap.read()
            if ret==True:
                #frame = cv2.flip(frame,0)
                out.write(frame)
            else:
                break
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()
    except Exception as e:
        return False
    else:
        return True