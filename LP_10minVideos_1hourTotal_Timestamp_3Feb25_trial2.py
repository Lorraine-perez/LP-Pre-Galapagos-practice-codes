#2nd partially succesful code for continuous videos with timestamp. Tried to address issues with first code. 
#Issues: still striggling with jumping frames, lag between recordings, variations in video length
import os
import time
import cv2
from datetime import datetime
from picamera2 import MappedArray, Picamera2
from picamera2.encoders import H264Encoder

# Folder for storing videos\
folder_name = "OG-FUL-500-25"
os.makedirs(folder_name, exist_ok=True)

# Initialize camera\
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280,720)}) #reduce resolution for better performance
picam2.configure(video_config)

colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(request):
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

picam2.pre_callback = apply_timestamp

# Encoder setup\
encoder = H264Encoder(25000000) #increase bitrate for better quality 

# Recording settings\
total_duration = 60 * 60  # 1 hour in seconds\
video_length = 10 * 60  # 10 minutes in seconds\
num_videos = total_duration // video_length  # Number of 10-min videos\

picam2.start()

for i in range(num_videos):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"FUL-500_{timestamp}.h264"
    video_path = os.path.join(folder_name, video_filename)
    
    print(f"Recording:{video_filename}") #print recording filename

    #start and record video with precise timing
    picam2.start_recording(encoder, video_path)
    time.sleep(video_length) #record for specified duration
    picam2.stop_recording()

picam2.stop()
print("Recording session complete! ;D")

