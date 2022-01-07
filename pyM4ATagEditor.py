import ui, photos, sys, os.path, appex, base64
from console import open_in
from mutagen.mp4 import MP4, MP4Cover
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

def AudioTagEdit(AS):
	i = AS.superview
	title = i['Title'].text
	if title == '':
		title = None
	artist = i['Artist'].text
	if artist == '':
		artist = None
	albumartist = i['AlbumArtist'].text
	if albumartist == '':
		albumartist = None
	album = i['Album'].text
	if album == '':
		album = None
	genre = i['Genre'].text
	if genre == '':
		genre = None
	year = i['Year'].text
	if year == '':
		year = None
	total_track_num = i['TotalTrackNum'].text
	if total_track_num == '':
		total_track_num = None
	track_num = i['TrackNum'].text
	if track_num == '':
		track_num = None
	total_disc_num = i['TotalDiscNum'].text
	if total_disc_num == '':
		total_disc_num = None
	disc_num = i['DiscNum'].text
	if disc_num == '':
		disc_num = None

	if FilePath.split('/')[-1].split('.')[-1].lower() == 'm4a':
		AudioFile = MP4(FilePath)
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
		open_in(FilePath)
		remove(FilePath)
	else:
		sys.exit(0)

def LoadFileName(sf):
	global FilePath
	filename = sf.superview
	if not FilePath == '':
		filename['ViewFile'].text = '"{}"'.format(FilePath.split('/')[-1])
	else:
		try:
			if filename['FileName'].text[0] + filename['FileName'].text[1] == './':
				tmpAudioFile = os.path.join(current_directory, filename['FileName'].text)
			else:
				tmpAudioFile = os.path.join(filename['FileName'].text)
		except:
			tmpAudioFile = os.path.join(filename['FileName'].text)
		try:
			copyfile(tmpAudioFile, os.path.join(os.getenv('HOME'), 'tmp',  filename['FileName'].text))
		except:
			pass
		FilePath = os.path.join(os.getenv('HOME'), 'tmp', filename['FileName'].text)
		filename['ViewFile'].text = '"{}"'.format(FilePath.split('/')[-1])

class M4A_TagEditor(ui.View):
	def will_close(self):
		try:
			remove(FilePath)
		except:
			pass

