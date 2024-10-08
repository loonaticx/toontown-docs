"""
EditorGlobals module: contains global editor data used for assigning
unique entity IDs (entIds) for game levels and ensuring proper user setup
before editing. This module helps manage level editing processes by
validating the user and ensuring the correct configuration of
editor-related data.

Main Components:
- EditTargetPostName: A constant used to store the name of the current
  level being edited.
- username2entIdBase: A dictionary mapping usernames to a base entity ID
  range, ensuring unique entIds for each user.
- Functions: Various utility functions to validate user readiness and
  provide their specific entId allocation range.
"""

from direct.showbase.PythonUtil import uniqueElements

# The posting name under which levels being edited should be registered
EditTargetPostName = 'inGameEditTarget'

# The range of entIds that can be assigned per user
EntIdRange = 10000

# A mapping of usernames to their base entId allocation.
# Once a range has been assigned to a user, please don't change it.
username2entIdBase = {
    'darren': 1 * EntIdRange,
    'samir': 2 * EntIdRange,
    'skyler': 3 * EntIdRange,
    'joe': 4 * EntIdRange,
    'DrEvil': 5 * EntIdRange,
    'asad': 6 * EntIdRange,
    'drose': 7 * EntIdRange,
    'pappy': 8 * EntIdRange,
    'patricia': 9 * EntIdRange,
    'jloehrle': 10 * EntIdRange,
    'rurbino': 11 * EntIdRange,
}

# Ensure that all assigned entId bases are unique
assert uniqueElements(username2entIdBase.values())

# Configuration variable for storing the editor's username
usernameConfigVar = 'level-edit-username'

# The value assigned if the username is not set
undefinedUsername = 'UNDEFINED_USERNAME'

# Fetch the configured username from the environment (or assign 'undefined')
editUsername = config.GetString(usernameConfigVar, undefinedUsername)


def checkNotReadyToEdit():
    """
    Verifies if the system is properly configured for level editing.

    Returns:
        A string describing the error if not ready; None if ready.
    """
    if editUsername == undefinedUsername:
        return "you must config '%s'; see %s.py" % (
            usernameConfigVar, __name__)

    if editUsername not in username2entIdBase:
        return "unknown editor username '%s'; see %s.py" % (
            editUsername, __name__)

    return None


def assertReadyToEdit():
    """
    Ensures the system is ready for editing, otherwise raises an assertion.
    """
    msg = checkNotReadyToEdit()
    if msg is not None:
        assert False, msg


def getEditUsername():
    """
    Returns the current editor's username.
    """
    return editUsername


def getEntIdAllocRange():
    """
    Returns the valid range of entIds for the current user.

    The function computes the range based on the base entId for the
    editor's username.

    Returns:
        A list [min, max+1] representing the entId range for the user.
        The returned values are compatible with range() and xrange()
        functions.
    """
    baseId = username2entIdBase[editUsername]
    return [baseId, baseId + EntIdRange]
