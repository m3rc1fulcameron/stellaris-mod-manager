#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import os
import sys
import json
from collections import defaultdict
import datetime
import logging
from tkscrolledframe import ScrolledFrame
from enum import Enum

VERSION = '0.0.1'
MOD_LIST_WIDTH = 60
IGNORED_FILES = ['modname.mod', 'descriptor.mod', 'thumbnail.jpg', 'thumbnail.png']

class Issue(object):
	class IssueSeverity(Enum):
		NOTICE = 1
		WARNING = 2
		ERROR = 3
	class IssueType(Enum):
		LOAD_ORDER = 1
		UNRESOLVED_OVERWRITE = 2
		UNKNOWN_MOD = 3
		
	def __init__(self, severity, issue_type, src_mod, aux_mods=[], description=None):
		self.severity = severity
		self.issue_type = issue_type
		self.src_mod = src_mod
		self.aux_mods = aux_mods
		self.description = description
		
	def pprint(self):
		output = ''
		if self.severity == Issue.IssueSeverity.NOTICE:
			output += '[NOTICE] '
		elif self.severity == Issue.IssueSeverity.WARNING:
			output += '[WARNING] '
		elif self.severity == Issue.IssueSeverity.ERROR:
			output += '[ERROR] '
		if self.issue_type == Issue.IssueType.LOAD_ORDER:
			output += 'Load order violation: %s; %s' % (self.src_mod, self.description if self.description != None else '')
		elif self.issue_type == Issue.IssueType.UNRESOLVED_OVERWRITE:
			mods = ', '.join(m for m in self.aux_mods)
			output += 'Unresolved overwrite: %s (%s); %s' % (self.src_mod, mods, self.description if self.description != None else '')
		elif self.issue_type == Issue.IssueType.UNKNOWN_MOD:
			output += 'Unknown mod: %s; %s' % (self.src_mod, self.description if self.description != None else '')
		return output

class Mod(object):
	@staticmethod
	def from_registry_data(mid, load_order, data):
		raw = json.dumps(data, indent=4, separators=(',', ': '))
		return Mod(mid, load_order, raw, **data)
	def __init__(self, mid, load_order, raw, steamId=None, displayName=None, tags=[], timeUpdated=None, source=None, thumbnailUrl=None, dirPath=None, status=None, gameRegistryId=None, requiredVersion=None, cause=None, thumbnailPath=None, **kwargs):
		self.mid = mid
		if displayName != None:
			self.name = displayName
		elif gameRegistryId != None:
			self.name = gameRegistryId
		else:
			self.name = mid
		self.load_order = load_order
		self.raw = raw
		self.steam_id = steamId
		self.tags = tags
		self.last_updated = datetime.datetime.fromtimestamp(timeUpdated) if timeUpdated != None else None
		self.source = source
		self.thumbnail_url = thumbnailUrl
		self.install_dir = dirPath
		self.status = status
		self.game_registry_id = gameRegistryId
		self.required_version = requiredVersion
		self.cause = cause
		self.thumbnail_path = thumbnailPath
		
class Conflict(object):
	def __init__(file, mods):
		self.file = file
		self.mods = mods
		
	def get_actual_provider():
		pass
		
