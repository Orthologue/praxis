# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Invoice:
    """
    Representation of a financial transaction between two entities
    """


    # public data
    tid = None
    start = None
    finish = None
    receipt = None

    subtotal = 0
    total = 0
    tendered = 0
    change = 0

    void = False
    training = False

    terminal = None
    cashier = None
    customer = None

    transactions = None
    returns = None
    corrections = None
    prompts = None

    tenders = None
    discounts = None
    taxes = None
    refunds = None
    cards = None
    history = None


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize
        self.transactions = []
        self.returns = []
        self.corrections = []
        self.prompts = []
        self.tenders = []
        self.discounts = []
        self.refunds = []
        self.taxes = []
        self.cards = []
        self.history = []
        # all done
        return


    # debugging support
    def dump(self, channel, indent=''):
        # inject
        channel.line('{}invoice {.tid}'.format(indent, self))

        # if the invoice were voided
        if self.void:
            # tell me
            channel.line('{}     status: VOID'.format(indent))
        # if this is a training mode transaction
        if self.training:
            # tell me
            channel.line('{}       mode: TRAINING'.format(indent))

        # dump the rest of the meta-data
        channel.line('{}      start: {.start}'.format(indent, self))
        channel.line('{}     finish: {.finish}'.format(indent, self))
        channel.line('{}    cashier: {.cashier}'.format(indent, self))
        channel.line('{}   terminal: {.terminal}'.format(indent, self))
        channel.line('{}   customer: {.customer}'.format(indent, self))

        # flush
        channel.log()
        # all done
        return


# end of file
