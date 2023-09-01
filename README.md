Python tools developed during a multiplayer "full py" modded playthrough.

These are intended as "good enough" scripts, not fully reliable and tested libraries. You may need to make local
modifications to get the behavior you want.

### Environment setup

The `factorio-draftsman` package will need to be configured to recognize the set of mods you are playing with.

Run `draftsman-update -p "/absolute/path/to/mods"` to accomplish this. If you are on Windows, use forward slashes in
path names rather than backslashes. Ex: `C:/Users/me/AppData/Roaming/Factorio/mods`.

#### IDE

This project was written in the PyCharm IDE.

#### Dependencies

Install with `pip install <package>`

*   https://github.com/redruin1/factorio-draftsman - for python factorio blueprint manipulation
*   https://pypi.org/project/pyperclip/ - for API to copy/paste clipboard