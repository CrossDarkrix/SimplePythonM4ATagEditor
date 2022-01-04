import ui, photos, sys, os.path, appex
from console import open_in
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3
from os import getcwd as pwd, remove
from shutil import copyfile
current_directory = pwd()
FilePath = ''

try:
	tmp_read_file = appex.get_attachments()[0]
	tmp_File = open(tmp_read_file, 'rb').read()
	tmp_file_name = tmp_read_file.split('/')[-1]
	FilePath = os.path.join(os.getenv('HOME'), 'tmp', tmp_file_name)
	with open(FilePath, 'wb') as tmpf:
		tmpf.write(tmp_File)	
except IndexError:
		pass

def GetPicture(getter):
	global ImgBytes
	PAssert = photos.Asset
	p = getter.superview
	try:
		ImgBytes = photos.Asset.get_image_data(photos.pick_asset()).read()
	except:
		ImgBytes = ''
	try:
		CoverPicture = ui.Image.from_data(ImgBytes)
		p['CoverArt'].image = CoverPicture
	except:
		pass

def RemoteFile(Remote):
	R = Remote.superview
	ShowFileName = Remote.superview['ViewFile']
	ShowFileName.text = '"{}"'.format(FilePath.split('/')[-1])
	R['FileName'].text = '~/tmp/{}'.format(FilePath.split('/')[-1])

def LoadMetaData(d):
	E = d.superview
	try:
		AudioFile = MP4(FilePath)
		AlbumArt = ui.Image.from_data(AudioFile['covr'][0])
	except:
		pass
	try:
		E['CoverArt'].image = AlbumArt
	except:
		pass
	try:
		E['Title'].text = AudioFile.tags['\xa9nam'][0]
	except:
		pass
	try:
		E['Artist'].text = AudioFile.tags['\xa9ART'][0]
	except:
		pass
	try:
		E['AlbumArtist'].text = AudioFile.tags['aART'][0]
	except:
		pass
	try:
		E['Album'].text = AudioFile.tags['\xa9alb'][0]
	except:
		pass
	try:
		E['Genre'].text = AudioFile.tags['\xa9gen'][0]
	except:
		pass
	try:
		E['Year'].text = AudioFile.tags['\xa9day'][0]
	except:
		pass
	try:
		TrackNum, TotalTrack = AudioFile.tags['trkn'][0]
		E['TrackNum'].text = str(TrackNum)
		E['TotalTrackNum'].text = str(TotalTrack)
	except:
		pass
	try:
			DiscNum, TotalDisc = AudioFile.tags['disk'][0]
			E['DiscNum'].text = str(DiscNum)
			E['TotalDiscNum'].text = str(TotalDisc)
	except:
		pass
	try:
		remove(FilePath)
	except:
		pass

def AudioTagEdit(file_path, title=None, artist=None, albumartist=None, album=None, genre=None, year=None, track_num=None, total_track_num=None, disc_num=None, total_disc_num=None):

	if file_path.split('/')[-1].split('.')[-1].lower() == 'm4a':
		AudioFile = MP4(file_path)
		if title:
			AudioFile.tags['\xa9nam'] = title
		if artist:
			AudioFile.tags['\xa9ART'] = artist
		if albumartist:
			AudioFile.tags['aART'] = albumartist
		if album:
			AudioFile.tags['\xa9alb'] = album
		if genre:
			AudioFile.tags['\xa9gen'] = genre
		if year:
			AudioFile.tags['\xa9day'] = year
		if total_track_num:
			if track_num:
				AudioFile.tags['trkn'] = [(int(track_num), int(total_track_num))]
			else:
				AudioFile.tags['trkn'] = [(0, int(total_track_num))]
		else:
			if track_num:
				AudioFile.tags['trkn'] = [(int(track_num), int(track_num))]
		if total_disc_num:
			if disc_num:
				AudioFile.tags['disk'] = [(int(disc_num), int(total_disc_num))]
			else:
				AudioFile.tags['disk'] = [(0, int(total_disc_num))]
		else:
			if disc_num:
				AudioFile.tags['disk'] = [(int(disc_num), int(disc_num))]

		try:
			AudioFile.tags['covr'] = [MP4Cover(ImgBytes)]
		except NameError:
			pass
		AudioFile.save()
		open_in(file_path)
		remove(file_path)
	else:
		sys.exit(0)

def WriteTags(sender):
	global FilePath
	i = sender.superview
	filename = sender.superview['ViewFile']
	if not FilePath == '':
		filename.text = '"{}"'.format(FilePath.split('/')[-1])
	else:
		tmpAudioFile = os.path.join(current_directory, i['FileName'].text)
		try:
			copyfile(tmpAudioFile, os.path.join(os.getenv('HOME'), 'tmp',  i['FileName'].text))
		except:
			pass
		FilePath = os.path.join(os.getenv('HOME'), 'tmp', i['FileName'].text)
		filename.text = '"{}"'.format(FilePath.split('/')[-1])
	
	Title = i['Title'].text
	Artist = i['Artist'].text
	AlbumArtist = i['AlbumArtist'].text
	Album = i['Album'].text
	Genre = i['Genre'].text
	Year = i['Year'].text
	TotalTrackNumbar = i['TotalTrackNum'].text
	TrackNumbar = i['TrackNum'].text
	TotalDiscNumbar = i['TotalDiscNum'].text
	DiscNumbar = i['DiscNum'].text

	AudioTagEdit(FilePath, title=Title, artist=Artist, albumartist=AlbumArtist, album=Album, genre=Genre, year=Year, track_num=TrackNumbar, total_track_num=TotalTrackNumbar, disc_num=DiscNumbar, total_disc_num=TotalDiscNumbar)

v = ui.load_view()
v.present('sheet')
