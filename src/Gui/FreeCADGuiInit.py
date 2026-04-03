# ***************************************************************************
# *   Copyright (c) 2002,2003 Jürgen Riegel <juergen.riegel@web.de>         *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/
from dataclasses import dataclass

# FreeCAD gui init module
#
# Gathering all the information to start FreeCAD
# This is the second one of three init scripts, the third one
# runs when the gui is up

# imports the one and only
import FreeCAD, FreeCADGui
from enum import IntEnum, Enum

# shortcuts
Gui = FreeCADGui


# --- BEGIN external workbench icon central patch ---
def _fc_external_workbench_icon(fallback_path):
    try:
        _os = __import__("os")
        _fc = __import__("FreeCAD")

        path = ""
        enabled = False
        prefer_external = True

        try:
            group = _fc.ParamGet("User parameter:BaseApp/Preferences/Bitmaps/ExternalTheme")
            enabled = group.GetBool("Enabled", False)
            prefer_external = group.GetBool("PreferExternal", True)
            path = group.GetString("Path", "")
        except Exception:
            pass

        env_enabled = _os.environ.get("FREECAD_EXTERNAL_ICON_THEME_ENABLED")
        if env_enabled is not None:
            enabled = env_enabled.strip().lower() not in ("0", "false", "no", "off")

        env_prefer = _os.environ.get("FREECAD_EXTERNAL_ICON_THEME_PREFER_EXTERNAL")
        if env_prefer is not None:
            prefer_external = env_prefer.strip().lower() not in ("0", "false", "no", "off")

        env_path = _os.environ.get("FREECAD_EXTERNAL_ICON_THEME")
        if env_path:
            path = env_path
            enabled = True

        if enabled and prefer_external and path and fallback_path:
            fallback_str = str(fallback_path)
            base = _os.path.splitext(_os.path.basename(fallback_str))[0]
            candidates = []
            for ext in (".svg", ".png", ".xpm"):
                candidates.append(_os.path.join(path, base + ext))
                candidates.append(_os.path.join(path, "icons", base + ext))

            for candidate in candidates:
                if _os.path.isfile(candidate):
                    return candidate

            for root, _dirs, files in _os.walk(path):
                for ext in (".svg", ".png", ".xpm"):
                    name = base + ext
                    if name in files:
                        return _os.path.join(root, name)
    except Exception:
        pass

    return fallback_path


def _fc_patch_workbench_icon_object(workbench_obj):
    try:
        if hasattr(workbench_obj, "Icon") and workbench_obj.Icon:
            resolved = _fc_external_workbench_icon(workbench_obj.Icon)
            try:
                workbench_obj.__dict__["Icon"] = resolved
            except Exception:
                try:
                    setattr(workbench_obj, "Icon", resolved)
                except Exception:
                    pass
    except Exception:
        pass
    return workbench_obj


def _fc_install_add_workbench_icon_wrapper(gui_module):
    try:
        current = getattr(gui_module, "addWorkbench", None)
        if current is None:
            return
        if getattr(current, "__name__", "") == "_fc_add_workbench_with_external_icon":
            return

        original_add_workbench = current

        def _fc_add_workbench_with_external_icon(*args, **kwargs):
            if args:
                patched_first = _fc_patch_workbench_icon_object(args[0])
                if len(args) == 1:
                    args = (patched_first,)
                else:
                    args = (patched_first,) + tuple(args[1:])
            return original_add_workbench(*args, **kwargs)

        try:
            _fc_add_workbench_with_external_icon.__name__ = "_fc_add_workbench_with_external_icon"
        except Exception:
            pass
        gui_module.addWorkbench = _fc_add_workbench_with_external_icon
    except Exception:
        pass
# --- END external workbench icon central patch ---

# this is to keep old code working
Gui.listCommands = Gui.Command.listAll
Gui.isCommandActive = lambda cmd: Gui.Command.get(cmd).isActive()


# The values must match with that of the C++ enum class ResolveMode
class ResolveMode(IntEnum):
    NoResolve = 0
    OldStyleElement = 1
    NewStyleElement = 2
    FollowLink = 3


Gui.Selection.ResolveMode = ResolveMode


# The values must match with that of the C++ enum class SelectionStyle
class SelectionStyle(IntEnum):
    NormalSelection = 0
    GreedySelection = 1


# The values must match with that of the Python enum class in ViewProvider.pyi
class ToggleVisibilityMode(Enum):
    CanToggleVisibility = "CanToggleVisibility"
    NoToggleVisibility = "NoToggleVisibility"


Gui.Selection.SelectionStyle = SelectionStyle