class SMM(tk.Tk):
	def get_stellaris_dir(self):
		if sys.platform.startswith('linux'):
			return os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Stellaris')
		elif sys.platform.startswith('darwin'):
			return os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Stellaris')
		elif sys.platform.startswith('win32'):
			return os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Stellaris')
		else:
			raise Exception('Unsupported platform %s' % sys.platform)
	def get_mods_registry_path(self):
		return os.path.join(self.get_stellaris_dir(), 'mods_registry.json')
	def get_load_order_path(self):
		return os.path.join(self.get_stellaris_dir(), 'dlc_load.json')

	def get_mods(self):
		registry_path = self.get_mods_registry_path()
		load_order_path = self.get_load_order_path()
		mods = {}
		with open(registry_path, 'r') as fp:
			mods = json.loads(fp.read())
		load_order = defaultdict(lambda: -1)
		with open(load_order_path, 'r') as fp:
			enabled = json.loads(fp.read())['enabled_mods']
			load_order.update({enabled[i]: i for i in range(len(enabled))})
		return [Mod.from_registry_data(id, load_order[data['gameRegistryId']], data) for id, data in mods.items()]

	def scan_conflicts(self, mods):
		uses = {}
		for mod in mods:
			mod_dir = mod.install_dir
			descriptor_path = os.path.join(mod_dir, 'descriptor.mod')
			if not os.path.isfile(descriptor_path):
				logging.error("ERROR: %s is not a valid mod (%s)" % (mod_dir, mod.name))
				continue
			print("Working on %s (%s)" % (mod_dir, mod.name))
			files = [os.path.relpath(os.path.join(root, name), mod_dir) for root, dirs, files in os.walk(mod_dir) for name in files]
			print("Found %d files" % len(files))
			for file in files:
				if not file in uses.keys():
					uses[file] = []
				if not mod in uses[file]:
					uses[file].append(mod)
		conflicts = {file: use for file, use in uses.items() if len(use) > 1 and file not in IGNORED_FILES}
		return conflicts
		
	def scan_issues(self, mods, conflicts, db):
		issues = []
		s_mods = [m for m in sorted(mods, key=lambda x: x.load_order) if m.load_order >= 0]
		# Scan for known load order issues
		for i in range(len(s_mods)):
			mod = s_mods[i]
			if mod.load_order < 0:
				continue
			if not mod.name in db.keys():
				issues.append(Issue(Issue.IssueSeverity.WARNING, Issue.IssueType.UNKNOWN_MOD, mod.name))
				continue
			before = db[mod.name]["before"]
			for mod2 in s_mods[:i]:
				if mod2.name in before:
					issues.append(Issue(Issue.IssueSeverity.ERROR, Issue.IssueType.LOAD_ORDER, mod.name, [mod2.name]))
				if mod2.name in db.keys():
					after = db[mod2.name]["after"]
					if mod.name in after:
						issues.append(Issue(Issue.IssueSeverity.ERROR, Issue.IssueType.LOAD_ORDER, mod2.name, [mod.name]))
		# Scan for unresolved file conflicts
		for file, providers in conflicts.items():
			s_providers = [m for m in sorted(providers, key=lambda x: x.load_order) if m.load_order >= 0]
			if len(s_providers) == 0:
				continue
			fail = False
			# We can't reason about the conflict if *any* of the providing mods are unknown
			for mod in s_providers:
				if not mod.name in db.keys():
					fail = True
					break
			if fail:
				issues.append(Issue(Issue.IssueSeverity.WARNING, Issue.IssueType.UNRESOLVED_OVERWRITE, s_providers[-1].name, [m.name for m in s_providers[:-1]], description=file + ' (unknown mods)'))
				continue
			top = s_providers[-1]
			providers_names = set(m.name for m in s_providers[:-1] if not db[m.name]["allow_overwrite"])
			patches_names = set(db[top.name]["patches"])
			unresolved_names = list(providers_names - patches_names)
			if len(unresolved_names) > 0:
				severity = Issue.IssueSeverity.ERROR
				if file.endswith(".dds"):
					severity = Issue.IssueSeverity.WARNING
				issues.append(Issue(severity, Issue.IssueType.UNRESOLVED_OVERWRITE, top.name, unresolved_names, description=file))
		return issues
		
	def load_db(self):
		with open('smm_db.json') as fp:
			return json.loads(fp.read())
		
	def show_info(self, mod):
		self.rp.show_info(mod)
		
	def refresh(self):
		mods = self.get_mods()
		conflicts = self.scan_conflicts(mods)
		db = self.load_db()
		issues = self.scan_issues(mods, conflicts, db)
		self.ml.set_mods(mods)
		self.rp.show_conflicts(conflicts)
		self.rp.show_issues(issues)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title('Stellaris Mod Manager v' + VERSION)
		self.state('zoomed')
		
		self.mb = SMMMenu(self, self)
		self.ml = ModList(self, self)
		self.rp = RightPane(self, self)
		self.refresh()
		
