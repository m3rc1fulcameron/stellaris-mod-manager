The purpose of this project is to provide a tool which allows users to diagnose file conflicts between mods in Stellaris.
It works by maintaining a database of which mods are known to be compatible with each other and what order they should be loaded in.
Mods which violate the prescribed load order or overwrite common files without being marked as compatible generate an issue in
the issues pane.

This is very much in the proof of concept phase, and several improvements are needed:

0. Rewrite from scratch when not sleep-deprived so as to have a sane codebase.
1. Automatically generate an optimal load order and apply that load order based off of the rules database.
2. Provide a tool for diffing conflicting files and quickly creating patches which merge changes.
3. Provide an API for people to implement automatic merge strategies.
3. Move re-architect the tool using a sane GUI library like QT instead of tkinter.
4. Provide the ability to import and export load orders to facilitate the easy distribution of mod packs.
5. (Don't know if this is possible) Hook the Steam Workshop to pull mod dependencies automatically and provide the ability to automatically download mods in an imported modpack.
6. Support multiple modding profiles to facilitate the concurrent installation of multiple modpacks.