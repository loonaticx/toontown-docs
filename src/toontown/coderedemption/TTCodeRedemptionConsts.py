from toontown.toonbase.ToontownModules import *

DefaultDbName = 'tt_code_redemption'

RedeemErrors = Enum(
    'Success, CodeDoesntExist, CodeIsInactive, CodeAlreadyRedeemed, AwardCouldntBeGiven, '
    'TooManyAttempts, SystemUnavailable, ')

# for ~code response
RedeemErrorStrings = {
    RedeemErrors.Success: 'Success',
    RedeemErrors.CodeDoesntExist: 'Invalid code',
    #RedeemErrors.CodeIsExpired: 'Code is expired',
    RedeemErrors.CodeIsInactive: 'Code is inactive',
    RedeemErrors.CodeAlreadyRedeemed: 'Code has already been redeemed',
    RedeemErrors.AwardCouldntBeGiven: 'Award could not be given',
    RedeemErrors.TooManyAttempts: 'Too many attempts, code ignored',
    RedeemErrors.SystemUnavailable: 'Code redemption is currently unavailable',
    }

assert len(RedeemErrorStrings) == len(RedeemErrors)

MaxCustomCodeLen = ConfigVariableInt('tt-max-custom-code-len', 16).getValue()
