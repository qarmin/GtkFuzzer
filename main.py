import gi
from inspect import getmembers, isfunction # Used to get list of all functions 

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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

# Waits for user input
"run",

# Freezes script
"show_now",
]
disallowed_classes = [
    "Box", # Not sure, need to be checked
    "CssProvider", #GIT 3957
    "TextIter", # A lot of crashes

    "Window", "ToplevelAccessible" # Both classes together causes crashes, so this need to be tracked
]
def start_test(_unused):
    for _i in range(1000):
        # aa = Gtk.WidgetPath()
        # bb = Gtk.Window()
        # aa = Gtk.GestureDrag()
        # aa.get_bounding_box_center()
        pass    

    print("Looks that there is no crash")
    gtk_objects = dir(Gtk)

    index = 0

    # This loop creates Gtk objects like Window or ScrolledWindow
    for base_object in gtk_objects:
        index += 1
        type_of_thing = eval("type(Gtk." + base_object + ")")
        str_type_of_thing = str(type_of_thing)
        # print(type_of_thing)
        if str_type_of_thing.find("gi.types") == -1:
            continue
        if base_object in disallowed_classes:
            continue
        
        # if not((index > 1116 and index < 1118) or (index > 1116 and index < 1118)):
        #     continue
        if index < 500 or index > 12000:
            continue
        print(str(index) + " - testing " + str(base_object))

        ar = getattr(Gtk, base_object)
        try:
            obj = ar()
            try:
                for function in dir(obj):
                    for _i in range(1): # 100 times because sometimes memory is corrupted, and crash doesn't always show
                        obj = ar()
                        
                        type_of_function = eval("type(Gtk." + base_object + "." + function  + ")") # We get info about this thing
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
                        # TODO Check if function cause bugs(excluded function)
                        # TODO Check if arguments are supported
                        print("Executing " + base_object + "." + function)
                        try:
                            function_handler = getattr(obj, function)
                            function_handler() # TODO Add support for parameters
                        except:
                            print("ERROR: Failed to execute function " + function)
            except:
                print("ERROR: Did")
        except:
            print("Failed to create - " + str(base_object))
            continue

    print("Ended test")
    Gtk.main_quit() # Uncomment to fix crash



window = Gtk.Window(title="Close close to sta")
window.show()
window.connect("destroy", start_test)
Gtk.main()