class SMMMenu(tk.Menu):
	def refresh(self):
		self.controller.refresh()

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		
		self.add_command(label="Refresh", command=self.refresh)
		parent.config(menu=self)

class ModList(tk.Listbox):
	def handle_select(self, evt):
		s = self.curselection()
		if len(s) < 1:
			return
		i = int(s[0])
		mod = self.mods[i]
		self.controller.show_info(mod)
		
	def set_mods(self, mods):
		self.mods = mods
		self.delete(0, tk.END)
		for mod in mods:
			self.insert(tk.END, '{} ({})'.format(mod.name, mod.load_order if mod.load_order >= 0 else 'disabled'))

	def __init__(self, parent, controller):
		super().__init__(parent, selectmode=tk.SINGLE, width=MOD_LIST_WIDTH)
		self.pack(fill=tk.Y, side=tk.LEFT)
		self.mods = []
		
		self.controller = controller
		self.bind('<<ListboxSelect>>', self.handle_select)
		
class ModInfo(tk.Frame):
	install_path = None
	def show_info(self, mod):
		self.set_prop('name', mod.name)
		self.set_prop('last_updated', mod.last_updated.strftime('%c') if mod.last_updated != None else '<unknown>')
		self.set_prop('load_order', mod.load_order)
		self.set_prop('id', mod.mid)
		self.set_prop('game_registry_id', mod.game_registry_id)
		self.set_prop('steam_id', mod.steam_id)
		self.set_prop('required_version', mod.required_version)
		self.set_prop('install_dir', mod.install_dir)
		self.install_path = mod.install_dir
		self.raw_data.set(mod.raw)
		
	def open_in_file_explorer(self):
		if self.install_path == None:
			return
		if sys.platform=='win32':
			os.startfile(self.install_path)
		elif sys.platform=='darwin':
			subprocess.Popen(['open', self.install_path])
		else:
			try:
				subprocess.Popen(['xdg-open', self.install_path])
			except OSError:
				logging.error("Unable to find a valid method for opening a file explorer.")
		
	def set_prop(self, key, val):
		prop = self.props[key]
		prop[1].set(prop[0] + ': ' + (str(val) if val != None else '<null>'))
		
	def init_prop(self, key, name, initval=''):
		if name in self.props.keys():
			raise Exception('Tried to init duplicate prop ' + name)
		var = tk.StringVar()
		l = tk.Label(self, textvariable=var, bg='white')
		l.pack(side=tk.TOP, anchor=tk.NW)
		self.props[key] = (name, var, l)

	props = {}
	def __init__(self, parent):
		super().__init__(parent, bg='white')
		self.pack(fill=tk.BOTH, expand=1)
		
		self.btn_show_in_fp = tk.Button(self, text="Open Install Dir", command=self.open_in_file_explorer)
		self.btn_show_in_fp.pack(side=tk.RIGHT, anchor=tk.NE)
		self.init_prop('name', 'Name')
		self.init_prop('last_updated', 'Last Updated')
		self.init_prop('load_order', 'Current Load Order')
		self.init_prop('id', 'ID')
		self.init_prop('game_registry_id', 'Registry ID')
		self.init_prop('steam_id', 'Steam ID')
		self.init_prop('required_version', 'Required Game Version')
		self.init_prop('install_dir', 'Install Directory')
		self.w_raw_data_label = tk.Label(self, text='Raw JSON:', bg='white')
		self.w_raw_data_label.pack(side=tk.TOP, anchor=tk.NW)
		self.raw_data = tk.StringVar()
		self.w_raw_data = tk.Message(self, textvariable=self.raw_data, anchor=tk.NW, relief=tk.SUNKEN, bg='white')
		self.w_raw_data.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
		
