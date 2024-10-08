"""AccountServerConstants.py: contains the AccountServerConstants class """

from otp.otpbase.OTPModules import *
from .RemoteValueSet import *
from direct.directnotify import DirectNotifyGlobal
from . import TTAccount
from . import HTTPUtil

class AccountServerConstants(RemoteValueSet):
    notify = \
           DirectNotifyGlobal.directNotify.newCategory("AccountServerConstants")

    def __init__(self, cr):
        """ might throw a TTAccountException """
        self.expectedConstants = [
            b'minNameLength',
            b'minPwLength',
            b'allowNewAccounts',
            b'freeTrialPeriodInDays',
            b'priceFirstMonth',
            b'pricePerMonth',
            b'customerServicePhoneNumber',
            b'creditCardUpFront',
            ]
        # if in dev env with no account server, constants will be set to
        # an arbitrary string. If a constant needs to be something more
        # specific, set it here
        # rurbino the minPw and minName used to be zero, that sounds bad and upped it to 1
        self.defaults = {
            b'minNameLength': '1',
            b'minPwLength': '1',
            b'allowNewAccounts': '1',
            b'creditCardUpFront': '0',
            b'priceFirstMonth': '9.95',
            b'pricePerMonth': '9.95',
            }

        # do not query server for AccountConstants (US is no - will query)
        noquery = 1
#
# rest deprecated because all production functionality should have moved to website
# (only used for customer service number for the US)

        if cr.productName == 'DisneyOnline-US':
            if ConfigVariableBool('tt-specific-login',0).getValue():
                # the new website does not have constants.php, don't try to query it
                pass
            else:
                noquery = 0

        if (cr.accountOldAuth or
            ConfigVariableBool('default-server-constants', noquery).getValue()):
            self.notify.debug('setting defaults, not using account server constants')

            # fake it; create and populate a 'dict' object
            self.dict = {}

            # user is running in dev env, with no account server
            # set some defaults
            for constantName in self.expectedConstants:
                self.dict[constantName] = 'DEFAULT'
            # some constants need to be something more specific
            self.dict.update(self.defaults)
            return

        url = URLSpec(AccountServerConstants.getServer())
        url.setPath('/constants.php')
        self.notify.debug('grabbing account server constants from %s' %
                          url.cStr())

        RemoteValueSet.__init__(self, url, cr.http,
                                expectedHeader=b'ACCOUNT SERVER CONSTANTS\n',
                                expectedFields=self.expectedConstants,)

    # override the accessors so we can warn about undeclared constants
    def getBool(self, name):
        return self.__getConstant(name, RemoteValueSet.getBool)

    def getInt(self, name):
        return self.__getConstant(name, RemoteValueSet.getInt)

    def getFloat(self, name):
        return self.__getConstant(name, RemoteValueSet.getFloat)

    def getString(self, name):
        return self.__getConstant(name, RemoteValueSet.getString)

    def __getConstant(self, constantName, accessor):
        if not constantName in self.expectedConstants:
            self.notify.warning(
                "requested constant '%s' not in expected constant list; "
                "if it's a new constant, add it to the list" %
                constantName)
        return accessor(self, constantName)

    # this is used by the tcr in error msgs
    @staticmethod
    def getServer():
        return TTAccount.getAccountServer().cStr()
    @staticmethod
    def getServerURL():
        return TTAccount.getAccountServer()