# Important definitions
class Workbench:
    """The workbench base class."""

    MenuText = ""
    ToolTip = ""
    Icon = None

    def Initialize(self):
        """Initializes this workbench."""
        App.Console.PrintWarning(
            str(self) + ": Workbench.Initialize() not implemented in subclass!"
        )

    def ContextMenu(self, recipient):
        pass

    def appendToolbar(self, name, cmds):
        self.__Workbench__.appendToolbar(name, cmds)

    def removeToolbar(self, name):
        self.__Workbench__.removeToolbar(name)

    def listToolbars(self):
        return self.__Workbench__.listToolbars()

    def getToolbarItems(self):
        return self.__Workbench__.getToolbarItems()

    def appendCommandbar(self, name, cmds):
        self.__Workbench__.appendCommandbar(name, cmds)

    def removeCommandbar(self, name):
        self.__Workbench__.removeCommandbar(name)

    def listCommandbars(self):
        return self.__Workbench__.listCommandbars()

    def appendMenu(self, name, cmds):
        self.__Workbench__.appendMenu(name, cmds)

    def removeMenu(self, name):
        self.__Workbench__.removeMenu(name)

    def listMenus(self):
        return self.__Workbench__.listMenus()

    def appendContextMenu(self, name, cmds):
        self.__Workbench__.appendContextMenu(name, cmds)

    def removeContextMenu(self, name):
        self.__Workbench__.removeContextMenu(name)

    def reloadActive(self):
        self.__Workbench__.reloadActive()

    def name(self):
        return self.__Workbench__.name()

    def GetClassName(self):
        """Return the name of the associated C++ class."""
        # as default use this to simplify writing workbenches in Python
        return "Gui::PythonWorkbench"


class StandardWorkbench(Workbench):
    """A workbench defines the tool bars, command bars, menus,
    context menu and dockable windows of the main window.
    """

    def Initialize(self):
        """Initialize this workbench."""
        # load the module
        Log("Init: Loading FreeCAD GUI\n")

    def GetClassName(self):
        """Return the name of the associated C++ class."""
        return "Gui::StdWorkbench"


class NoneWorkbench(Workbench):
    """An empty workbench."""

    MenuText = "<none>"
    ToolTip = "The default empty workbench"

    def Initialize(self):
        """Initialize this workbench."""
        # load the module
        Log("Init: Loading FreeCAD GUI\n")

    def GetClassName(self):
        """Return the name of the associated C++ class."""
        return "Gui::NoneWorkbench"


@dataclass
class InputHint:
    """
    Represents a single input hint (shortcut suggestion).

    The message is a Qt formatting string with placeholders like %1, %2, ...
    The placeholders are replaced with input representations - be it keys, mouse buttons etc.
    Each placeholder corresponds to one input sequence. Sequence can either be:
     - one input from Gui.UserInput enum
     - tuple of mentioned enum values representing the input sequence

    >>> InputHint("%1 change mode", Gui.UserInput.KeyM)
    will result in a hint displaying `[M] change mode`

    >>> InputHint("%1 new line", (Gui.UserInput.KeyControl, Gui.UserInput.KeyEnter))
    will result in a hint displaying `[ctrl][enter] new line`

    >>> InputHint("%1/%2 increase/decrease ...", Gui.UserInput.KeyU, Gui.UserInput.KeyJ)
    will result in a hint displaying `[U]/[J] increase / decrease ...`
    """

    InputSequence = Gui.UserInput | tuple[Gui.UserInput, ...]

    message: str
    sequences: list[InputSequence]

    def __init__(self, message: str, *sequences: InputSequence):
        self.message = message
        self.sequences = list(sequences)


class HintManager:
    """
    A convenience class for managing input hints (shortcut suggestions) displayed to the user.
    It is here mostly to provide well-defined and easy to reach API from python without developers needing
    to call low-level functions on the main window directly.
    """

    def show(self, *hints: InputHint):
        """
        Displays the specified input hints to the user.

        :param hints: List of hints to show.
        """
        Gui.getMainWindow().showHint(*hints)

    def hide(self):
        """
        Hides all currently displayed input hints.
        """
        Gui.getMainWindow().hideHint()


Gui.InputHint = InputHint
Gui.HintManager = HintManager()


