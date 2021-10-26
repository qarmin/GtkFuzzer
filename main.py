import gi
from inspect import getmembers, isfunction # Used to get list of all functions 
import inspect
import random # Shuffle

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

exceptions = ["modify_cursor", #Not reported because it is deprecated, but still may be reported later 
# May cause strange crashes, hard to reproduce
"unref",
"_unref",
"ref",
"_ref",
"destroy",


"check_resize", "bind_model", # TODO crashes.c PopupMenu?
"present", # TODO crashes.c Offscreen


"mark_busy", # GIT 3954

"get_object_type", # TODO  WidgetPath

# Python bugs?
"get_height", # TODO PrintContext - Can't create
"get_width", # TODO PrintContext - Can't create
"map", # TODO PlacesSidebar, can't find this
"serialize", # TODO NumerableIcon - Can't find function
"get_n_links", # TODO LabelAccessible - Accesible not available in GTK
"initialize", # TODO IconViewAccessible - Accesible not available in GTK
"get_app_info", # GtkAppChooserButton
"new", # TODO Button new, Box new Pygobject
"free", # Border free PyGobject
"_unref", # TODO CssProvider._unref
"get_bounding_box_center", # TODO GestureDrag.get_bounding_box_center
"init_template", # Gtk.FileChooserButton().init_template()
"start_editing", # Below ComboBox + FileChooserDialog
"popup_at_pointer", # Below Menu

# TODO - created test case, but not reported
"draw_page_finish", # TODO PrintOperation


# Waits for user input
"run",

# Freezes script
"show_now",
]

# TODO 
        # a1 = Gtk.ComboBox()
        # a1.start_editing()
        # a1.start_editing()
        # a2 = Gtk.FileChooserDialog()

        # q = Gtk.Menu()
        # q.unparent()
        # q.popup_at_pointer()

disallowed_classes = [
    "Box", # Not sure, need to be checked
    "CssProvider", #GIT 3957
    "ThemingEngine", # Returns null when not found
    "TextIter", # A lot of crashes and TextIter doesn't seems to be instantable

    "Window", "ToplevelAccessible" # Both classes together causes crashes, so this need to be tracked
]
def start_test(_unused):
    # print("SSSSSSSSSSSSTATATST")
    # for _i in range(10):
    #     q = Gtk.Menu()
    #     q.unparent()
    #     q.popup_at_pointer()

    # print("ENDDSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    # return  

    print("Looks that there is no crash")
    old_gtk_objects = dir(Gtk)
    gtk_objects = []

    for base_object in old_gtk_objects:
        type_of_thing = eval("type(Gtk." + base_object + ")")
        str_type_of_thing = str(type_of_thing)
        # print(type_of_thing)
        if str_type_of_thing.find("gi.types") == -1:
            continue
        if base_object in disallowed_classes:
            continue

        gtk_objects.append(base_object)


    gtk_objects = gtk_objects[0:2000]

    list_of_functions = []

    index = 0
    # This loop creates Gtk objects like Window or ScrolledWindow
    for base_object in gtk_objects:
        index += 1
        print(str(index) + " - testing " + str(base_object))

        ar = getattr(Gtk, base_object)
        try:
            obj = ar()
        except:
            print("Failed to create - " + str(base_object))
            continue

        functions_in_object = dir(obj)
        for _i in range(5): # 100 times because sometimes memory is corrupted, and crash doesn't always show
            random.shuffle(functions_in_object)
            for function in functions_in_object:
                # obj = ar() # This option create new object for each executed function
                if bool(random.getrandbits(1)) == True:
                    continue

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
                print("Trying to execute " + base_object + "." + function)
                function_handler = getattr(obj, function)
                try:
                    function_handler() # TODO Add support for parameters
                    print("KKKKKGtk." + base_object + "()." + function + "()")
                    list_of_functions.append("Gtk." + base_object + "()." + function + "()")
                except:
                    pass
                    # print("ERROR: Failed to execute function " + function)
    for i in list_of_functions:
        print(i)
    print("Ended test")
    #Gtk.main_quit() # Uncomment to fix crash

def end_test(_unused):
    Gtk.main_quit()


window = Gtk.Window(title="Close close to sta")
window.show()
window.connect("destroy", start_test)
window2 = Gtk.Window(title="End Everything")
window2.show()
window2.connect("destroy", end_test)
Gtk.main()
