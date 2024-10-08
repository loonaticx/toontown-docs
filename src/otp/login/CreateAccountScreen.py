"""CreateAccountScreen module: contains the CreateAccountScreen class"""

from otp.otpbase.OTPModules import *
from direct.gui.DirectGui import *
from direct.fsm import StateData
from otp.otpgui import OTPDialog
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from . import TTAccount
from . import GuiScreen
from otp.otpbase import OTPGlobals
from direct.distributed.MsgTypes import *

class CreateAccountScreen(StateData.StateData, GuiScreen.GuiScreen):
    """
    contains methods for displaying the account creation screen
    """
    # special methods

    # Create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CreateAccountScreen")

    ActiveEntryColor = Vec4(1,1,1,1)
    InactiveEntryColor = Vec4(0.8,0.8,0.8,1)

    labelFg = (1,1,1,1)
    labelFgActive = (1,1,0,1)

    def __init__(self, cr, doneEvent):
        """
        Set up the account creation screen interface
        """
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        assert cr.serverVersion
        self.cr = cr
        self.loginInterface = self.cr.loginInterface

        self.fsm = ClassicFSM.ClassicFSM('CreateAccountScreen',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['create',
                                         ]),
                            State.State('create',
                                        self.enterCreate,
                                        self.exitCreate,
                                        ['waitForLoginResponse',
                                         'create',
                                         ]),
                            State.State('waitForLoginResponse',
                                        self.enterWaitForLoginResponse,
                                        self.exitWaitForLoginResponse,
                                        ['create',
                                         ]),
                            ],
                           'off',
                           'off',
                           )
        self.fsm.enterInitialState()

    def load(self):
        self.notify.debug('load')
        masterScale = 0.8

        textScale = 0.1*masterScale
        entryScale = 0.08*masterScale
        lineHeight = 0.21*masterScale

        buttonScale = 1.3*masterScale
        buttonLineHeight = 0.16*masterScale

        # account creation screen
        self.frame = DirectFrame(
            parent = aspect2d,
            relief = None,
            )
        self.frame.hide()

        linePos=0.5
        linePos-=lineHeight

        self.nameLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.21, 0, linePos),
            text = OTPLocalizer.CreateAccountScreenUserName,
            text_scale = textScale,
            text_align = TextNode.ARight,
            text_fg = self.labelFg,
            text_shadow = (0,0,0,1),
            text_shadowOffset = (0.08, 0.08),
            )
        self.nameEntry = DirectEntry(
            parent = self.frame,
            relief = DGG.SUNKEN,
            borderWidth = (0.1,0.1),
            scale = entryScale,
            pos = (-0.125, 0.0, linePos),
            width = OTPGlobals.maxLoginWidth,
            numLines = 1,
            focus = 0,
            cursorKeys = 1,
            )
        self.nameEntry.label = self.nameLabel
        linePos-=lineHeight

        self.passwordLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.21, 0, linePos),
            text = OTPLocalizer.CreateAccountScreenPassword,
            text_scale = textScale,
            text_align = TextNode.ARight,
            text_fg = self.labelFg,
            text_shadow = (0,0,0,1),
            text_shadowOffset = (0.08, 0.08),
            )
        self.passwordEntry = DirectEntry(
            parent = self.frame,
            relief = DGG.SUNKEN,
            borderWidth = (0.1,0.1),
            scale = entryScale,
            pos = (-0.125, 0.0, linePos),
            width = OTPGlobals.maxLoginWidth,
            numLines = 1,
            focus = 0,
            cursorKeys = 1,
            obscured = 1,
            )
        self.passwordEntry.label = self.passwordLabel
        linePos-=lineHeight

        self.passwordConfirmLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.21, 0, linePos),
            text = OTPLocalizer.CreateAccountScreenConfirmPassword,
            text_scale = textScale,
            text_align = TextNode.ARight,
            text_fg = self.labelFg,
            text_shadow = (0,0,0,1),
            text_shadowOffset = (0.08, 0.08),
            )
        self.passwordConfirmEntry = DirectEntry(
            parent = self.frame,
            relief = DGG.SUNKEN,
            borderWidth = (0.1,0.1),
            scale = entryScale,
            pos = (-0.125, 0.0, linePos),
            width = OTPGlobals.maxLoginWidth,
            numLines = 1,
            focus = 0,
            cursorKeys = 1,
            obscured = 1,
            )
        self.passwordConfirmEntry.label = self.passwordConfirmLabel
        linePos-=lineHeight

        linePos-=lineHeight

        self.submitButton = DirectButton(
            parent = self.frame,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = buttonScale,
            text = OTPLocalizer.CreateAccountScreenSubmit,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.__handleSubmit,
            )
        linePos-=buttonLineHeight

        self.cancelButton = DirectButton(
            parent = self.frame,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = buttonScale,
            text = OTPLocalizer.CreateAccountScreenCancel,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.__handleCancel,
            )
        linePos-=buttonLineHeight

        self.dialogDoneEvent = "createAccountDialogAck"
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.dialog = dialogClass(
            dialogName = 'createAccountDialog',
            doneEvent = self.dialogDoneEvent,
            message = "",
            style = OTPDialog.Acknowledge,
            # make sure this dialog shows up over other things
            sortOrder = DGG.NO_FADE_SORT_INDEX + 100,
            )
        self.dialog.hide()

    def unload(self):
        self.notify.debug('unload')
        self.dialog.cleanup()
        del self.dialog
        self.frame.destroy()
        del self.fsm
        del self.loginInterface
        del self.cr

    def enter(self):
        self.__firstTime = 1
        self.frame.show()
        self.fsm.request("create")

    def exit(self):
        self.ignore(self.dialogDoneEvent)
        self.fsm.requestFinalState()
        self.frame.hide()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterCreate(self):
        # always clear out the password fields
        self.password = ""
        self.passwordEntry.set("")
        self.passwordConfirmEntry.set("")

        # if this is the first time we're entering the account creation
        # screen, clear out the rest of the fields
        if self.__firstTime:
            self.userName = ""
            self.nameEntry.set(self.userName)

        self.__firstTime = 0

        self.focusList = [
            self.nameEntry,
            self.passwordEntry,
            self.passwordConfirmEntry,
            ]
        # override the Enter-press behavior for the last focus item,
        # to remove the input focus; otherwise, the focus would
        # momentarily be advanced to the first entry
        self.startFocusMgmt(overrides = {},
                            globalFocusHandler=self.__handleFocusChange,
                            )

    def exitCreate(self):
        self.stopFocusMgmt()

    # event handlers

    # this is called whenever the input focus changes
    def __handleFocusChange(self, focusItem):
        # 'focusItem' is None or is the item that just gained the input focus
        # highlight the label for this item (non-DirectEntry widgets
        # have no way to show input focus, so this will do)
        for item in self.focusList:
            item.label.component('text0').setFg(self.labelFg)
        if focusItem is not None:
            focusItem.label.component('text0').setFg(self.labelFgActive)

    def __handleSubmit(self):
        # make sure no entries have focus
        self.removeFocus()

        # If they typed the password in correctly, let them attempt to
        # create the account
        self.userName = self.nameEntry.get()
        self.password = self.passwordEntry.get()
        passwordConfirm = self.passwordConfirmEntry.get()

        minNameLength = self.cr.accountServerConstants.getInt('minNameLength')
        minPwdLength = self.cr.accountServerConstants.getInt('minPwLength')

        if (self.userName == ''):
            self.dialog.setMessage(OTPLocalizer.CreateAccountScreenNoAccountName)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleUsernameAck)
        elif (len(self.userName) < minNameLength):
            self.dialog.setMessage(
                OTPLocalizer.CreateAccountScreenAccountNameTooShort %
                (minNameLength))
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleUsernameAck)
        elif (len(self.password) < minPwdLength):
            self.dialog.setMessage(
                OTPLocalizer.CreateAccountScreenPasswordTooShort %
                (minPwdLength))
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
        elif self.password != passwordConfirm:
            self.dialog.setMessage(OTPLocalizer.CreateAccountScreenPasswordMismatch)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handlePasswordAck)
        else:
            self.fsm.request("waitForLoginResponse")

    def __handleCancel(self):
        messenger.send(self.doneEvent, [{'mode': 'cancel'}])

    def __handleUsernameAck(self):
        self.dialog.hide()
        # Reenter the create state
        self.fsm.request("create")
        # set the focus to the username entry
        self.setFocus(self.nameEntry)

    def __handlePasswordAck(self):
        self.dialog.hide()
        # Reenter the create state
        self.fsm.request("create")
        # set the focus to the password entry
        self.setFocus(self.passwordEntry)

    def enterWaitForLoginResponse(self):
        self.cr.handler = self.handleWaitForLoginResponse
        self.cr.userName = self.userName
        self.cr.password = self.password

        try:
            data = {
                }

            # include the referrer code if there is one
            referrer = launcher.getReferrerCode()
            if referrer is not None:
                data['referrer'] = referrer

            error=self.loginInterface.createAccount(self.userName,
                                                    self.password,
                                                    data)
        except TTAccount.TTAccountException as e:
            # show the error message, and back out of account creation
            error = str(e)
            self.notify.info(error)
            self.dialog.setMessage(
                error + OTPLocalizer.CreateAccountScreenConnectionErrorSuffix)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent,
                            self.__handleConnectionErrorAck)
            return

        if error:
            self.notify.info(error)
            self.dialog.setMessage(error)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent,
                            self.__handleBadAccountAck)
        else:
            self.cr.logAccountInfo()
            self.loginInterface.sendLoginMsg()
            self.waitForDatabaseTimeout(
                requestName='CreateAccountWaitForLoginResponse')

    def exitWaitForLoginResponse(self):
        self.cleanupWaitingForDatabase()
        self.cr.handler = None

    def handleWaitForLoginResponse(self, msgType, di):
        if msgType == CLIENT_LOGIN_2_RESP:
            self.handleLoginResponseMsg2(di)
        elif msgType == CLIENT_LOGIN_RESP:
            self.handleLoginResponseMsg(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.cr.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.cr.handleServerDown(di)
        else:
            self.cr.handleMessageType(msgType, di)

    def handleLoginResponseMsg2(self, di):
        # Get the return code
        returnCode = di.getUint8()
        self.notify.info("Login response return code: " + str(returnCode))
        if returnCode == 0:
            # Here's what is in the rest of the datagram.  But, we don't use it:
            # commentString = di.getString()
            # nameString = di.getString()
            # chat = di.getUint8()
            #  These are vestigial.
            # sec = di.getUint32()
            # usec = di.getUint32()
            self.__handleLoginSuccess()
        else:
            # if the return code is bad, go to reject mode
            errorString = di.getString()
            self.notify.warning(errorString)
            messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def __handleLoginSuccess(self):
        self.notify.info("Logged in with username: %s" % (self.userName))
        launcher.setGoUserName(self.userName)
        launcher.setLastLogin(self.userName)
        launcher.setUserLoggedIn()
        messenger.send(self.doneEvent, [{'mode': 'success'}])

    def handleLoginResponseMsg(self, di):
        # Get the return code
        returnCode = di.getUint8()
        self.notify.info("Login response return code: " + str(returnCode))
        if returnCode == 0:
            # if the return code is good, record the account code
            # and request the avatar list
            accountCode = di.getUint32()
            commentString = di.getString()
            # These are vestigial.
            sec = di.getUint32()
            usec = di.getUint32()

            self.__handleLoginSuccess()

        elif returnCode == 12:
            self.notify.info("Bad password")
            self.dialog.setMessage(OTPLocalizer.CreateAccountScreenUserNameTaken)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleBadPasswordAck)

        elif returnCode == 14:
            self.notify.info("Bad word in user name")
            self.dialog.setMessage(OTPLocalizer.CreateAccountScreenInvalidUserName)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleBadWordInUserName)

        elif returnCode == 129:
            self.notify.info("Username not found")
            self.dialog.setMessage(OTPLocalizer.CreateAccountScreenUserNameNotFound)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleBadAccountAck)

        else:
            # if the return code is bad, go to reject mode
            accountCode = di.getUint32()
            errorString = di.getString()
            self.notify.warning(errorString)
            messenger.send(self.doneEvent, [{'mode': 'reject'}])

    def __handleConnectionErrorAck(self):
        self.dialog.hide()
        messenger.send(self.doneEvent, [{'mode': 'failure'}])

    def __handleBadPasswordAck(self):
        self.dialog.hide()
        self.fsm.request("create")

    def __handleBadAccountAck(self):
        self.dialog.hide()
        self.fsm.request("create")

    def __handleBadWordInUserName(self):
        # clear out the username field for them
        self.userName = ""
        self.nameEntry.set("")
        self.dialog.hide()
        self.fsm.request("create")