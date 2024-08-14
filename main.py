from pytube import YouTube
link = str(input("Enter your link : "))
yt = YouTube(link)
stream = yt.streams.get_highest_resolution()
stream.download()
print("DOWNLOADED SUCCESSFULLY ! ")