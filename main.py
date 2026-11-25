import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw
import textwrap

TOKEN = os.environ.get("BOT_TOKEN")

def make_long_video(script):
    scenes = script.split(".")
    clips = []
    for i, scene in enumerate(scenes):
        if len(scene.strip()) < 5: continue
        tts = gTTS(text=scene, lang='bn')
        tts.save(f"voice_{i}.mp3")
        img = Image.new('RGB', (1280,720), color=(15,15,35))
        d = ImageDraw.Draw(img)
        d.text((100,300), textwrap.fill(scene.strip(), width=30), fill=(255,255,255))
        img.save(f"bg_{i}.png")
        audio = AudioFileClip(f"voice_{i}.mp3")
        clip = ImageClip(f"bg_{i}.png").set_duration(audio.duration).set_audio(audio)
        clips.append(clip)
    final = concatenate_videoclips(clips)
    final.write_videofile("long_video.mp4", fps=24)
    return "long_video.mp4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Script পাঠান, আমি লং ভিডিও বানিয়ে দিচ্ছি।")

async def handle_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ভিডিও বানাচ্ছি... ২-৩ মিনিট লাগবে।")
    path = make_long_video(update.message.text)
    await update.message.reply_video(video=open(path,'rb'))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_script))
app.run_polling()