class HELP(ui.View):
	def __init__(self):
		w, h = ui.get_screen_size()
		self.TV = ui.TextView()
		self.TV.width = w*1
		self.TV.height = h*1
		self.width = w*1
		self.height = h*1
		self.TV.editable = False
		self.TV.font = ('<system-bold>', 20)
		self.TV.text = base64.b64decode("CltNNEFUYWdFZGl0b3Ig44OY44Or44OX44Oa44O844K4XQoKW+S9v+OBhOaWuV0K44O7UHl0aG9uaXN0YTPjgYvjgonjga7loLTlkIg6CuOAjOODleOCoeOCpOODq+WQjeOAjeOBq+e3qOmbhuOBl+OBn+OBhG00YeODleOCoeOCpOODq+OBruODleODq+ODkeOCueOCkuWFpeWKm+OBl+OBpuOBj+OBoOOBleOBhOOAggoK44O75YWx5pyJ44Oh44OL44Ol44O844GL44KJ44Gu5aC05ZCIOgrjg5XjgqHjgqTjg6vjgpLplbfmirzjgZfnrYnjgaflhbHmnInjg6Hjg4vjg6Xjg7zjgpLplovjgY3jgIHjgIxSdW4gUHl0aG9uaXN0YSBTY3JpcHTjgI3jgYvjgonku7vmhI/jga7lkI3liY3jgavjgZfjgZ/jgqjjgq/jgrnjg4bjg7Pjgrfjg6fjg7PjgpLplovjgY/jgIIKClvlkITnqK7jg5zjgr/jg7Pjga7oqqzmmI5dCuODu+WFseacieOBleOCjOOBn+ODleOCoeOCpOODq+OBruihqOekujoK5YWx5pyJ44Oh44OL44Ol44O844GL44KJ6ZaL44GE44Gf44OV44Kh44Kk44Or44KS6KGo56S644GV44Gb44KL54K644Gu44Oc44K/44Oz44Gn44GZ44CCCgrjg7vjg5jjg6vjg5fjg5zjgr/jg7M6CuOBk+OBruODmuODvOOCuOOCkumWi+OBj+ODnOOCv+ODs+OBp+OBmeOAggoK44O744OH44O844K/44Gu6Kqt44G/6L6844G/OgrlhbHmnInjg6Hjg4vjg6Xjg7zjgYvjgonplovjgYTjgZ/jg5XjgqHjgqTjg6vjgYvjgonjg6Hjgr/jg4fjg7zjgr/jgpLoqq3jgb/ovrzjgb/jgb7jgZnjgIIKCuODu+eUu+WDj+OBruiqreOBv+i+vOOBvzoK44OV44Kp44OI44Op44Kk44OW44Op44Oq44O844GL44KJ44Ki44Or44OQ44Og44K444Oj44Kx44OD44OI44KS6YG444G544G+44GZ44CCCgrjg7vjgr/jgrDjgpLoqK3lrprjgZfjgabmm7jjgY3lh7rjgZk6CuioreWumuOBl+OBn+ODoeOCv+ODh+ODvOOCv+OCkuODleOCoeOCpOODqyjkuIDmmYLjg5XjgqHjgqTjg6sp44Gr5pu444GN5Ye644GX44Gm5LuW44Gu44Ki44OX44Oq44GL44KJ6ZaL44GR44KL44KI44GG44Gr44GX44G+44GZ44CCCgpbUSZBXQrjg7vkuIDmmYLjg5XjgqHjgqTjg6vjga7mtojjgZfmlrk6CuW3puS4iuOBq+OBguOCi+OAjOKdjOOAjeODnOOCv+ODs+OCkuaKvOOBmeOBqOS4gOaZguODleOCoeOCpOODq+OBjOWJiumZpOOBleOCjOOCi+anmOOBq+OBquOBo+OBpuOBiuOCiuOAgeaJi+WLleOBp+a2iOOBl+OBn+OBhOWgtOWQiOOBr+OAjCRIT01FL3RtcOOAjeOBq+S4gOaZguODleOCoeOCpOODq+OCkuS/neWtmOOBl+OBpuOBhOOBvuOBmeOAggoK44O75LiA5pmC44OV44Kh44Kk44Or44KS5L2V5pWF5L2c5oiQ44GZ44KL44GLOgrlhbHmnInjg6Hjg4vjg6Xjg7zjga7liLbntITkuIrlhbHmnInjgZfjgZ/jg5XjgqHjgqTjg6vjgbjnm7TmjqXmm7jjgY3ovrzjgoHjgarjgYTjgojjgYbjgafjgZnjgIIK44Gq44Gu44Gn5LiA5pmC44OV44Kh44Kk44Or44KSUHl0aG9uaXN0YTPjgbjjgrPjg5Tjg7zjgZfjgabjgYvjgonmm7jjgY3lh7rjgZfjgabjgYTjgb7jgZnjgIIKCuODu+S9leaVhU00QeWwgueUqOOBquOBruOBizoK5LuK44Gp44GNTTRB44Gg44GR44Gu44K/44Kw44Gu5pu444GN5Ye644GX44Gv5L2/44GE5Yud5omL44GM6ZmQ44KJ44KM44KL44Gu44Gn44GZ44GM44CBUHl0aG9uaXN0YTPjgYzkvb/jgYjjgovjg6Hjg6Ljg6rjg7zjgrXjgqTjgrrjgYzpmZDjgonjgozjgabjgYTjgovjga7jgadGbGFj562J44KS6Kqt44G/6L6844KA44Go44Kv44Op44OD44K344Ol44GX44Gm44GX44G+44GG44Gu44Go44CB44Ki44Or44OQ44Og44K444Oj44Kx44OD44OI44KS6Kqt44G/5pu444GN44GZ44KL44Gu44GM6KSH6ZuR44Gq44Gu44GnTTRB44Gg44GR44Gr57We44KK44G+44GX44Gf44CCCgoKCgo=").decode()
		self.TV.text_color = '#fffaf4'
		self.TV.background_color = '#292929'
		self.background_color = '#292929'
		self.tint_color = '#ff0000'
		self.name = 'ヘルプページ'
		self.add_subview(self.TV)

def HelpPage(_se):
	HELP().present('sheet')

v = ui.load_view()
v.present('sheet')
