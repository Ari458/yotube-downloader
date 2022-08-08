import time
import pytube as pt
import shutil
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
#import moviepy.editor as mp 

def takeInput():
    yt_link=input('Enter your link here: ')
    folder_name=input('Enter folder name(you can find it on your Desktop): ')
    return yt_link,folder_name    

def getPath(folder_name):
    path='C:\\Users\\'+os.getlogin()+'\\Desktop\\'+folder_name
    temp_path='C:\\%temp%'
    return path,temp_path

def generateLinkType(link):
    type=''
    dataP=pt.Playlist(link)
    
    try:
        if len(dataP)==0:
            type='S'
        else:
            type='M'    
    except:
        type='S'

    return type

def convertMp3(path,download_path):
    print('\t\tConverting..')
    save_path=download_path.split('\\')
    save_path=path+'\\'+save_path[len(save_path)-1].split('.')[0]+'.mp3'
    VideoFileClip(download_path).audio.write_audiofile(save_path)
    print('~~~~Task Completed~~~~')

def single_link(link,temp_path,choice):
    raw=pt.YouTube(link)
    data=raw.streams
    title=raw.title

    if choice=='1':
        download_path=data.first().download(temp_path)
    elif choice=='2':
        download_path=data.get_highest_resolution().download(temp_path)

    print(title+'\t------------>Download Complete')

    return download_path

def playlistLink(link,temp_path,choice):
    data=pt.Playlist(link)
    download_path=[]

    for i in data:
        download_path.append(single_link(i,temp_path,choice))

    return download_path    

def deleteTempFiles(temp_path,output_path):
    os.system('taskkill /im ffmpeg-win64-v4.2.2.exe /t /f')
    time.sleep(5)
    shutil.rmtree(temp_path) 
    os.startfile(output_path)

while True:
    
    choice=input("\n***************Youtube Downloader********************\n\n1.Audio\n2.Video\n3.exit\n\n$$Enter your choice$$\n--> ")

    if choice in ('1','2'):
        yt_link,folder_name=takeInput()
        output_path,temp_path=getPath(folder_name)
        link_type=generateLinkType(yt_link)

    if choice=='1':
        try:
            os.mkdir(output_path)
        except:
            print()
        print('\t\tPlease Wait(keep patience).....')
        if link_type=='S':
            convertMp3(output_path,single_link(yt_link,temp_path,choice))
        elif link_type=='M':
            total_links=playlistLink(yt_link,temp_path,choice)

            for link in total_links:
                convertMp3(output_path,link)
        deleteTempFiles(temp_path,output_path)        
    elif choice=='2':
        print('\t\tPlease Wait(keep patience).....')
        if link_type=='S':
            single_link(yt_link,output_path,choice)
        elif link_type=='M':
            playlistLink(yt_link,output_path,choice) 
        os.startfile(output_path)
        time.sleep(2)            
    elif choice=='3':
        quit(108)
    else:
        print('\n# Wrong Choice\nTry again...\n')
       


