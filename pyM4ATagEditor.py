import ui, photos, sys, os.path, appex
from console import open_in
from mutagen.mp4 import MP4, MP4Cover
from os import getcwd as pwd, remove
from shutil import copyfile
current_directory = pwd()
FilePath = ''
HelpText = """[M4ATagEditor ヘルプページ]\n
[使い方]
・Pythonista3からの場合:
「ファイル名」に編集したいm4aファイルのフルパスを入力してください。\n
・共有メニューからの場合:
ファイルを長押し等で共有メニューを開き、「Run Pythonista Script」から任意の名前にしたエクステンションを開く。\n
[各種ボタンの説明]
・共有されたファイルの表示:
共有メニューから開いたファイルを表示させる為のボタンです。\n
・ヘルプボタン:
このページを開くボタンです。\n
・データの読み込み:
共有メニューから開いたファイルからメタデータを読み込みます。\n
・画像の読み込み:
フォトライブラリーからアルバムジャケットを選べます。\n
・タグを設定して書き出す:
設定したメタデータをファイル(一時ファイル)に書き出して他のアプリから開けるようにします。\n
[Q&A]
・一時ファイルの消し方:
左上にある「❌」ボタンを押すと一時ファイルが削除される様になっており、手動で消したい場合は「$HOME/tmp」に一時ファイルを保存しています。\n
・一時ファイルを何故作成するか:
共有メニューの制約上共有したファイルへ直接書き込めないようです。\nなので一時ファイルをPythonista3へコピーしてから書き出しています。\n
・何故M4A専用なのか:
今どきM4Aだけのタグの書き出しは使い勝手が限られるのですが、Pythonista3が使えるメモリーサイズが限られているのでFlac等を読み込むとクラッシュしてしまうのと、アルバムジャケットを読み書きするのが複雑なのでM4Aだけに絞りました。\n\n\n\n\n"""

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
		self.TV.text = HelpText
		self.TV.text_color = '#fffaf4'
		self.TV.background_color = '#292929'
		self.background_color = '#292929'
		self.name = 'ヘルプページ'
		self.add_subview(self.TV)

def HelpPage(_se):
	HELP().present('sheet')

v = ui.load_view()
v.present('sheet')
