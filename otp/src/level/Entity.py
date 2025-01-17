"""
Entity.py: contains the Entity class, which serves as the base class for all objects
that exist within a level and can be edited with the LevelEditor. Entities are responsible
for handling their attributes, managing their lifecycle, and interacting with the level
they belong to. The class also supports attribute setting, entity destruction, and
level-related actions.

Main Components:
- Entity class: The main class representing an object in the level.
- Functions: Includes initialization, destruction, and utility methods for entities.
"""

from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import lineInfo
import string
from direct.directnotify import DirectNotifyGlobal


class Entity(DirectObject):
    """
    Entity is the base class for all objects that exist in a Level
    and can be edited with the LevelEditor. It handles initializing and managing
    its attributes, interactions with the level, and supports destruction and
    attribute-setting operations.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('Entity')

    def __init__(self, level=None, entId=None):
        """
        Initializes the Entity class. Optionally takes a level and entId.

        Args:
            level: The level to which the entity belongs.
            entId: A unique identifier for the entity within its level.
        """
        self.initializeEntity(level, entId)

    def initializeEntity(self, level, entId):
        """
        Sets the entity's attributes, such as level and entId, and ensures the entity
        is properly initialized in the level. This is typically called after the
        entity is generated to assign it its attributes.

        Args:
            level: The level to which the entity belongs.
            entId: A unique identifier for the entity within its level.
        """
        self.level = level
        self.entId = entId
        if (self.level is not None) and (self.entId is not None):
            self.level.initializeEntity(self)

    def __str__(self):
        """
        Returns a string representation of the entity. If the entity has a level,
        it returns a formatted string containing the entity's type and ID. Otherwise,
        it returns the entity's class name or name attribute if present.

        Returns:
            A string representation of the entity.
        """
        if hasattr(self, 'level') and self.level:
            return 'ent%s(%s)' % (self.entId, self.level.getEntityType(self.entId))
        elif hasattr(self, 'name'):
            return self.name
        elif hasattr(self, 'entId'):
            return '%s-%s' % (self.__class__.__name__, self.entId)
        else:
            return self.__class__.__name__

    def destroy(self):
        """
        Destroys the entity. This is called when the level no longer needs the entity.
        After this is called, the entity should be considered defunct. Distributed
        entities may still exist after destruction, but they are no longer valid
        entities.
        """
        Entity.notify.debug('Entity.destroy() %s' % self.entId)
        if self.level:
            if self.level.isInitialized():
                self.level.onEntityDestroy(self.entId)
            else:
                Entity.notify.warning('Entity %s destroyed after level??' % self.entId)
        self.ignoreAll()
        del self.level
        del self.entId

    def getUniqueName(self, name, entId=None):
        """
        Returns a unique name for the entity, based on its name, level ID, and entId.

        Args:
            name: The base name to use in the unique name.
            entId: Optional. The entity ID to include in the unique name.

        Returns:
            A string that uniquely identifies the entity.
        """
        if entId is None:
            entId = self.entId
        return '%s-%s-%s' % (name, self.level.levelId, entId)

    def getParentToken(self):
        """
        Returns a token that uniquely identifies this entity for the purpose
        of distributed parenting.

        Returns:
            A unique identifier for this entity used for distributed parenting.
        """
        return self.level.getParentTokenForEntity(self.entId)

    def getOutputEventName(self, entId=None):
        """
        Returns the event name generated by an entity, based on the entity's ID.

        Args:
            entId: Optional. The entity ID to use for generating the event name.

        Returns:
            A string representing the event name generated by the entity.
        """
        if entId is None:
            entId = self.entId
        return self.getUniqueName('entityOutput', entId)

    def getZoneEntId(self):
        """
        Returns the entId of the zone that contains this entity.

        Returns:
            The entId of the zone containing the entity.
        """
        return self.level.getEntityZoneEntId(self.entId)

    def getZoneEntity(self):
        """
        Returns the zone entity for the zone that contains this entity.

        Returns:
            The zone entity for the zone containing this entity.
        """
        return self.level.getEntity(self.getZoneEntId())

    def getZoneNode(self):
        """
        Returns the zone node for the zone that contains this entity.

        Returns:
            The zone node containing this entity.
        """
        return self.getZoneEntity().getNodePath()

    def privGetSetter(self, attrib):
        """
        Retrieves the setter function for a given attribute if it exists.

        Args:
            attrib: The attribute for which the setter is retrieved.

        Returns:
            The setter function if available, otherwise None.
        """
        setFuncName = 'set%s%s' % (string.upper(attrib[0]), attrib[1:])
        if hasattr(self, setFuncName):
            return getattr(self, setFuncName)
        return None

    def callSetters(self, *attribs):
        """
        Calls setters for the provided attributes if they exist on the entity.

        Args:
            attribs: List of attributes to call setters for.
        """
        self.privCallSetters(0, *attribs)

    def callSettersAndDelete(self, *attribs):
        """
        Calls setters for the provided attributes and deletes the attributes from the entity.

        Args:
            attribs: List of attributes to call setters for and delete.
        """
        self.privCallSetters(1, *attribs)

    def privCallSetters(self, doDelete, *attribs):
        """
        Common implementation of callSetters and callSettersAndDelete.

        Args:
            doDelete: Whether to delete the attributes after calling their setters.
            attribs: List of attributes to process.
        """
        for attrib in attribs:
            if hasattr(self, attrib):
                setter = self.privGetSetter(attrib)
                if setter is not None:
                    value = getattr(self, attrib)
                    if doDelete:
                        delattr(self, attrib)
                    setter(value)

    def setAttribInit(self, attrib, value):
        """
        Initializes an attribute on the entity.

        Args:
            attrib: The attribute to initialize.
            value: The value to set for the attribute.
        """
        self.__dict__[attrib] = value

    if __debug__:
        def debugPrint(self, message):
            """
            Prints a debug message for the entity.

            Args:
                message: The message to print.
            """
            return self.notify.debug(
                str(self.__dict__.get('entId', '?')) + ' ' + message)

    if __dev__:
        # Support for level editing
        def handleAttribChange(self, attrib, value):
            """
            Handles changes to entity attributes during level editing.

            Args:
                attrib: The attribute that was changed.
                value: The new value for the attribute.
            """
            setter = self.privGetSetter(attrib)
            if setter is not None:
                setter(value)
            else:
                self.__dict__[attrib] = value
                self.attribChanged(attrib, value)

        def attribChanged(self, attrib, value):
            """
            Called when an attribute is changed directly, without calling a setter.
            Override this method in derived classes to handle attribute changes.

            Args:
                attrib: The attribute that was changed.
                value: The new value for the attribute.
            """
            pass
