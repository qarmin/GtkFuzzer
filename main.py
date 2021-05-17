import gi
from inspect import getmembers, isfunction # Used to get list of all functions 

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

exceptions = ["modify_cursor"]

def start_test(_unused):
    aa = Gtk.Application()
    aa.mark_busy()
    return
    gtk_objects = dir(Gtk)

    index = 2000

    # This loop creates Gtk objects like Window or ScrolledWindow
    for base_object in gtk_objects:
        type_of_thing = eval("type(Gtk." + base_object + ")")
        str_type_of_thing = str(type_of_thing)
        # print(type_of_thing)
        if str_type_of_thing.find("gi.types") == -1:
            continue
        # print(str(type_of_thing) +  "    " + base_object)
        # print(i)
        # print(type_of_thing)
        # index -= 1
        # if index < 0:
        #     break
        # if index < 1500:
        #     continue


        ar = getattr(Gtk, base_object)
        try:
            obj = ar()
            try:
                for function in dir(obj):
                    obj = ar()
                    type_of_function = eval("type(Gtk." + base_object + "." + function  + ")") # We get info about this thing
                    if str(type_of_function).find("gi.FunctionInfo") == -1: # It is not GTK function
                        continue
                    if function in exceptions:
                        continue
                    # print(type_of_function)
                    # TODO Check if function cause bugs(excluded function)
                    # TODO Check if arguments are supported
                    try:
                        
                        print("Executing " + base_object + "." + function)
                        function_handler = getattr(obj, function)
                        function_handler() # TODO Add support for parameters

                    except:
                        print("Failed to execute function " + function) 
            except:
                print("HEHE")
        except:
            print("Failed to create - " + str(base_object))
            continue

    print("Ended test")
    Gtk.main_quit() # Uncomment to fix crash



window = Gtk.Window(title="Close close to sta")
window.show()
window.connect("destroy", start_test)
Gtk.main()
