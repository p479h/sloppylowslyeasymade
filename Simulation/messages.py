
"""
     This file contains all the messages that are used on the 
     help buttons in the simulator"""
m1=\
     """
    If you do not provide a name to this page, it will be
    assumed that you have created the main page
    """ #Used because pages will be organized by name.



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Used in Page1:

m2 = \
   """
    If ticked, the current time of the simulation
    will be displayed in the bottom left corner of
    the screen.
    Current time represents time since Initial t.
    """

m3 = \
   """
    If ticked, your representation of the universe
    will contain stars whose location will be ran-
    domly assigned.
    """

m4 = \
   """
    This option speaks for itself.
    Using two dimensions will lead to more efficient
    animation. But it looks less cool.
    """

m5 = \
   """
    Just the initial time from which the plot
    will count from. It does not affect the physics
    of the app.
    """

m6 = \
   """
    This is the interval between calculations of
    interactions between planets. You can change
    this option later, but this variable is THE
    most important determinant of how precise the
    simulation will be.
    """

m7 = \
   """
    This is the limit of the visible part of the
    simulated universe. It is the limit of the axis
    of the graph where you will watch the simulation.
    """

m8 = \
   """
    This is the name that can be placed on top of
    the simulation in case you want to take a pic
    of it with some message.
    """

m9 = \
   """
    Graphs make use of Blit to get smoother
    frame transition during animation.
    for 3D graphs this comes at the cost of
    being unnable to rotate the plot.
    """
page1messages = [m2, m3, m4, m5, m6, m7, m8, m9]


m10 = \
    """
    This affects the function to set all planets
    in orbit. Moons will orbit the closest Planets,
    which will orbit the closes Sun.
    Other won't orbit anything.
    (Only valid if you make the program set an obit)
    """

m11 = \
    """
    The color of the object in the graph.

    """

m12 = \
    """
    The shape of the object in the plot.
    You can make custom markers using the
    notation $<Desired marker>$.
    Example: $?$ to get ?.
    """

m13 = \
    """
    If you tick this tick while making a
    planet, this planet will get a ring of
    random color.
    In 3D, this will severely affect performance.
    """

m15 = \
    """
    The charge density or the total charge of the
    object if it has any. Planets don't usually
    have charge, but imagination is the limit.
    Right? I want to provide you with the ability
    to get electromagnetism involved if wanted.
    """

m16 = \
    """
    Initial of the object as a vector.
    If you leave this blank, it will be
    assumed that your object starts with
    0 velocity in all components.
    """

m17 = \
    """
    Initial position as a vector.
    If you leave this blank, it will be
    asumed that your object starts at
    the origin of the figure's coordinate
    system.
    """

m18 = \
    """
    You can choose to either provide the mass
    or the density of the object. In either
    case the object is assumed to be spherical.
    """


m19 = \
    """
    If you got this far you can figure this one out.
    """

m20 = \
    """
    This is a unitless measure of the size of the
    object in the simulation. Play with it to get
    a better feeling.
    """

page1_1messages = [m10, m11, m12, m13, m15, m16, m17, m18, m19, m20]


mdt = \
    """
    This is the interval, in seconds, between force
    calculations. Changing this will immediately
    have an effect on the simulation.
    """

m_cycles = \
    """
    This is the number of dt intervals that are used
    when calculating the path of the planets. Which,
    in turn, is calculated and displayed after pressing
    the button with the image of a clock.
    """
