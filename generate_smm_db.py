import json

db = {
	"Unofficial Machine & Synthetic Empire DLC": {
		"name": "Unofficial Machine & Synthetic Empire DLC",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"EHOF - SpeedDial - UI Dynamic Patch": {
		"name": "EHOF - SpeedDial - UI Dynamic Patch",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Unofficial Hive DLC: Forgotten Queens": {
		"name": "Unofficial Hive DLC: Forgotten Queens",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"UI Overhaul Dynamic": {
		"name": "UI Overhaul Dynamic",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Tiny Outliner v2": {
		"name": "Tiny Outliner v2",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"UI Overhaul Dynamic + Tiny Outliner v2": {
		"name": "UI Overhaul Dynamic + Tiny Outliner v2",
		"after": [
			"Tiny Outliner v2"
		],
		"before": [],
		"patches": [
			"Tiny Outliner v2"
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Stellaris List EXtender - SLEX": {
		"name": "Stellaris List EXtender - SLEX",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Propaganda and Espionage": {
		"name": "Propaganda and Espionage",
		"after": [],
		"before": [
			"UI Overhaul Dynamic"
		],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"UI Overhaul - Prop&Esp Patch": {
		"name": "UI Overhaul - Prop&Esp Patch",
		"after": [
			"Propaganda and Espionage",
			"UI Overhaul Dynamic"
		],
		"before": [],
		"patches": [
			"Propaganda and Espionage",
			"UI Overhaul Dynamic"
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Kurogane Expand 2.7.1": {
		"name": "Kurogane Expand 2.7.1",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Gigastructural Engineering & More (2.7)": {
		"name": "Gigastructural Engineering & More (2.7)",
		"after": [
			"UI Overhaul Dynamic",
		],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Event Horizon Offset Facility": {
		"name": "Event Horizon Offset Facility",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"EHOF/Giga Compatibility Patch": {
		"name": "EHOF/Giga Compatibility Patch",
		"after": [
			"Event Horizon Offset Facility",
		],
		"before": [],
		"patches": [
			"Event Horizon Offset Facility",
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Balanced Space Warfare": {
		"name": "Balanced Space Warfare",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Balanced Space Warfare // More Ship Sections": {
		"name": "Balanced Space Warfare // More Ship Sections",
		"after": [
			"Balanced Space Warfare"
		],
		"before": [],
		"patches": [
			"Balanced Space Warfare"
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"A Deadly Tempest (2.7)": {
		"name": "A Deadly Tempest (2.7)",
		"after": [
			"~~Ariphaos Unofficial Patch (2.7)"
		],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"~~Ariphaos Unofficial Patch (2.7)": {
		"name": "~~Ariphaos Unofficial Patch (2.7)",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": True
	},
	"~ StarNet AI": {
		"name": "~ StarNet AI",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!!!Universal Resource Patch [2.4+]": {
		"name": "!!!Universal Resource Patch [2.4+]",
		"after": [
			"Gigastructural Engineering & More (2.7)",
			"Unofficial Hive DLC: Forgotten Queens",
			"Event Horizon Offset Facility",
		],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!!!!Machine DLC & Hive DLC Patch": {
		"name": "!!!!Machine DLC & Hive DLC Patch",
		"after": [
			"Unofficial Hive DLC: Forgotten Queens"
		],
		"before": [],
		"patches": [
			"Unofficial Hive DLC: Forgotten Queens"
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!! 00 Infinite Stellaris Framework": {
		"name": "!! 00 Infinite Stellaris Framework",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!! 00 Performance": {
		"name": "!! 00 Performance",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!! 00 Performance Plus": {
		"name": "!! 00 Performance Plus",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!! 00 Starnet Performance": {
		"name": "!! 00 Starnet Performance",
		"after": [
			"~ StarNet AI",
			"!! 00 Performance",
			"!! 00 Performance Plus",
		],
		"before": [],
		"patches": [
			"~ StarNet AI",
			"!! 00 Performance",
			"!! 00 Performance Plus",
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"!! 00 Performance Universial Compatibility": {
		"name": "!! 00 Performance Universial Compatibility",
		"after": [
			"Gigastructural Engineering & More (2.7)",
			"Unofficial Hive DLC: Forgotten Queens",
			"Extra Ship Components 3.0 [2.7+]",
		],
		"before": [],
		"patches": [
			"Gigastructural Engineering & More (2.7)",
			"Unofficial Hive DLC: Forgotten Queens",
			"Extra Ship Components 3.0 [2.7+]",
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Extra Ship Components 3.0 [2.7+]": {
		"name": "Extra Ship Components 3.0 [2.7+]",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Extra Ship Components 3.0 - Overwrites [2.7+]": {
		"name": "Extra Ship Components 3.0 - Overwrites [2.7+]",
		"after": [
			"Extra Ship Components 3.0 [2.7+]"
		],
		"before": [],
		"patches": [
			"Extra Ship Components 3.0 [2.7+]"
		],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Sensor Expansion": {
		"name": "Sensor Expansion",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
	"Bypass Adjustments": {
		"name": "Bypass Adjustments",
		"after": [],
		"before": [],
		"patches": [],
		"conflicts": [],
		"resolves": [],
		"allow_overwrite": False
	},
}
	
if __name__ == '__main__':
	with open('smm_db.json', 'w+') as fp:
		fp.write(json.dumps(db))