class Conflicts(ScrolledFrame):
	w_conflicts = []
	def show_conflicts(self, conflicts):
		for w in self.w_conflicts:
			w.destroy()
		self.w_conflicts = []
		for file, sources in conflicts.items():
			s_sources = sorted(sources, key=lambda x: x.load_order)
			nl = len(s_sources) + 1
			msg = file + '\n\t' + '\n\t'.join("%s (%d)" % (m.name, m.load_order) for m in s_sources)
			cf = tk.Text(self.inf, bg='white', height=nl)
			cf.insert(tk.INSERT, msg)
			cf.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=1)
			self.w_conflicts.append(cf)
			
	def _handle_resize(self, evt):
		if evt.width != self.sizer.winfo_width():
			self.sizer.config(width=evt.width)

	def __init__(self, parent):
		super().__init__(parent, bg='white')
		self.pack(fill=tk.BOTH, expand=1)
		self.inf = self.display_widget(tk.Frame)
		self.inf.config(bg='white')
		self.sizer = tk.Frame(self.inf, height=1)
		self.sizer.pack()
		self.bind('<Configure>', self._handle_resize)
		
class Issues(ScrolledFrame):
	w_issues = []
	def show_issues(self, issues):
		for w in self.w_issues:
			w.destroy()
		self.w_issues = []
		for issue in issues:
			msg = ''
			col_bg = 'white'
			nl = 1
			if issue.severity == Issue.IssueSeverity.NOTICE:
				msg += '[NOTICE] '
			elif issue.severity == Issue.IssueSeverity.WARNING:
				msg += '[WARNING] '
				col_bg = 'orange'
			elif issue.severity == Issue.IssueSeverity.ERROR:
				msg += '[ERROR] '
				col_bg = 'salmon'
			if issue.issue_type == Issue.IssueType.LOAD_ORDER:
				msg += 'A load order violation occurred'
				msg += '\n\t%s Mod load order should be reversed %s' % (issue.src_mod, issue.aux_mods[0])
				nl = 2
			elif issue.issue_type == Issue.IssueType.UNRESOLVED_OVERWRITE:
				msg += 'There was an unresolved overwrite'
				msg += '\n\tFile "%s" provided by %s overwrites the following mods:\n\t\t' % (issue.description, issue.src_mod)
				msg += '\n\t\t'.join(issue.aux_mods)
				nl = 2 + len(issue.aux_mods)
			elif issue.issue_type == Issue.IssueType.UNKNOWN_MOD:
				msg += 'Cannot scan for issues when dealing with an unknown mod "%s"' % issue.src_mod
			iss = tk.Text(self.inf, bg=col_bg, height=nl)
			iss.insert(tk.INSERT, msg)
			iss.pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=1)
			self.w_issues.append(iss)

	def _handle_resize(self, evt):
		if evt.width != self.sizer.winfo_width():
			self.sizer.config(width=evt.width)

	def __init__(self, parent):
		super().__init__(parent, bg='white')
		self.pack(fill=tk.BOTH, expand=1)
		self.inf = self.display_widget(tk.Frame)
		self.inf.config(bg='white')
		self.sizer = tk.Frame(self.inf, height=1)
		self.sizer.pack()
		self.bind('<Configure>', self._handle_resize)
		
class RightPane(ttk.Notebook):
	def show_conflicts(self, conflicts):
		self.cf.show_conflicts(conflicts)
		
	def show_info(self, mod):
		self.mi.show_info(mod)
		
	def show_issues(self, issues):
		self.iss.show_issues(issues)

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
		
		self.mi = ModInfo(self)
		self.cf = Conflicts(self)
		self.iss = Issues(self)
		self.add(self.mi, text='Mod Info')
		self.add(self.cf, text='Conflicts')
		self.add(self.iss, text='Issues')
		
def show_gui():
	top = SMM()
	top.mainloop()
	
show_gui()