def InitApplications():
    import sys, os, traceback
    import io as cStringIO

    # Searching modules dirs +++++++++++++++++++++++++++++++++++++++++++++++++++
    # (additional module paths are already cached)
    ModDirs = FreeCAD.__ModDirs__
    # print ModDirs
    Log("Init:   Searching modules\n")

    def RunInitGuiPy(Dir) -> bool:
        InstallFile = os.path.join(Dir, "InitGui.py")
        if os.path.exists(InstallFile):
            try:
                with open(InstallFile, "rt", encoding="utf-8") as f:
                    exec(compile(f.read(), InstallFile, "exec"))
            except Exception as inst:
                Log("Init:      Initializing " + Dir + "... failed\n")
                Log("-" * 100 + "\n")
                Log(traceback.format_exc())
                Log("-" * 100 + "\n")
                Err(
                    'During initialization the error "'
                    + str(inst)
                    + '" occurred in '
                    + InstallFile
                    + "\n"
                )
                Err("Look into the log file for further information\n")
                mod_name = os.path.normpath(Dir).split(os.path.sep)[-1].lower()
                if hasattr(FreeCAD, "__failed_mods__"):
                    FreeCAD.__failed_mods__.append(mod_name)
                else:
                    FreeCAD.__failed_mods__ = [mod_name]
                if mod_name not in FreeCAD.__fallback_mods__:
                    Err("Could not evaluate module '" + mod_name + "' for fallbacks\n")
                elif len(FreeCAD.__fallback_mods__[mod_name]) > 1:
                    new_path = os.path.normpath(FreeCAD.__fallback_mods__[mod_name][-2])
                    Err(f"A fallback module was found for module '{mod_name}': {new_path}\n")
                    Err(f"Rename or remove {os.path.normpath(Dir)} to use the fallback module\n")
            else:
                Log("Init:      Initializing " + Dir + "... done\n")
                return True
        else:
            Log("Init:      Initializing " + Dir + "(InitGui.py not found)... ignore\n")
        return False

    def processMetadataFile(Dir, MetadataFile):
        meta = FreeCAD.Metadata(MetadataFile)
        if not meta.supportsCurrentFreeCAD():
            return None
        content = meta.Content
        if "workbench" in content:
            FreeCAD.Gui.addIconPath(Dir)
            workbenches = content["workbench"]
            for workbench_metadata in workbenches:
                if not workbench_metadata.supportsCurrentFreeCAD():
                    return None
                subdirectory = (
                    workbench_metadata.Name
                    if not workbench_metadata.Subdirectory
                    else workbench_metadata.Subdirectory
                )
                subdirectory = subdirectory.replace("/", os.path.sep)
                subdirectory = os.path.join(Dir, subdirectory)
                ran_init = RunInitGuiPy(subdirectory)

                if ran_init:
                    # Try to generate a new icon from the metadata-specified information
                    classname = workbench_metadata.Classname
                    if classname:
                        try:
                            wb_handle = FreeCAD.Gui.getWorkbench(classname)
                        except Exception:
                            Log(
                                f"Failed to get handle to {classname} -- no icon\
                                can be generated,\n check classname in package.xml\n"
                            )
                        else:
                            GeneratePackageIcon(dir, subdirectory, workbench_metadata, wb_handle)

    def tryProcessMetadataFile(Dir, MetadataFile):
        try:
            processMetadataFile(Dir, MetadataFile)
        except Exception as exc:
            Err(str(exc))

    def checkIfAddonIsDisabled(Dir):
        DisabledAddons = FreeCAD.ConfigGet("DisabledAddons").split(";")
        Name = os.path.basename(Dir)

        if Name in DisabledAddons:
            Msg(
                f'NOTICE: Addon "{Name}" disabled by presence of "--disable-addon {Name}" argument\n'
            )
            return True

        stopFileName = "ALL_ADDONS_DISABLED"
        stopFile = os.path.join(Dir, os.path.pardir, stopFileName)
        if os.path.exists(stopFile):
            Msg(f'NOTICE: Addon "{Dir}" disabled by presence of {stopFileName} stopfile\n')
            return True

        stopFileName = "ADDON_DISABLED"
        stopFile = os.path.join(Dir, stopFileName)
        if os.path.exists(stopFile):
            Msg(f'NOTICE: Addon "{Dir}" disabled by presence of {stopFileName} stopfile\n')
            return True

        return False

    for Dir in ModDirs:
        if Dir not in ["", "CVS", "__init__.py"]:
            if checkIfAddonIsDisabled(Dir):
                continue
            MetadataFile = os.path.join(Dir, "package.xml")
            if os.path.exists(MetadataFile):
                tryProcessMetadataFile(Dir, MetadataFile)
            else:
                RunInitGuiPy(Dir)
    Log("All modules with GUIs using InitGui.py are now initialized\n")

    try:
        import pkgutil
        import importlib
        import freecad

        freecad.gui = FreeCADGui
        for _, freecad_module_name, freecad_module_ispkg in pkgutil.iter_modules(
            freecad.__path__, "freecad."
        ):
            # Check for a stopfile
            stopFile = os.path.join(
                FreeCAD.getUserAppDataDir(), "Mod", freecad_module_name[8:], "ADDON_DISABLED"
            )
            if os.path.exists(stopFile):
                continue

            # Make sure that package.xml (if present) does not exclude this version of FreeCAD
            MetadataFile = os.path.join(
                FreeCAD.getUserAppDataDir(), "Mod", freecad_module_name[8:], "package.xml"
            )
            if os.path.exists(MetadataFile):
                meta = FreeCAD.Metadata(MetadataFile)
                if not meta.supportsCurrentFreeCAD():
                    continue

            if freecad_module_ispkg:
                Log("Init: Initializing " + freecad_module_name + "\n")
                try:
                    freecad_module = importlib.import_module(freecad_module_name)
                    if any(
                        module_name == "init_gui"
                        for _, module_name, ispkg in pkgutil.iter_modules(freecad_module.__path__)
                    ):
                        importlib.import_module(freecad_module_name + ".init_gui")
                        Log("Init: Initializing " + freecad_module_name + "... done\n")
                    else:
                        Log(
                            "Init: No init_gui module found in "
                            + freecad_module_name
                            + ", skipping\n"
                        )
                except Exception as inst:
                    Err(
                        'During initialization the error "'
                        + str(inst)
                        + '" occurred in '
                        + freecad_module_name
                        + "\n"
                    )
                    Err("-" * 80 + "\n")
                    Err(traceback.format_exc())
                    Err("-" * 80 + "\n")
                    Log("Init:      Initializing " + freecad_module_name + "... failed\n")
                    Log("-" * 80 + "\n")
                    Log(traceback.format_exc())
                    Log("-" * 80 + "\n")
    except ImportError as inst:
        Err('During initialization the error "' + str(inst) + '" occurred\n')

    Log("All modules with GUIs initialized using pkgutil are now initialized\n")


