from toontown.toonbase.ToontownModules import *
from .ToontownAIMsgTypes import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toon import DistributedToonAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import types

class DatabaseObject:
    """
    This class represents an object as retrieved directly from the
    database via special direct-to-database queries. It is used for in-game operations
    as well as offline database repair utilities.

    Attributes
    ----------
    air : object
        The AI repository.
    doId : int or None
        The unique ID of the distributed object.
    values : dict
        A dictionary to store the values retrieved from or to be written to the database.
    gotDataHandler : callable or None
        The handler function to be called when data is received from the database.
    doneEvent : str
        The event name used when a database operation is completed.
    """

    notify = directNotify.newCategory("DatabaseObject")
    notify.setInfo(0)

    def __init__(self, air, doId=None, doneEvent="DatabaseObject"):
        """
        Initializes a DatabaseObject instance.

        Parameters
        ----------
        air : object
            The AI repository object.
        doId : int, optional
            The unique ID of the distributed object.
        doneEvent : str, optional
            The event to be triggered when a database operation completes.
        """
        self.air = air
        self.doId = doId
        self.values = {}
        self.gotDataHandler = None
        self.doneEvent = doneEvent

    def readToon(self, fields=None):
        """
        Reads and returns a `DistributedToonAI` object from the database.

        Parameters
        ----------
        fields : list, optional
            A subset of fields to read, if provided.

        Returns
        -------
        DistributedToonAI
            An empty `DistributedToonAI` object that will be populated with data later.
        """
        toon = DistributedToonAI.DistributedToonAI(self.air)
        self.readObject(toon, fields)
        return toon

    if simbase.wantPets:
        def readPet(self):
            """
            Reads and returns a Pet object from the database.

            Returns
            -------
            DistributedPetAI
                An empty `DistributedPetAI` object that will be populated later.
            """
            from toontown.pets import DistributedPetAI
            pet = DistributedPetAI.DistributedPetAI(self.air)
            self.readObject(pet, None)
            return pet

        def readPetProxy(self):
            """
            Reads and returns a Pet Proxy object from the database.

            Returns
            -------
            DistributedPetProxyAI
                An empty `DistributedPetProxyAI` object that will be populated later.
            """
            from toontown.pets import DistributedPetProxyAI
            petProxy = DistributedPetProxyAI.DistributedPetProxyAI(self.air)
            self.readObject(petProxy, None)
            return petProxy

    def readObject(self, do, fields=None):
        """
        Reads a DistributedObject from the database and fills its data.

        Parameters
        ----------
        do : object
            The distributed object to be read.
        fields : list, optional
            A subset of fields to read, if provided.
        """
        self.do = do
        className = do.__class__.__name__
        self.dclass = self.air.dclassesByName[className]
        self.gotDataHandler = self.fillin

        if fields is not None:
            self.getFields(fields)
        else:
            self.getFields(self.getDatabaseFields(self.dclass))

    def storeObject(self, do, fields=None):
        """
        Stores data from the distributed object into the database.

        Parameters
        ----------
        do : object
            The distributed object whose data is being stored.
        fields : list, optional
            A subset of fields to update, if provided.
        """
        self.do = do
        className = do.__class__.__name__
        self.dclass = self.air.dclassesByName[className]

        if fields is not None:
            self.reload(self.do, self.dclass, fields)
        else:
            dbFields = self.getDatabaseFields(self.dclass)
            self.reload(self.do, self.dclass, dbFields)

        values = self.values
        if fields is not None:
            values = {}
            for field in fields:
                if field in self.values:
                    values[field] = self.values[field]
                else:
                    self.notify.warning(f"Field {field} not defined.")

        self.setFields(values)

    def getFields(self, fields):
        """
        Retrieves the specified fields from the database.

        Parameters
        ----------
        fields : list
            A list of field names to retrieve from the database.
        """
        context = self.air.dbObjContext
        self.air.dbObjContext += 1
        self.air.dbObjMap[context] = self

        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_GET_STORED_VALUES)
        dg.addUint32(context)
        dg.addUint32(self.doId)
        dg.addUint16(len(fields))
        for f in fields:
            dg.addString(f)

        self.air.send(dg)

    def getFieldsResponse(self, di):
        """
        Handles the response from the database after retrieving fields.

        Parameters
        ----------
        di : PyDatagramIterator
            The data iterator containing the response from the database.
        """
        objId = di.getUint32()
        if objId != self.doId:
            self.notify.warning(f"Unexpected doId {objId}")
            return

        count = di.getUint16()
        fields = [di.getString() for _ in range(count)]
        retCode = di.getUint8()

        if retCode != 0:
            self.notify.warning(f"Failed to retrieve data for object {self.doId}")
        else:
            values = [di.getString().encode('ISO-8859-1') for _ in range(count)]
            for i in range(count):
                found = di.getUint8()
                if not found:
                    self.notify.info(f"Field {fields[i]} is not found")
                    self.values.pop(fields[i], None)
                else:
                    self.values[fields[i]] = PyDatagram(values[i])

            self.notify.info(f"Got data for {self.doId}")

            if self.gotDataHandler:
                self.gotDataHandler(self.do, self.dclass)
                self.gotDataHandler = None

        if self.doneEvent:
            messenger.send(self.doneEvent, [self, retCode])

    def setFields(self, values):
        """
        Sets the specified fields in the database.

        Parameters
        ----------
        values : dict
            A dictionary of field names and their values to be set in the database.
        """
        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_SET_STORED_VALUES)
        dg.addUint32(self.doId)
        dg.addUint16(len(values))

        items = list(values.items())
        for field, value in items:
            dg.addString(field)
        for field, value in items:
            dg.addString(value.getMessage())

        self.air.send(dg)

    def getDatabaseFields(self, dclass):
        """
        Retrieves the list of fields associated with the specified DCClass that should be stored in the database.

        Parameters
        ----------
        dclass : DCClass
            The DCClass whose fields are to be retrieved.

        Returns
        -------
        list
            A list of field names that are to be stored in the database.
        """
        fields = []
        for i in range(dclass.getNumInheritedFields()):
            dcf = dclass.getInheritedField(i)
            af = dcf.asAtomicField()
            if af and af.isDb():
                fields.append(af.getName())
        return fields

    def fillin(self, do, dclass):
        """
        Fills in the data from the `DatabaseObject` into the specified distributed object.

        Parameters
        ----------
        do : DistributedObjectAI
            The distributed object to fill in the data.
        dclass : DCClass
            The DCClass of the distributed object.
        """
        do.doId = self.doId
        for field, value in self.values.items():
            if field == "setZonesVisited" and value.getLength() == 1:
                self.notify.warning("Ignoring broken setZonesVisited")
            else:
                dclass.directUpdate(do, field, value)

    def reload(self, do, dclass, fields):
        """
        Reloads the data from the distributed object and stores it in the values table.

        Parameters
        ----------
        do : DistributedObjectAI
            The distributed object whose data is being reloaded.
        dclass : DCClass
            The DCClass of the distributed object.
        fields : list
            A list of field names to reload.
        """
        self.doId = do.doId
        self.values = {}
        for fieldName in fields:
            field = dclass.getFieldByName(fieldName)
            if field is None:
                self.notify.warning(f"No definition for {fieldName}")
            else:
                dg = PyDatagram()
                packOk = dclass.packRequiredField(dg, do, field)
                assert(packOk)
                self.values[fieldName] = dg

    def createObject(self, objectType):
        """
        Creates a new object in the database.

        Parameters
        ----------
        objectType : int
            The type of object to create, specified as an integer.

        Notes
        -----
        Values to initialize the new object can be provided in the `values` dictionary.
        """
        values = {}

        for key, value in values.items():
            values[key] = PyDatagram(str(value))

        assert isinstance(objectType, int)

        context = self.air.dbObjContext
        self.air.dbObjContext += 1
        self.air.dbObjMap[context] = self

        self.createObjType = objectType

        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_CREATE_STORED_OBJECT)

        dg.addUint32(context)
        dg.addString('')
        dg.addUint16(objectType)
        dg.addUint16(len(values))

        for field in values.keys():
            dg.addString(field)
        for value in values.values():
            dg.addString(value.getMessage())

        self.air.send(dg)

    def handleCreateObjectResponse(self, di):
        """
        Handles the response from the database after creating an object.

        Parameters
        ----------
        di : PyDatagramIterator
            The data iterator containing the response from the database.
        """
        retCode = di.getUint8()
        if retCode != 0:
            self.notify.warning(f"Database object {self.createObjType} create failed")
        else:
            del self.createObjType
            self.doId = di.getUint32()

        if self.doneEvent:
            messenger.send(self.doneEvent, [self, retCode])

    def deleteObject(self):
        """
        Deletes the object from the database.
        """
        self.notify.warning(f'Deleting object {self.doId}')

        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_DELETE_STORED_OBJECT)

        dg.addUint32(self.doId)
        dg.addUint32(0xdeadbeef)

        self.air.send(dg)
