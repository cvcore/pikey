import pytermgui as ptg

"""
Keyboard Forwarder
----------------------
Devices:
Nixie's Tastatur [ON ]
Unknown Mouse    [OFF]
----------------------
[Devices] [KEYMAP] [EXIT]

Keyboard Remap
----------------------
Press key: [ ]
Map to:    [ ]
[OK] [CANCEL]

Devices
----------------------
Paired Devices <-
Connect New
[BACK]

PAIR
----------------------
Available Devices:
... <-
...
[CANCEL]

PAIR-2
----------------------
Enter Pair code on Dev:
284817
[CANCEL]

"""

PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_DARK = "#4D4940"
PALETTE_DARKER = "#242321"

def _create_aliases() -> None:
    """Creates all the TIM aliases used by the application.
    Aliases should generally follow the following format:
        namespace.item
    For example, the title color of an app named "myapp" could be something like:
        myapp.title
    """

    ptg.tim.alias("app.text", "#cfc7b0")

    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")

    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "#cfc7b0")

    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")

def _configure_widgets() -> None:
    """Defines all the global widget configurations.
    Some example lines you could use here:
        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    # ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    # ptg.boxes.ROUNDED.set_chars_of(ptg.Container)

    # ptg.Slider.styles.filled__cursor = PALETTE_MID
    # ptg.Slider.styles.filled_selected = PALETTE_LIGHT

    # ptg.Label.styles.value = "app.text"

    # ptg.Window.styles.border__corner = "#C2B280"
    # ptg.Container.styles.border__corner = PALETTE_DARK

    ptg.Splitter.set_char("separator", "")

    ptg.Button.styles.label = "200 bold"
    ptg.Button.styles.highlight = "210 bold"


def keyboard_remap():
    pass

def show_devices():
    pass

def pair_devices():
    pass

def prompt_passcode():
    pass

def show_main_menu(manager: ptg.WindowManager):

    header = ptg.Window(
        "[app.header] Keyboard Remapper ",
        box="EMPTY",
        is_persistant=True
    )
    # header.styles.fill = "app.header.fill"

    manager.add(
        header,
        assign="header"
    )

    footer = ptg.Window(
        ptg.Splitter(
            ptg.Button("DEV", parent_align=0),
            ptg.Button("MAP", parent_align=0),
            ptg.Button("BYE", parent_align=0),
        ),
        box="EMPTY",
    )
    # footer.styles.fill = "app.footer"

    manager.add(
        footer,
        assign="footer"
    )

    manager.add(
        ptg.Window(
            "",
            ptg.Splitter(
                ptg.Label("Nixi...", parent_align=0),
                ptg.Button("ON ", parent_align=0)
            ),
            ptg.Splitter(
                ptg.Label("cw-mouse", parent_align=0),
                ptg.Button("OFF", parent_align=0)
            ),
            "",
            vertical_align=ptg.VerticalAlignment.TOP,
            # width=37,
            # height=12
        )
        .center()
        .set_title("Devices"),
        assign="body"
    )

def _define_layout() -> ptg.Layout:
    """Defines the application layout.
    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=1)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body")

    # A slot in the same row as body, using the full non-occupied height and
    # 20% of the terminal's height.

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=1)

    return layout

def main():
    _create_aliases()
    _configure_widgets()

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()
        show_main_menu(manager)

if __name__ == "__main__":
    main()
