import requests, bs4, re, os, ctypes
from ctypes import wintypes


####Static Variables####
Nasa_Website = 'https://apod.nasa.gov/apod/'
Name_Of_File = 'DesktopPhoto.jpg'


#Creating Path name of the location of the file
Path_User = os.path.expanduser('~')
Path_To_File = os.path.join(Path_User, 'Desktop' ,Name_Of_File)

#Getting the NASA HTML Page to find the link to the actual photo
archive = requests.get(Nasa_Website)
archive.raise_for_status()
archiveHTML = bs4.BeautifulSoup(archive.text)


#Finding the Image link in the HTML
aTags = archiveHTML.select('a')
image = re.search('image(.*).jpg', str(aTags[1])).group(0)
photoOfTheDayLink = Nasa_Website + image


#Grab Image and save to desktop
image = requests.get(photoOfTheDayLink) #grabs the image 
imageFile = open(Path_To_File, 'wb')
for chunk in image.iter_content(100000):
    imageFile.write(chunk)
imageFile.close()


#Setting Photo as Desktop Background
SPI_SETDESKWALLPAPER  = 0x0014
SPIF_UPDATEINIFILE    = 0x0001
SPIF_SENDWININICHANGE = 0x0002
user32 = ctypes.WinDLL('user32')


SystemParametersInfo = user32.SystemParametersInfoW
SystemParametersInfo.argtypes = ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint
SystemParametersInfo.restype = wintypes.BOOL
SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, Path_To_File, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)










