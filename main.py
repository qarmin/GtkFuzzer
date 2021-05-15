import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def start_test(_unused):
    gtk_objects = dir(Gtk)

    # This loop creates Gtk objects like Window or ScrolledWindow
    for i in gtk_objects:
        type_of_thing = eval("type(Gtk." + i + ")")
        if type_of_thing is gi.types:
            pass
        else:
            # print(str(type_of_thing) +  "    " + i)
            pass

        if i.startswith("_"):
            print("Ignoring " + i + ", builtin function")
            continue
        if i[0].islower():
            print("Ignoring " + i + " normal function")
            continue

        ar = getattr(Gtk, i)
        try:
            obj = ar()
            try:
                obj.show()
                print("Created and showed object - " + i)
            except:
                print("Created object but failed to show it - " + i)
                continue
        except:
            print("Failed to create - " + str(i))
            continue

    print("Ended test")
    # Gtk.main_quit() # Uncomment to fix crash


window = Gtk.Window(title="Close close to sta")
window.show()
window.connect("destroy", start_test)
Gtk.main()
