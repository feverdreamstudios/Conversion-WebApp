import streamlit as st
from PIL import Image
from PIL import PngImagePlugin
from io import BytesIO
import datetime as dt
import zipfile

def convertImages():
    zipBuffer = BytesIO()
    with zipfile.ZipFile(file=zipBuffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip:
        for image in uploadedFiles:
            filename = image.name[:-4]
            image = Image.open(image).convert("RGB")
            propChunk = PngImagePlugin.PngInfo()
            now = dt.datetime.now()
            timestamp = now.strftime("%Y,%m,%d,%H,%M,%S,%f")[:-3]
            propData = b"\x04\x00\x00\x00\x09\x00\x07\x00\x00\x00\x73\x69\x6d\x5f\x69\x64\x73\x00\x00\x00\x00\x07\x00\x00\x00\x74\x79\x70\x65\x5f\x69\x64\x02\x00\x00\x00\x2d\x31\x05\x00\x00\x00\x73\x68\x61\x72\x65\x01\x00\x00\x00\x30\x10\x00\x00\x00\x6f\x72\x69\x67\x69\x6e\x61\x6c\x5f\x73\x69\x6d\x5f\x69\x64\x73\x00\x00\x00\x00\x0a\x00\x00\x00\x6c\x69\x6b\x65\x5f\x63\x6f\x75\x6e\x74\x01\x00\x00\x00\x30\x07\x00\x00\x00\x63\x6f\x6d\x6d\x65\x6e\x74\x00\x00\x00\x00\x08\x00\x00\x00\x66\x61\x76\x6f\x72\x69\x74\x65\x01\x00\x00\x00\x30\x0a\x00\x00\x00\x74\x69\x6d\x65\x5f\x73\x74\x61\x6d\x70\x17\x00\x00\x00"+timestamp.encode("ASCII")+b"\x0c\x00\x00\x00\x68\x6f\x75\x73\x65\x68\x6f\x6c\x64\x5f\x69\x64\x00\x00\x00\x00"
            propChunk.add(cid=b"prOP", data=propData, after_idat=True)
            buffer = BytesIO()
            image.save(buffer, pnginfo=propChunk, format="png")
            zip.writestr(zinfo_or_arcname=f"{filename}.png", data=buffer.getvalue())
            buffer.close()
    zipBuffer.seek(0)
    return zipBuffer.getvalue()

st.title("Sims 4 Screenshot Converter")
st.write("This tool allows you to convert external screenshots and images to be recognised Sims 4 screenshots. Just upload the images, and download the converted screenshots as a ZIP archive. You can then extract the converted screenshots into your Sims 4 screenshot folder found at")
st.code(r"C:\Users\{Your Username}\Documents\Electronic Arts\The Sims 4\Screenshots", language=None)
col1, col2, col3 = st.columns(3,vertical_alignment="center")
uploadedFiles = col1.file_uploader(label="screenshots",accept_multiple_files=True,label_visibility="hidden")
col2.image("https://freepngimg.com/thumb/direction/21560-6-green-arrow-image.png")
col3.download_button(label="Download converted images", data=convertImages(), file_name="ConvertedScreenshots.zip", disabled=not uploadedFiles)