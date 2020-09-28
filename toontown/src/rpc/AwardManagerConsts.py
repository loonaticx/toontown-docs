GiveAwardErrors = Enum('Success, WrongGender, NotGiftable, FullMailbox, FullAwardMailbox, AlreadyInMailbox, AlreadyInGiftQueue, '
                       'AlreadyInOrderedQueue, AlreadyInCloset, AlreadyBeingWorn, AlreadyInAwardMailbox, '
                       'AlreadyInThirtyMinuteQueue, AlreadyInMyPhrases, AlreadyKnowDoodleTraining, '
                       'GenericAlreadyHaveError, UnknownError, UnknownToon, '
                       )

GiveAwardErrorStrings = {
    GiveAwardErrors.Success: "success",
    GiveAwardErrors.WrongGender: "wrong gender",
    GiveAwardErrors.NotGiftable: "item is not giftable",
    GiveAwardErrors.FullMailbox: "mailbox is full",
    GiveAwardErrors.FullAwardMailbox: "award mailbox is full",
    GiveAwardErrors.AlreadyInMailbox: "award already in mailbox.",
    GiveAwardErrors.AlreadyInGiftQueue: "award already in gift queue.",
    GiveAwardErrors.AlreadyInOrderedQueue: "award already in ordered queue.",
    GiveAwardErrors.AlreadyInCloset: "award already in closet.",
    GiveAwardErrors.AlreadyBeingWorn: "award already being worn.",
    GiveAwardErrors.AlreadyInAwardMailbox: "award already in award mailbox",
    GiveAwardErrors.AlreadyInThirtyMinuteQueue: "award already in 30 minute queue",
    GiveAwardErrors.AlreadyInMyPhrases: "speed chat award already in my phrases",
    GiveAwardErrors.AlreadyKnowDoodleTraining: "doodle training award already known",
    GiveAwardErrors.GenericAlreadyHaveError: "generic-already-have error",
    GiveAwardErrors.UnknownError: "unknown error",
    GiveAwardErrors.UnknownToon: "toon not in database",
    }

assert len(GiveAwardErrorStrings) == len(GiveAwardErrors)
