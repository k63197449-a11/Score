import os
import time
import subprocess

stream_key = os.environ.get('YT_STREAM_KEY')
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

print("Starting Realtime 5-Minute Stream Loop...")

ffmpeg_cmd = [
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=1080x1920:rate=30,format=yuv420p',
    '-stream_loop', '-1', '-re', '-i', 'commentary.mp3',
    '-vf', 'geq=r=\'12+sin(2*PI*X/W+T)*15\':g=\'20+cos(2*PI*Y/H+T)*15\':b=\'40+sin(T)*10\',drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:textfile=score.txt:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:fontsize=40:box=1:boxcolor=black@0.7:boxborderw=20,format=yuv420p',
    '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'veryfast', '-b:v', '2500k', '-t', '310',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-f', 'flv', rtmp_url
]

process = subprocess.Popen(ffmpeg_cmd)

start_time = time.time()
while time.time() - start_time < 300:
    print("Checking for realtime score updates...")
    # ১. নতুন স্কোর ফেচ করা
    os.system('node fetch-score.js')
    
    # ২. ফাইল থেকে সরাসরি ভয়েস জенারেট করা (১০০% সেফ মেথড)
    if os.path.exists('score.txt') and os.path.getsize('score.txt') > 0:
        os.system('edge-tts --voice bn-IN-PradeepNeural --file score.txt --write-media commentary.mp3')
    else:
        with open('score.txt', 'w', encoding='utf-8') as f:
            f.write("লাইভ স্কোর আপডেট হচ্ছে।")
        os.system('edge-tts --voice bn-IN-PradeepNeural --file score.txt --write-media commentary.mp3')
        
    time.sleep(30)

process.wait()
