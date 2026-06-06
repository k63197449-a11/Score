import os
import time
import subprocess

# ইউটিউব স্ট্রিম কি গিটহাব এনভায়রনমেন্ট থেকে নেবে
stream_key = os.environ.get('YT_STREAM_KEY')
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

print("Starting Realtime 5-Minute Stream Loop...")

# এফএফমপেগ কম্যান্ড যা ব্যাকগ্রাউন্ডে ৩২০ সেকেন্ড (প্রায় ৫ মিনিট) রান করবে
# এটি প্রতি মুহূর্তে score.txt এবং commentary.mp3 ফাইল রিড করবে লাইভ অবস্থায়
ffmpeg_cmd = [
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=1080x1920:rate=30,format=yuv420p',
    '-stream_loop', '-1', '-re', '-i', 'commentary.mp3',
    '-vf', 'geq=r=\'12+sin(2*PI*X/W+T)*15\':g=\'20+cos(2*PI*Y/H+T)*15\':b=\'40+sin(T)*10\',drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:textfile=score.txt:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:fontsize=40:box=1:boxcolor=black@0.7:boxborderw=20,format=yuv420p',
    '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'veryfast', '-b:v', '2500k', '-t', '310',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-f', 'flv', rtmp_url
]

# লাইভ স্ট্রিম ব্যাকগ্রাউন্ডে স্টার্ট করা হলো
process = subprocess.Popen(ffmpeg_cmd)

# এই ৫ মিনিটের লুপের ভেতরে প্রতি ৩০ সেকেন্ড পর পর স্কোর ও ভয়েস আপডেট হবে রিয়েলটাইম!
start_time = time.time()
while time.time() - start_time < 300:
    print("Checking for realtime score updates...")
    # ১. নতুন স্কোর ফেচ করা
    os.system('node fetch-score.js')
    # ২. নতুন রিয়েলটাইম ভয়েস জেনারেট করা
    os.system('edge-tts --voice bn-IN-PradeepNeural --text "$(cat score.txt)" --write-media commentary.mp3')
    
    time.sleep(30) # ৩০ সেকেন্ড পর পর আপডেট করবে

# ৫ মিনিট শেষ হলে প্রসেস বন্ধ হবে এবং পরবর্তী গিটহাব শিডিউল আবার নতুন লুপ শুরু করবে
process.wait()
