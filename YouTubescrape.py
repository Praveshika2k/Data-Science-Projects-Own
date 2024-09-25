from pytube import YouTube

link = input("Enter Youtube video link: ")
try:
    yt = YouTube(link)
    print("Title :", yt.title)
    print("Views :", yt.views)
    print("Duration :", yt.length)
    print("Description :", yt.description)
    print("Ratings :", yt.rating)
    #for download
    # stream = yt.streams.get_highest_resolution()
    # stream.download()
    # print("Downloaded Successfully.")

except Exception as e:
    print(f"Failed to fetch...:{e}")
