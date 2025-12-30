import os
import zipfile
from pathlib import Path
from send2trash import send2trash

directoryStr = "./"
directory = os.fsencode(directoryStr)

# Extract images from cbz files if they don't already exist, naming them sequentially
if not(os.path.isfile("./01.jpg") or os.path.isfile("./01.png") or os.path.isfile("./001.jpg") or os.path.isfile("./001.png")):
	cbzArr = [f for f in os.listdir(directory) if os.fsdecode(f).endswith(".cbz")]
	i = 1
	for file in cbzArr:
		filename = os.fsdecode(file)
		print("Extracting cbz ...",filename)
		zipdata = zipfile.ZipFile(filename)
		zipinfos = sorted(zipdata.infolist(), key=lambda x: Path(x.filename).stem)
		for zipinfo in zipinfos:
			extension = zipinfo.filename[-4:]
			if (extension.endswith("jpg") or extension.endswith("png")):
				padi = str(i) if i>99 else "0"+str(i) if i>9 else "00"+str(i)
				zipinfo.filename = directoryStr + padi + extension
				zipdata.extract(zipinfo)
				i += 1
		continue

# Merge images into one cbz
print("Merging ...")
merged = zipfile.ZipFile(directoryStr+"merged.cbz", mode="a")
imgArr = [f for f in os.listdir(directory) if (os.fsdecode(f).endswith(".jpg") or os.fsdecode(f).endswith(".png"))]
for img in imgArr:
	imgname = os.fsdecode(img)
	merged.write(directoryStr+imgname, imgname)
	print("Merged ...",imgname)

# Cleanup
print("Cleaning up ...")
for img in imgArr:
	imgname = os.fsdecode(img)
	send2trash(directoryStr+imgname)
	print("Moved",imgname,"to recycle bin.")

wait = input("Done")
