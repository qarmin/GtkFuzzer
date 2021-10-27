import gi
from inspect import getmembers, isfunction # Used to get list of all functions 

import random

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, GLib



# setting
setting_save_to_file = True
setting_always_new_object = False
setting_mix_functions = True
setting_miss_some_functions = True

results_file_handler = open("results.txt", "w")

exceptions = ["modify_cursor", #Not reported because it is deprecated, but still may be reported later 
# May cause strange crashes, hard to reproduce
"unref",
"_unref",
"ref",
"_ref",

"mark_busy", # GIT 3954
"new", # TODO Button new, Box new Pygobject
"free", # Border free PyGobject
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
"set_text", #TODO PasswordEntryBuffer
"get_height", #TODO PrintContext
"get_width", #TODO PrintContext
"draw_page_finish", #TODO PrintOperation
"get_request_mode", #TODO BinLayout
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
    "ScrolledWindow", # Strange crash
    "",
    "",
]

def print_custom(what,level):
    for i in range(level):
        what = "  " + what
    print(what)    

def save_to_file(what):
    results_file_handler.write(what + "\n")
    results_file_handler.flush()

class fuzzer:
    def __init__(self):
        print("Initializing")
        GLib.timeout_add(50, self.starting)

        self.current_number = 0 # Number which shows how many classes/objects were tested
        self.all_classes_dict = {}
        self.all_classes_arr = []

        gtk_objects = dir(Gtk)
        # Collect all classes 
        for base_object_name in gtk_objects:
            type_of_thing = eval("type(Gtk." + base_object_name + ")")
            str_type_of_thing = str(type_of_thing)
            # print(type_of_thing)
            if str_type_of_thing.find("gi.types") == -1:
                continue
            if base_object_name in disallowed_classes:
                continue
                
            # Checks if class is instantable, if not, not check it
            ar = getattr(Gtk, base_object_name)
            try:
                test_obj = ar()
            except:
                continue
            try:
                True
                #test_obj.free()
            except:
                continue
            
            self.all_classes_arr.append(base_object_name)
        
        ##### Here can be split     
        self.all_classes_arr = self.all_classes_arr[0:]
        
        for base_object_name in self.all_classes_arr:
            array_of_functions = []
            
            ar = getattr(Gtk, base_object_name)
            test_obj = ar()
                
            # Finds all available methods of this class
            for function in dir(test_obj):
                type_of_function = ""
                # Looks that parent_class may fail
                type_of_function = eval("type(Gtk." + base_object_name + "." + function  + ")") # We get info about this thing
                        
                if str(type_of_function).find("gi.FunctionInfo") == -1: # It is not GTK function
                    continue
                if function in exceptions:
                    continue      
                if function.startswith("_"): # Private stuff, not really usable since probably this is also Python internals
                    continue
                if function.find("wait_") != -1: # This functions freezes entire script
                    continue
                
                array_of_functions.append(function)
            
            self.all_classes_dict[base_object_name] = array_of_functions 
            

        # TODO save to list all available methods
        self.tested_index = 0 # 0 is start index and can be changed to any value
        self.number_of_all_classes = len(self.all_classes_arr)
        print("Found " + str(self.number_of_all_classes) + " classes to check")
        
    def get_variable_name(self):
        return "variable" + str(self.current_number)
        
    def starting(self):

        self.tested_class = self.all_classes_arr[self.tested_index]
        
        print_custom(str(self.tested_index) + " - testing " + str(self.tested_class),0)
        save_to_file("############# " + str(self.tested_class) + " #############")

        ar = getattr(Gtk, self.tested_class)
        for _z in range(1):
                self.current_number += 1
                print_custom("Trying to create_instance of - " + str(self.tested_class),1)
                save_to_file(self.get_variable_name() + " = "+ self.tested_class + "()")
                obj = ar()
                
                #print_custom("Trying to show object",1)
                # TODO check if this is needed(this function may be executed later, but not sure if it is possible to take parent methods)
                #try:
                #    obj.show()
                #except:
                #    print_custom("ERROR: Failed to show object",1)
                
                for _i in range(1): # may be executed several times, because sometimes memory is corrupted, and crash doesn't always happens
                    test_functions = self.all_classes_dict[self.tested_class]
                    random.shuffle(test_functions)
                    
                    for function in test_functions:
                        if setting_miss_some_functions:
                            if random.choice([True, False]):
                                continue
                            
                        if setting_always_new_object:
                            print("Freeing and creating "+ self.tested_class)
                            #obj.unref()
                            obj = ar()
                        
                        print_custom("Trying to execute:  " + function,3)
                        # TODO Check if arguments are supported
                        try:
                            function_handler = getattr(obj, function)
                            function_handler() # TODO Add support for parameters
                        except:
                            print_custom("ERROR: Failed to execute function " + function,3)
                
                print("Freeing object")
                #obj.unref()

        self.tested_index += 1
        self.tested_index = self.tested_index % self.number_of_all_classes
        return True # Needs to run in loop things
    #Gtk.main_quit() 

def start_test(app):
    fuzz = fuzzer()
    window = Gtk.ApplicationWindow(application=app)
    window.show()
    roman = Gtk.Window()
    print(type(Gtk.Window.show))

app = Gtk.Application(application_id='pl.pl.pl')
app.connect('activate', start_test)
app.run(None)
 
