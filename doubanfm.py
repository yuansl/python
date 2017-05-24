# -*- Mode: python; coding: utf-8; tab-width: 8; indent-tabs-mode: t; -*-
#
# Copyright (C) 2017 yuansl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# The Rhythmbox authors hereby grant permission for non-GPL compatible
# GStreamer plugins to be used and distributed together with GStreamer
# and Rhythmbox. This permission is above and beyond the permissions granted
# by the GPL license by which Rhythmbox is covered. If you modify this code
# you may extend this exception to your version of the code, but you are not
# obligated to do so. If you do not wish to do so, delete this exception
# statement from your version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.
#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GObject, Gio, GLib, Peas
from gi.repository import RB
import rb
import urllib.parse
import json
from datetime import datetime
from urllib import parse
import time
from selenium import webdriver
import gettext
gettext.install('rhythmbox', RB.locale_dir())

# rhythmbox app registered with soundcloud with the account notverysmart@gmail.com
CLIENT_ID = 'e4ef6572c2baf401db2f64b4e0eae9ce'

class SoundCloudEntryType(RB.RhythmDBEntryType):
	def __init__(self):
		RB.RhythmDBEntryType.__init__(self, name='doubanfm')

	def do_get_playback_uri(self, entry):
		uri = entry.get_string(RB.RhythmDBPropType.MOUNTPOINT)
		return uri

	def do_can_sync_metadata(self, entry):
		return False


class DoubanfmPlugin(GObject.Object, Peas.Activatable):
	__gtype_name = 'DoubanfmPlugin'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		shell = self.object

		rb.append_plugin_source_path(self, "icons")

		db = shell.props.db

		self.entry_type = SoundCloudEntryType()
		db.register_entry_type(self.entry_type)

		model = RB.RhythmDBQueryModel.new_empty(db)
		self.source = GObject.new (SoundCloudSource,
					   shell=shell,
					   name=_("douban.fm"),
					   plugin=self,
					   query_model=model,
					   entry_type=self.entry_type,
					   icon=Gio.ThemedIcon.new("soundcloud-symbolic"))
		shell.register_entry_type_for_source(self.source, self.entry_type)
		self.source.setup()
		group = RB.DisplayPageGroup.get_by_id ("shared")
		shell.append_display_page(self.source, group)

	def do_deactivate(self):
		self.source.delete_thyself()
		self.source = None

