class BanquetTableBase:
    """
    A base class that holds methods and constants shared between the client
    and AI versions of the banquet table logic. This class manages diner states
    and other relevant properties.

    Attributes
    ----------
    HUNGRY : int
        The state of a diner who is hungry.
    DEAD : int
        The state of a diner who has died.
    EATING : int
        The state of a diner who is eating.
    ANGRY : int
        The state of a diner who has become angry from not being fed.
    HIDDEN : int
        The state of a diner who is hidden from view in the scene.
    INACTIVE : int
        The state of a diner who is waiting for the next battle phase.
    """

    # States of the diners
    HUNGRY = 1
    DEAD = 0
    EATING = 2  # Distance between each food node
    ANGRY = 3  # Not fed for a while, resets to 0 after being fed
    HIDDEN = 4  # Not shown in the scene
    INACTIVE = 5  # Sitting in a chair, waiting for the next battle phase
