import gi
from inspect import getmembers, isfunction # Used to get list of all functions 

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, GLib

exceptions = ["modify_cursor", #Not reported because it is deprecated, but still may be reported later 
# May cause strange crashes, hard to reproduce
"unref",
"_unref",
"ref",
"_ref",

"mark_busy", # GIT 3954
"get_app_info", # GtkAppChooserButton
"new", # TODO Button new, Box new Pygobject
"free", # Border free PyGobject
"_unref", # TODO CssProvider._unref
"get_bounding_box_center", # TODO GestureDrag.get_bounding_box_center
"initialize", # TODO IconViewAccessible
"get_n_links", # TODO LabelAccessible
"serialize", # TODO NumerableIcon
"map", # TODO PlacesSidebar
"get_height", # TODO PrintContext
"get_width", # TODO PrintContext
"draw_page_finish", # TODO PrintOperation
"backward_char", # TODO TextIter
"backward_cursor_position", # TODO TextIter
"backward_line", # TODO TextIter
"backward_sentence_start", # TODO TextIter
"backward_to_tag_toggle", # TODO TextIter
"backward_visible_cursor_position", # TODO TextIter
"backward_visible_line", # TODO TextIter
"backward_visible_word_start", # TODO TextIter
"backward_word_start", # TODO TextIter
"begins_tag", # TODO TextIter
"ends_line", # TODO TextIter
"get_path", # TODO ThemingEngine
"get_object_type", # TODO  WidgetPath
"get_request_mode", # TODO BinLayout
"next", #TODO BitsetIter
"previous", #TODO BitsetIter
"notify", #TODO DropTarget 
"override_property", #TODO DropTarget
"get_formats", #TODO DropTarget
"insert_prefix", #TODO EntryCompletion
"thaw_notify", #TODO PasswordEntryBuffer
"get_capabilities", #TODO Printer
"get_default_page_size", #TODO Printer
"get_hard_margins", #TODO Printer
"list_papers", #TODO Printer
"request_details", #TODO Printer
"gl_shader_pop_texture", #TODO Snapshot
"pop", #TODO Snapshot
"restore", #TODO Snapshot
"save", #TODO  Snapshot
"to_node", #TODO  Snapshot
"to_paintable", #TODO  Snapshot
"transform", #TODO  Snapshot
"get_border", #TODO StyleContext
"get_color", #TODO StyleContext
"get_margin", #TODO StyleContext
"get_padding", #TODO StyleContext
"get_state", #TODO StyleContext
"ends_sentence", #TODO TextIter
"ends_tag", #TODO TextIter
"ends_word", #TODO 
"forward_char", #TODO 
"forward_cursor_position", #TODO 
"forward_line", #TODO 
"forward_sentence_end", #TODO 
"forward_to_end", #TODO 
"forward_to_line_end", #TODO 
"forward_to_tag_toggle", #TODO 
"forward_visible_cursor_position", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 
"", #TODO 

# Waits for user input
"run",

# Freezes script
"show_now",
]

disallowed_classes = [
    # Instancing
    "ActivateAction",
    "MnemonicAction",
    "NamedAction",
    "NeverTrigger",
    "NothingAction",
    "NothingAction",
    "PrintJob",
    "SignalAction",
    # Showing
    "DragIcon",
    "EmojiChooser",
    "Popover",
    "PopoverMenu",
    # Other
    "FileChooserDialog", # Shows error too many open files
    "FileChooserWidget", # Shows error too many open files
    "FileChooserNative", # Slow
    "FontChooserWidget", # Slow
    "TextIter", # Too much crashes
    "",
    "",
    "",
]

def print_custom(what,level):
    for i in range(level):
        what = "  " + what
    print(what)    


class fuzzer:
    def __init__(self):
        print("Initializing")
        GLib.timeout_add(50, self.starting)

        self.all_classes = []

        gtk_objects = dir(Gtk)
        # Collect all classes 
        for base_object in gtk_objects:
            type_of_thing = eval("type(Gtk." + base_object + ")")
            str_type_of_thing = str(type_of_thing)
            # print(type_of_thing)
            if str_type_of_thing.find("gi.types") == -1:
                continue
            if base_object in disallowed_classes:
                continue
            self.all_classes.append(base_object)    

        # TODO save to list all available methods
        self.tested_index = 419 # 0 is start index and can be changed to any value
        self.number_of_all_classes = len(self.all_classes)

    def print_hi(self):
        print("Hi")
        return True

    def starting(self):

        self.tested_class = self.all_classes[self.tested_index]
        
        print_custom(str(self.tested_index) + " - testing " + str(self.tested_class),0)

        ar = getattr(Gtk, self.tested_class)
        for _z in range(1):
            try:
                print_custom("Trying to create_instance of - " + str(self.tested_class),1)
                obj = ar()
                
                print_custom("Trying to show object",1)
                try:
                    obj.show()
                except:
                    print_custom("ERROR: Failed to show object",1)
                
                try:
                    for function in dir(obj):
                        for _i in range(3): # may be executed several times, because sometimes memory is corrupted, and crash doesn't always happens
                            obj = ar()
                            type_of_function = eval("type(Gtk." + self.tested_class + "." + function  + ")") # We get info about this thing
                            
                            if str(type_of_function).find("gi.FunctionInfo") == -1: # It is not GTK function
                                continue
                            if function in exceptions:
                                continue      
                            if function.startswith("_"): # Private stuff, TODO check this one by one
                                continue
                            # This functions freezes entire script
                            if function.find("wait_") != -1:
                                continue
                            
                            # print(type_of_function)
                            # TODO Check if arguments are supported
                            print_custom("Executing " + self.tested_class + "." + function,3)
                            try:
                                function_handler = getattr(obj, function)
                                function_handler() # TODO Add support for parameters
                            except:
                                print_custom("ERROR: Failed to execute function " + function,3)

                except:
                    print_custom("ERROR: Internal error(not sure what exactly worked bad)",2)
            except:
                print_custom("ERROR: Failed to create instance of - " + str(self.tested_class),1)

        self.tested_index += 1
        self.tested_index = self.tested_index % self.number_of_all_classes
        return True # Needs to run in loop things
    #Gtk.main_quit() 

def start_test(app):
    fuzz = fuzzer()
    window = Gtk.ApplicationWindow(application=app)
    window.show()
    print(type(Gtk.Window.show))

app = Gtk.Application(application_id='pl.pl.pl')
app.connect('activate', start_test)
app.run(None)
 