class SoundCloudSource(RB.StreamingSource):
	def __init__(self, **kwargs):
		super(SoundCloudSource, self).__init__(kwargs)

		self.browser = None
		
		self.host = 'https://douban.fm'

		# default search type		
		self.default_st = 'all'

		self.doubanfm_cache = None

		self.search_count = 1
		self.search_types = {
			'all': {
				'label': _("Search all"),
				'placeholder': _("Search Artist/Song/MHZ/Scene on douban.fm"),
				'title': "",	# container view is hidden
				'endpoint': '/all.json',
				'containers': False
			},
			'artist': {
				'label': _("Search artist"),
				'placeholder': _("Search artists on douban.fm"),
				'title': "douban.fm artists",
				'endpoint': '/artist.json',
				'containers': True
			},
			'song': {
				'label': _("Search song"),
				'placeholder': _("Search songs on douban.fm"),
				'title': "douban.fm songs",
				'endpoint': '/song.json',
				'containers': True
			},
			'channel': {
				'label': _("Search channel"),
				'placeholder': _("Search channels on douban.fm"),
				'title': "douban.fm channels",
				'endpoint': '/channel.json',
				'containers': True
			},
			'songlist': {
				'label': _("Search songlist"),
				'placeholder': _("Search songlists on douban.fm"),
				'title': "douban.fm songlists",
				'endpoint': '/songlist.json',
				'containers': True
			}
		}

		self.container_types = {
			'user': {
				'attributes': ['username', 'kind', 'uri', 'permalink_url', 'avatar_url', 'description'],
				'tracks-url': '/tracks.json',
				'tracks-type': 'plain',
			},
			'playlist': {
				'attributes': ['title', 'kind', 'uri', 'permalink_url', 'artwork_url', 'description'],
				'tracks-url': '.json',
				'tracks-type': 'playlist',
			},
			'group': {
				'attributes': ['name', 'kind', 'uri', 'permalink_url', 'artwork_url', 'description'],
				'tracks-url': '/tracks.json',
				'tracks-type': 'plain',
			},
		}

	def hide_entry_cb(self, entry):
		shell = self.props.shell
		shell.props.db.entry_set(entry, RB.RhythmDBPropType.HIDDEN, True)

	def new_model(self):
		shell = self.props.shell
		plugin = self.props.plugin
		db = shell.props.db

		self.search_count = self.search_count + 1
		q = GLib.PtrArray()
		db.query_append_params(q, RB.RhythmDBQueryType.EQUALS, RB.RhythmDBPropType.TYPE, plugin.entry_type)
		db.query_append_params(q, RB.RhythmDBQueryType.EQUALS, RB.RhythmDBPropType.LAST_SEEN, self.search_count)
		model = RB.RhythmDBQueryModel.new_empty(db)

		db.do_full_query_async_parsed(model, q)
		self.props.query_model = model
		self.songs.set_model(model)

	def add_track(self, db, entry_type, item):
		location = item['url']
		entry = db.entry_lookup_by_location(location)
		if entry:
			db.entry_set(entry, RB.RhythmDBPropType.LAST_SEEN, self.search_count)
		else:
			entry = RB.RhythmDBEntry.new(db, entry_type, item['url'])
			db.entry_set(entry, RB.RhythmDBPropType.MOUNTPOINT, item['url'])
			home_page = 'https://douban.fm/song/%sg%s' % (item['sid'], item['ssid'])
			db.entry_set(entry, RB.RhythmDBPropType.LOCATION, home_page)
			db.entry_set(entry, RB.RhythmDBPropType.TITLE, item['title'])
			db.entry_set(entry, RB.RhythmDBPropType.ARTIST, item['artist'])			
			db.entry_set(entry, RB.RhythmDBPropType.ALBUM, item['albumtitle'])
			genre = ''
			for singer in item['singers']:
				for gen in singer['genre']:
					genre = genre + gen
			db.entry_set(entry, RB.RhythmDBPropType.GENRE, genre)
			db.entry_set(entry, RB.RhythmDBPropType.DURATION, int(item['length']))
			db.entry_set(entry, RB.RhythmDBPropType.LAST_SEEN, self.search_count)
			db.entry_set(entry, RB.RhythmDBPropType.BEATS_PER_MINUTE, int(item.get('kbps', '128')))
			db.entry_set(entry, RB.RhythmDBPropType.MB_ALBUMID, item.get('albumtitle', ''))
			public_year = item.get('public_time', '')
			if public_year == '':
				public_year = '1980'
			release_year = int(public_year)
			date = GLib.Date.new_dmy(item.get('release_day', 1), item.get('release_month', 1), release_year)
			db.entry_set(entry, RB.RhythmDBPropType.DATE, date.get_julian())
		db.commit()

	def add_container(self, item):
		k = item['kind']
		if k not in self.container_types:
			return

		ct = self.container_types[k]
		self.containers.append([item.get(i) for i in ct['attributes']])

	def search_tracks_api_cb(self, tracks):
		if tracks is None:
			return

		shell = self.props.shell
		db = shell.props.db
		entry_type = self.props.entry_type
		for song in tracks:
			self.add_track(db, entry_type, song)

	def search_containers_api_cb(self, data):
		if data is None:
			return
		
		for item in data:
			self.add_container(item)

	def resolve_api_cb(self, data):
		if data is None:
			return
		data = data.decode('utf-8')
		stuff = json.loads(data)

		if stuff['kind'] == 'track':
			shell = self.props.shell
			db = shell.props.db
			self.add_track(db, self.props.entry_type, stuff)
		else:
			self.add_container(stuff)
			# select, etc. too?

	def playlist_api_cb(self, data):
		if data is None:
			return

		shell = self.props.shell
		db = shell.props.db

		for item in data:
			self.add_track(db, self.props.entry_type, item)

	def cancel_request(self):
		if self.browser:
			self.browser.delete_all_cookies()
			self.browser.quit()
			self.browser = None
		if self.doubanfm_cache:
			self.doubanfm_cache.clear()
			self.doubanfm_cache = None

	def search_popup_cb(self, widget):
		self.search_popup.popup(None, None, None, None, 3, Gtk.get_current_event_time())

	def search_type_action_cb(self, action, parameter):
		self.search_type = parameter.get_string()
		print(parameter.get_string() + " selected")
		# return true if there is search text in the search entry
		if self.search_entry.searching():
			self.do_search()

		st = self.search_types[self.search_type]
		# set the 'placeholder' text in the search entry box
		self.search_entry.set_placeholder(st['placeholder'])

	def search_entry_cb(self, widget, term):
		self.search_text = term
		self.do_search()

	def doubanfm_search(self):
		""" 
		do search on douban.fm for you
		And there are four objects will be retured
		object #0 for type artist
		object #1 for type song
		object #2 for type channel
		object #3 for type songlist
		"""
		search_path = '/j/v2/query/all'
		query = { 'start':'0', 'limit':'5' }
		query['q'] = self.search_text
		url = self.host + search_path + '?' + parse.urlencode(query)
		data = self.doubanfm_get(url)
		return data

	def do_search(self):
		self.cancel_request()

		self.new_model()
		self.containers.clear()
		term = self.search_text
		if self.search_type not in self.search_types:
			print("not sure how to search for " + self.search_type)
			return

		# for container view
		print("searching for " + self.search_type + " matching " + term)
		st = self.search_types[self.search_type]
		self.container_view.get_column(0).set_title(st['title'])
		
		self.browser = webdriver.PhantomJS()
		search_results = self.doubanfm_search()

		self.doubanfm_cache = {}
		
		self.doubanfm_cache['song'] = search_results[1]['items']
		self.doubanfm_cache['all'] = search_results
		if st['containers']:
			self.scrolled.show()

			data = []
			if self.search_type == 'artist':
				artists = search_results[0]['items']
				for artist in artists:
					song = {}
					song['kind'] = 'user'
					song['username'] = artist['name_usual']
					song['uri'] = artist['channel']
					song['permalink_url'] = 'https://douban.fm/artist/%s/' % artist['id']
					data.append(song)

			elif self.search_type == 'channel':
				channels = search_results[2]['items']
				for channel in channels:
					song = {}
					song['kind'] = 'group'
					song['name'] = channel['title']
					song['uri'] = str(channel['id'])
					song['permalink_url'] = 'https://douban.fm'
					data.append(song)
			else:
				if self.search_type == 'song':
					items = search_results[1]['items']
					for item in items:
						song = {}
						song['kind'] = 'playlist'
						song['title'] = item['title'] + ' by ' + item['artist']
						song['uri'] = item['id']
						song['permalink_url'] = 'https://douban.fm/song/%sg%s/' % (item['sid'], item['ssid'])
						data.append(song)
				else:
					items = search_results[3]['items']
					for item in items:
						song = {}
						song['kind'] = 'playlist'
						song['title'] = item['title']
						song['uri'] = str(item['id'])
						song['permalink_url'] = 'https://douban.fm/songlist/%d/' % item['id']
						data.append(song)
			
			self.search_containers_api_cb(data)
		else:
			self.scrolled.hide()

			songs = search_results[1]['items']
			songlist = search_results[3]['items']
			for song in songlist:
				data = self.doubanfm_get_songlist(song['id'])
				for song in data:
					songs.append(song)
			
			self.search_tracks_api_cb(songs)
			
	def doubanfm_get(self, url):
		self.browser.get(url)
		body = self.browser.find_element_by_tag_name('body')
		data = json.loads(body.text)
		return data
	
	def doubanfm_get_artist(self, artist_id):
		"""
		get information about artist from douban.fm
		returned data contains: name, genre, channel_id, region, liked_count, etc...
		"""
		artist_path = '/j/v2/artist/%s/' % artist_id
		url = self.host + artist_id
		data = self.doubanfm_get(url)
		return data

	# search MHZ
	def doubanfm_get_channel_info(self, channel_id):
		channel_path = '/j/v2/channel_info'
		query = 'id=%s' % channel_id
		url = self.host + channel_path + '?' + query
		channel_info = self.doubanfm_get(url)
		print('channel_info: ', str(channel_info))
		data = channel_info['data']
		channels = data['channels']
		song_num = channels[0].get('song_num', 0)
		return song_num

	# search playlist
	def doubanfm_get_playlist(self, channel_id):
		data = {
			'channel': channel_id,
			'kbps': '192',
			'client': 's:mainsite|y:3.0',
			'app_name': 'radio_website',
			'version': '100',
			'type': 'n'
		}
		playlist_path = '/j/v2/playlist'
		query = parse.urlencode(data)
		url = self.host + playlist_path + '?' + query
		print('url: ' + url)
		song_info = self.doubanfm_get(url)
		song = song_info.get('song', None)
		return song

	def doubanfm_get_songlist(self, id):
		"""get songlist from douban.fm with given songlist id"""
		songlist_path = '/j/v2/songlist/%s/' % id
		query = 'kbps=192'
		url = self.host + songlist_path + '?' + query
		data = self.doubanfm_get(url)
		return data['songs']
	
	def doubanfm_fetch_cache(self, tracks_type, uri):
		if tracks_type == 'playlist':
			if self.search_type == 'song':
				data = []
				songs = self.doubanfm_cache['song']
				for song in songs:
					if song['id'] == uri:
						data = [song]
						break
			else:
				data = self.doubanfm_cache['songlist']
			self.playlist_api_cb(data)
		else:
			if self.search_type == 'artist':
				data = self.doubanfm_cache['artist'][self.search_type]
			else:
				data = self.doubanfm_cache['channel']
			self.search_tracks_api_cb(data)
			
			
	def doubanfm_retrive(self, tracks_type, uri):
		self.cancel_request()
		self.browser = webdriver.PhantomJS()
		self.doubanfm_cache = {}
		if tracks_type == 'playlist':
			if self.search_type == 'songlist':
				data = self.doubanfm_get_songlist(uri)
				self.doubanfm_cache['songlist'] = {}
				self.doubanfm_cache['songlist'][model.title] = data
			else:   # search_type is song
				songs = self.doubanfm_cache['song']
				for song in songs:
					if song['id'] == uri:
						data = [song]
						break

				self.playlist_api_cb(data)
		else:
			# tracks-type 'plain'
			# for container type: user and group
			data = self.doubanfm_get_playlist(uri)
			if self.search_type == 'artist':
				self.doubanfm_cache['artist'] = {}
				self.doubanfm_cache['artist'][self.search_type] = data
			else:
				self.doubanfm_cache['channel'] = {}
				self.doubanfm_cache['channel'][self.search_type] = data
			self.search_tracks_api_cb(data)
			
	def doubanfm_cache_exists(self):
		if self.doubanfm_cache is None:
			return False
		return self.doubanfm_cache.get(self.search_type, None) != None
		
	# callback function for selection of container_view
	def selection_changed_cb(self, selection):
		self.new_model()
		
		self.build_sc_menu()

		(model, aiter) = selection.get_selected()
		if aiter is None:
			return
		[itemtype, uri] = model.get(aiter, 1, 2)
		if itemtype not in self.container_types:
			return

		print("loading %s %s" % (itemtype, uri))
		ct = self.container_types[itemtype]
		
		if self.doubanfm_cache_exists() is True:
			print('artist exists %s' % self.search_type)
			print('cache[artist] = ' + str(self.doubanfm_cache['artist']))
			self.doubanfm_fetch_cache(ct['tracks-type'], uri)
		else:
			self.doubanfm_retrive(ct['tracks-type'], uri)

	def sort_order_changed_cb(self, obj, pspec):
		obj.resort_model()

	def songs_selection_changed_cb(self, songs):
		self.build_sc_menu()

	def playing_entry_changed_cb(self, player, entry):
		self.build_sc_menu()
		if not entry:
			return
		if entry.get_entry_type() != self.props.entry_type:
			return

		au = entry.get_string(RB.RhythmDBPropType.MB_ALBUMID)
		if au:
			key = RB.ExtDBKey.create_storage("title", entry.get_string(RB.RhythmDBPropType.TITLE))
			key.add_field("artist", entry.get_string(RB.RhythmDBPropType.ARTIST))
			self.art_store.store_uri(key, RB.ExtDBSourceType.EMBEDDED, au)

	def open_uri_action_cb(self, action, param):
		shell = self.props.shell
		window = shell.props.window
		screen = window.get_screen()

		uri = param.get_string()
		print('URI = ' + uri)
		Gtk.show_uri(screen, uri, Gdk.CURRENT_TIME)

	def build_sc_menu(self):
		menu = {}

		# playing track
		shell = self.props.shell
		player = shell.props.shell_player
		entry = player.get_playing_entry()
		if entry is not None and entry.get_entry_type() == self.props.entry_type:
			url = entry.get_string(RB.RhythmDBPropType.LOCATION)
			
			menu[url] = _("View '%(title)s' on douban.fm") % {'title': entry.get_string(RB.RhythmDBPropType.TITLE) }
			# artist too?


		# selected track
		if self.songs.have_selection():
			entry = self.songs.get_selected_entries()[0]
			url = entry.get_string(RB.RhythmDBPropType.LOCATION)
			menu[url] = _("View '%(title)s' on douban.fm") % {'title': entry.get_string(RB.RhythmDBPropType.TITLE) }
			# artist too?

		# selected container
		selection = self.container_view.get_selection()
		(model, aiter) = selection.get_selected()
		if aiter is not None:
			[name, url] = model.get(aiter, 0, 3)
			menu[url] = _("View '%(container)s' on douban.fm") % {'container': name}

		if len(menu) == 0:
			self.sc_button.set_menu_model(None)
			self.sc_button.set_sensitive(False)
			return None

		m = Gio.Menu()
		for u in menu:
			i = Gio.MenuItem()
			i.set_label(menu[u])
			i.set_action_and_target_value("win.soundcloud-open-uri", GLib.Variant.new_string(u))
			m.append_item(i)
		self.sc_button.set_menu_model(m)
		self.sc_button.set_sensitive(True)

	def setup(self):
		shell = self.props.shell

		builder = Gtk.Builder()
		builder.add_from_file(rb.find_plugin_file(self.props.plugin, "soundcloud.ui"))

		self.scrolled = builder.get_object("container-scrolled")
		self.scrolled.set_no_show_all(True)
		self.scrolled.hide()

		self.search_entry = RB.SearchEntry(spacing=6)
		self.search_entry.props.explicit_mode = True

		action = Gio.SimpleAction.new("soundcloud-search-type", GLib.VariantType.new('s'))
		action.connect("activate", self.search_type_action_cb)
		shell.props.window.add_action(action)

		m = Gio.Menu()
		for st in sorted(self.search_types):
			i = Gio.MenuItem()
			i.set_label(self.search_types[st]['label'])
			i.set_action_and_target_value("win.soundcloud-search-type", GLib.Variant.new_string(st))
			m.append_item(i)

		self.search_popup = Gtk.Menu.new_from_model(m)

		action.activate(GLib.Variant.new_string(self.default_st))
		grid = builder.get_object("soundcloud-source")
		self.search_entry.connect("search", self.search_entry_cb)
		self.search_entry.connect("activate", self.search_entry_cb)
		self.search_entry.connect("show-popup", self.search_popup_cb)
		self.search_entry.set_size_request(400, -1)
		builder.get_object("search-box").pack_start(self.search_entry, False, True, 0)
		self.search_popup.attach_to_widget(self.search_entry, None)
		self.containers = builder.get_object("container-store")
		self.container_view = builder.get_object("containers")
		self.container_view.set_model(self.containers)

		action = Gio.SimpleAction.new("soundcloud-open-uri", GLib.VariantType.new('s'))
		action.connect("activate", self.open_uri_action_cb)
		shell.props.window.add_action(action)

		r = Gtk.CellRendererText()
		c = Gtk.TreeViewColumn("", r, text=0)
		self.container_view.append_column(c)

		self.container_view.get_selection().connect('changed', self.selection_changed_cb)

		self.songs = RB.EntryView(db=shell.props.db,
					  shell_player=shell.props.shell_player,
					  is_drag_source=True,
					  is_drag_dest=False,
					  shadow_type=Gtk.ShadowType.NONE)
		self.songs.append_column(RB.EntryViewColumn.TITLE, True)
		self.songs.append_column(RB.EntryViewColumn.GENRE, True)
		self.songs.append_column(RB.EntryViewColumn.ARTIST, True)
		self.songs.append_column(RB.EntryViewColumn.ALBUM, True)
		self.songs.append_column(RB.EntryViewColumn.YEAR, True)
		self.songs.append_column(RB.EntryViewColumn.DURATION, True)
		self.songs.append_column(RB.EntryViewColumn.BPM, False)
		self.songs.append_column(RB.EntryViewColumn.FIRST_SEEN, False)
		self.songs.append_column(RB.EntryViewColumn.RATING, True)
		self.songs.set_model(self.props.query_model)
		self.songs.connect("notify::sort-order", self.sort_order_changed_cb)
		self.songs.connect("selection-changed", self.songs_selection_changed_cb)
		paned = builder.get_object("paned")
		paned.pack2(self.songs)

		self.bind_settings(self.songs, paned, None, True)

		# 'powerd by soundcloud' button
		self.sc_button = Gtk.MenuButton()
		self.sc_button.set_relief(Gtk.ReliefStyle.NONE)
		img = Gtk.Image.new_from_file(rb.find_plugin_file(self.props.plugin, "powered-by-soundcloud.png"))
		self.sc_button.add(img)
		box = builder.get_object("soundcloud-button-box")
		box.pack_start(self.sc_button, True, True, 0)

		self.build_sc_menu()

		self.pack_start(grid, expand=True, fill=True, padding=0)
		grid.show_all()

		self.art_store = RB.ExtDB(name="album-art")
		player = shell.props.shell_player
		player.connect('playing-song-changed', self.playing_entry_changed_cb)

	def do_get_entry_view(self):
		return self.songs

	def do_get_playback_status(self, text, progress):
		return self.get_progress()

	def do_can_copy(self):
		return False

GObject.type_register(SoundCloudSource)
