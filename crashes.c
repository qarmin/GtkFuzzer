#include <gtk/gtk.h>
int main (int argc, char **argv)
{
    printf("EXECUTED\n");
    gtk_init( & argc, & argv );

    for(int i = 0; i< 10; i++){
        GtkMenu *thing;
        thing = gtk_menu_new();
        gtk_widget_unparent(thing);
        gtk_menu_popup_at_pointer(thing,NULL);

    }
    // GtkOffscreenWindow *thing;
    // thing = gtk_offscreen_window_new();
    // gtk_window_present(thing);
    // gtk_window_present(thing);

	// GtkPopoverMenu *thing;
	// thing = gtk_popover_menu_new();
	// gtk_popover_bind_model(GTK_POPOVER(thing), NULL, NULL);
	// gtk_container_check_resize(thing);

    // GtkCssProvider *thing;
    // thing = gtk_css_provider_get_named (NULL,NULL);

    // GtkPrintOperation *thing;
    // thing = gtk_print_operation_new();
    // gtk_print_operation_draw_page_finish (thing);


    return 0;
}

