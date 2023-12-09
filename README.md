Python tools developed during a multiplayer "full py" modded playthrough.

These are intended as "good enough" scripts, not fully reliable and tested libraries. You may need to make local
modifications to get the behavior you want.

### Environment setup

The `factorio-draftsman` package will need to be configured to recognize the set of mods you are playing with.

Run `draftsman-update -p "/absolute/path/to/mods"` to accomplish this. If you are on Windows, use forward slashes in
path names rather than backslashes. Ex: `C:/Users/me/AppData/Roaming/Factorio/mods`.

If draftsman-update complains about a mod version issue it may be a mod you have installed depends on a version of
the base mod newer than what is bundled with the current draftsman release. To fix this you can download the contents
of the base mod matching the version you have installed at https://github.com/wube/factorio-data/tags and then
overwrite the contents of `venv/Lib/site-packages/draftsman/factorio-data` and then run draftsman-update again.  

#### IDE

This project was written in the PyCharm IDE.

If you are on Windows, I recommend making sure you install PyCharm as Administrator and add bin to your PATH
(one of the options during setup).

#### Dependencies

Install with `pip install <package>`

*   https://github.com/redruin1/factorio-draftsman - for python factorio blueprint manipulation
*   https://pypi.org/project/pyperclip/ - for API to copy/paste clipboard
*   (optional) https://pypi.org/project/pipreqs/ - For keeping requirements.txt up to date. 
