import os
import time
import subprocess

stream_key = os.environ.get('YT_STREAM_KEY')
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

print("Starting Realtime 5-Minute Google TTS Stream Loop...")

# এফএফমপেগ কমান্ড যা লাইভ ব্যাকগ্রাউন্ডে চলবে এবং অডিও ফিল্টার দিয়ে ভয়েস কোয়ালিটি একটু স্মুথ করবে
ffmpeg_cmd = [
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=1080x1920:rate=30,format=yuv420p',
    '-stream_loop', '-1', '-re', '-i', 'commentary.mp3',
    '-vf', 'geq=r=\'12+sin(2*PI*X/W+T)*15\':g=\'20+cos(2*PI*Y/H+T)*15\':b=\'40+sin(T)*10\',drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:textfile=score.txt:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:fontsize=40:box=1:boxcolor=black@0.7:boxborderw=20,format=yuv420p',
    '-af', 'atempo=0.95', # গুগলের যান্ত্রিক গলা কিছুটা স্বাভাবিক করার জন্য স্পিড সামান্য কমানো হয়েছে
    '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'veryfast', '-b:v', '2500k', '-t', '310',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-f', 'flv', rtmp_url
]

process = subprocess.Popen(ffmpeg_cmd)

start_time = time.time()
while time.time() - start_time < 300:
    print("Checking for realtime score updates...")
    # ১. নতুন স্কোর ফেচ করা
    os.system('node fetch-score.js')
    
    # ২. ফাইল থেকে ডাটা নিয়ে গুগল টিটিএস দিয়ে অডিও তৈরি করা
    if os.path.exists('score.txt') and os.path.getsize('score.txt') > 0:
        # আপনি যদি বাংলায় কমেন্ট্রি চান তবে নিচের lang='en' কেটে lang='bn' করে দেবেন
        os.system('python -c "from gtts import gTTS; text = open(\'score.txt\', \'r\').read(); tts = gTTS(text=text, lang=\'en\'); tts.save(\'commentary.mp3\')"')
    else:
        with open('score.txt', 'w', encoding='utf-8') as f:
            f.write("Live score is updating. Please wait.")
        os.system('python -c "from gtts import gTTS; text = open(\'score.txt\', \'r\').read(); tts = gTTS(text=text, lang=\'en\'); tts.save(\'commentary.mp3\')"')
        
    time.sleep(30) # প্রতি ৩০ সেকেন্ড পর পর লাইভ স্কোর ও ভয়েস আপডেট হবে

process.wait()
