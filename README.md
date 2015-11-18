# mcedit2-Filter-Wrapper-Plugin
Wrapper plugin for mcedit2 that allows MCEdit 1.0 filters to be ran

## Setup
1. Download mcedit2's soruce code from [here](https://github.com/mcedit/mcedit2)
2. Open the project up in your favorite IDE
3. Change line 50 in `src/mcedit2/editortools/__init__.py` from `)` to `) + tuple(_registered_tools)`
4. Create a directory in the `src/plugins` directory called `wrapper`
5. Download the code in this repository and put the `wrapper` directory
6. Create a directory named `filters` in the `wrapper` directory, or run MCEdit 2.0 once to create the directory
7. Put a MCEdit Legacy/1.0/Unified filter in the `filters` directory and run it from the "Legacy Filter Wrapper" tool in the Toolbar

_Note: The line number in step 3 may change, and this fix is only to be used until Tool plugins are fully supported_