def GeneratePackageIcon(
    dir: str, subdirectory: str, workbench_metadata: FreeCAD.Metadata, wb_handle: Workbench
) -> None:
    relative_filename = workbench_metadata.Icon
    if not relative_filename:
        # Although a required element, this content item does not have an icon. Just bail out
        return
    absolute_filename = os.path.join(subdirectory, relative_filename)
    if hasattr(wb_handle, "Icon") and wb_handle.Icon:
        Log(
            f"Init:      Packaged workbench {workbench_metadata.Name} specified icon\
            in class {workbench_metadata.Classname}"
        )
        Log(f" ... replacing with icon from package.xml data.\n")
    wb_handle.__dict__["Icon"] = absolute_filename


Log("Init: Running FreeCADGuiInit.py start script...\n")


# init the gui

# signal that the gui is up
App.GuiUp = 1
App.Gui = FreeCADGui
FreeCADGui.Workbench = Workbench

_fc_install_add_workbench_icon_wrapper(Gui)

Gui.addWorkbench(_fc_patch_workbench_icon_object(NoneWorkbench()))
# init modules
InitApplications()

# set standard workbench (needed as fallback)
Gui.activateWorkbench("NoneWorkbench")

# Register .py, .FCScript and .FCMacro
FreeCAD.addImportType("Inventor V2.1 (*.iv *.IV)", "FreeCADGui")
FreeCAD.addImportType(
    "VRML V2.0 (*.wrl *.WRL *.vrml *.VRML *.wrz *.WRZ *.wrl.gz *.WRL.GZ)", "FreeCADGui"
)
FreeCAD.addImportType("Python (*.py *.FCMacro *.FCScript *.fcmacro *.fcscript)", "FreeCADGui")
FreeCAD.addExportType("Inventor V2.1 (*.iv)", "FreeCADGui")
FreeCAD.addExportType("VRML V2.0 (*.wrl *.vrml *.wrz *.wrl.gz)", "FreeCADGui")
FreeCAD.addExportType("X3D Extensible 3D (*.x3d *.x3dz)", "FreeCADGui")
FreeCAD.addExportType("WebGL/X3D (*.xhtml)", "FreeCADGui")
# FreeCAD.addExportType("IDTF (for 3D PDF) (*.idtf)","FreeCADGui")
# FreeCAD.addExportType("3D View (*.svg)","FreeCADGui")
FreeCAD.addExportType("Portable Document Format (*.pdf)", "FreeCADGui")

del InitApplications
del NoneWorkbench
del StandardWorkbench

Log("Init: Running FreeCADGuiInit.py start script... done\n")
