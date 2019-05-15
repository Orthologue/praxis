# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import datetime, re
# support
import praxis


# declaration
class Transactions:
    """
    Extracts transaction details from the CATAPULT transaction journal report in CSV format
    are lists of clock-in/clock-out pairs of timestamps
    """


    # exceptions
    from ..exceptions import ParsingError
    # types
    from .. import model


    # interface
    def parse(self, stream, invoices=None, errors=None, warnings=None, **kwds):
        """
        Extract transactions from the given {stream}

        The additional {kwds} are passed to the CSV reader without any further processing
        """
        # get the csv package
        import csv
        # make a reader
        reader = csv.reader(stream, **kwds)
        # reset the pile of errors and warnings
        errors = [] if errors is None else errors
        warnings = [] if warnings is None else warnings
        # the pile of discrepancies
        discrepancies = []
        # extract invoices
        for invoice in self.retrieveInvoices(records=reader, errors=errors, warnings=warnings):
            # add them to the pile
            invoices[invoice.tid] = invoice

        # all done
        return


    # implementation details
    def retrieveInvoices(self, records, errors, warnings, **kwds):
        """
        Consume all {records} pertaining to a single invoice
        """
        # get my scanner
        scanner = self.SCANNER
        # the pile of amount discrepancies
        discrepancies = []
        # the current invoice
        invoice = None
        # and it's number
        cid = None

        # start processing records
        for record in records:
            # get the invoice number from the record
            tid = record[self.OFFSET_INVOICE]
            # if it corresponds to a new invoice
            if tid != cid:
                # and we have an existing one
                if invoice:
                    # close it and send it off
                    yield self.finalizeInvoice(invoice=invoice)
                # record the current invoice id
                cid = tid
                # open a new one
                invoice = self.model.invoice()
                # set its transaction id
                invoice.tid = tid
                # if it's from a training session
                if record[self.OFFSET_MODE].startswith('TRAINING MODE'):
                    # mark it as such
                    invoice.training = True
                # decorate it with the available meta-data
                invoice.receipt = record[self.OFFSET_RECEIPT]
                invoice.terminal = record[self.OFFSET_TERMINAL]
                invoice.cashier = record[self.OFFSET_CASHIER]
                invoice.customer = record[self.OFFSET_CUSTOMER_NUMBER]
                invoice.start = datetime.datetime.strptime(
                    record[self.OFFSET_START], self.TIME_FORMAT)
                invoice.finish = datetime.datetime.strptime(
                    record[self.OFFSET_FINISH], self.TIME_FORMAT)
                # show me
                print(f'invoice {invoice.tid}: cashier: {invoice.cashier}')

            # in any case, this record contains information about this invoice
            item = record[self.OFFSET_ITEMID].strip()
            description = record[self.OFFSET_DESCRIPTION]
            quantity = self.float(record[self.OFFSET_QUANTITY])
            price = self.money(record[self.OFFSET_PRICE])
            charge = self.money(record[self.OFFSET_CHARGE])

            # do not disturb the order of the line item handling without walking through the
            # cases carefully; there are tricky interactions among the fields that must be
            # handled in the correct order; for example, line items don't all have item ids,
            # item removal can have both positive and negative quantities to handle removal of
            # returns, etc.

            # the section below catches all items that have a multiplier on their price,
            # regardless of whether they have item ids or not; this handles correctly the
            # removal of a coupon from the transaction, which leaves behind a line that does
            # not include the coupon id

            # if we have an item count
            if quantity != 0:
                # make a new transaction
                transaction = self.model.transaction()
                # decorate
                transaction.item = item
                transaction.description = description
                transaction.quantity = quantity
                transaction.price = price
                transaction.amount = charge

                # handle item removal with higher priority than the rest: if the description
                # indicates a correction
                if description.startswith('Removed >>'):
                    # quantity can be of either sign; that's how removal of returned items is
                    # handled...
                    # show me
                    # print('    correction: cashier: {.cashier}'.format(invoice))
                    # print('        {}: {}'.format(tid, item))
                    # print('        {}'.format(description))
                    # print('        count: {}, price: {}, charge: {}'.format(
                        # quantity, price, charge))
                    # add it to the corrections
                    invoice.corrections.append(transaction)
                    # and move on
                    continue

                # if this appears to be a return
                if quantity < 0:
                    # show me
                    # print('    return: cashier: {.cashier}'.format(invoice))
                    # print('        {}: {}'.format(tid, item))
                    # print('        {}'.format(description))
                    # print('        count: {}, price: {}, charge: {}'.format(
                        # quantity, price, charge))
                    # add it to the returns
                    invoice.returns.append(transaction)
                    # done with this record
                    continue

                # otherwise, add it to the regular items
                invoice.transactions.append(transaction)
                # and move on
                continue

            # if the quantity zero, this line is metadata:
            #   the item field may be blank
            #   the action is in the same field as the item description
            #   the quantity is always 0
            #   the price is always 0
            #   the charge is negative for discounts and refunds, positive for tenders
            #

            if price:
                # show me
                print('    meta with non-zero price: cashier: {.cashier}'.format(invoice))
                print('        {}: {}'.format(tid, item))
                print('        {}'.format(description))
                print('        count: {}, price: {}, charge: {}'.format(
                    quantity, price, charge))
                # and bail
                raise SystemExit(0)

            # some lines are separators
            if not description:
                # skip
                continue

            # attempt to extract the meaning of this line
            match = scanner.match(description)
            # if we know nothing about it
            if not match:
                # show me
                print(f'invoice {invoice.tid}: no match: {description!r}')
                # and bail
                raise SystemExit(0)

            # find the handler
            handler = getattr(self, match.lastgroup)
            # invoke it
            handler(
                records=records, match=match,
                invoice=invoice, action=description, item=item, amount=charge)
            # and move on
            continue

            # if the charge is positive
            if charge > 0:
                # it is a tender
                tender = self.model.tender()
                tender.mode = description
                tender.amount = charge
                # save it
                invoice.tenders.append(tender)
                # grab the next line
                continue

        # all done
        return


    # invoice life cycle management
    def finalizeInvoice(self, invoice):
        """
        Handler invoked when the parser has determined that all invoice information has been
        extracted
        """
        # check whether the invoice has any tenders
        if not invoice.tenders:
            # and if not, mark it as void; we may get here if catapult is configured to not
            # generate a void marker when the last item is removed from a
            # transaction
            invoice.void = True

        # we may need other invoice post-processing; but for now, that's all
        return invoice


    # type converters
    def float(self, text):
        """
        Parse a floating point number out of text
        """
        # detect the parentheses that indicate a negative number
        if text[0] == '(' and text[-1] == ')':
            # strip and parse
            return -float(''.join(text[1:-1].split(',')))
        # otherwise, let float do its thing
        return float(''.join(text.split(',')))


    def money(self, text):
        """
        Parse a floating point number out of text
        """
        # detect the parentheses that indicate a negative number
        if text[0] == '(' and text[-1] == ')':
            # strip the pair of parentheses and the dollar sign
            return -1*float(''.join(text[2:-1].split(',')))

        # otherwise
        return float(''.join(text[1:].split(',')))


    # invoice meta data handlers
    def cash(self, invoice, amount, action, **kwds):
        # make a new tender
        tender = self.model.cash()
        # decorate it
        tender.amount = amount

        # if this is a correction
        if action.startswith('Removed >>'):
            # add it to the right pile
            invoice.corrections.append(tender)
            # all done
            return

        # if the charge is positive
        if amount > 0:
            # it's a payment
            invoice.tenders.append(tender)
            # show me
            # print('    charge to credit: {}'.format(amount))
            return

        # otherwise, it's a refund
        invoice.refunds.append(tender)
        # show me
        # print('    refund on credit: {}'.format(amount))
        # all done
        return


    def credit(self, invoice, amount, action, **kwds):
        # make a new tender
        tender = self.model.credit()
        # decorate it
        tender.amount = amount

        # if this is a correction
        if action.startswith('Removed >>'):
            # add it to the right pile
            invoice.corrections.append(tender)
            # all done
            return

        # if the charge is positive
        if amount > 0:
            # it's a payment
            invoice.tenders.append(tender)
            # show me
            # print('    charge to credit: {}'.format(amount))
            # all done
            return

        # otherwise, it's a refund
        invoice.refunds.append(tender)
        # show me
        # print('    refund on credit: {}'.format(amount))
        # all done
        return


    def debit(self, invoice, amount, action, **kwds):
        # make a new tender
        tender = self.model.debit()
        # decorate it
        tender.amount = amount

        # if this is a correction
        if action.startswith('Removed >>'):
            # add it to the right pile
            invoice.corrections.append(tender)
            # all done
            return

        # if the charge is positive
        if amount > 0:
            # it's a payment
            invoice.tenders.append(tender)
            # show me
            # print('    charge to debit: {}'.format(amount))
            # all done
            return

        # otherwise, it's a refund
        invoice.refunds.append(tender)
        # show me
        # print('    refund on debit: {}'.format(amount))
        # all done
        return


    def gift(self, invoice, match, item, action, amount, **kwds):
        """
        Payment using a gift card
        """
        # make a new transaction
        card = self.model.giftcard()
        # decorate
        card.account = item
        card.amount = amount

        # if it's a removal of a refund
        if action.startswith('Removed >>'):
            # add it to the corrections
            invoice.corrections.append(card)
            # all done
            return

        # if the charge is positive
        if amount > 0:
            # it's a payment
            invoice.tenders.append(card)
            # show me
            # print('    charge to gift card: {}'.format(amount))
            # all done
            return

        # otherwise, it's a refund
        invoice.refunds.append(card)
        # all done
        return


    def coupon(self, invoice, match, item, action, amount, **kwds):
        """
        Refund monies to the customer
        """
        # make a new transaction
        coupon = self.model.coupon()
        # decorate
        coupon.item = item
        coupon.code = match.group('code')
        coupon.amount = amount

        # if it's a removal of a refund
        if action.startswith('Removed >>'):
            # add it to the corrections
            print('********************************8')
            raise SystemExit(0)
            invoice.corrections.append(coupon)
            return

        # add it to the refunds
        invoice.discounts.append(coupon)
        # all done
        return


    def refund(self, invoice, action, amount, **kwds):
        """
        Refund monies to the customer
        """
        # make a new transaction
        refund = self.model.refund()
        # decorate
        refund.description = action
        refund.amount = amount

        # if it's a removal of a refund
        if action.startswith('Removed >>'):
            # add it to the corrections
            invoice.corrections.append(refund)
        # otherwise
        else:
            # add it to the refunds
            invoice.refunds.append(refund)
        # all done
        return


    def account(self, **kwds):
        """
        Paid on account handling
        """
        # ignore, for now
        return


    def taxes(self, invoice, match, amount, **kwds):
        """
        Add a tax
        """
        # make one
        tax = self.model.tax()
        tax.type = match.group()
        tax.amount = amount
        # save it
        invoice.taxes.append(tax)
        # show me
        # print('    tax: {}'.format(amount))
        # all done
        return


    def discount(self, invoice, action, amount, **kwds):
        """
        Apply a discount
        """
        # make one
        discount = self.model.discount()
        discount.mode = action
        discount.amount = -amount
        # save it
        invoice.discounts.append(discount)
        # show me
        # print('    discount: {.cashier}'.format(invoice))
        # print('        mode: {.mode!r}'.format(discount))
        # print('        amount: {.amount:.2f}'.format(discount))
        # all done
        return


    def void(self, invoice, **kwds):
        """
        Mark the invoice as void
        """
        # do it
        invoice.void = True
        # all done
        return


    # markers
    def subtotal(self, invoice, amount, **kwds):
        """
        The invoice subtotal
        """
        # save the amount
        invoice.subtotal = amount

        # show me
        # go through the line items and add them
        # items = sum(item.amount for item in invoice.transactions)
        # print('        items:       {:8.2f}'.format(items))
        # corrections
        # corrections = sum(item.amount for item in invoice.corrections)
        # print('        corrections: {:8.2f}'.format(corrections))
        # discounts
        # discounts = sum(item.amount for item in invoice.discounts)
        # print('        discounts:   {:8.2f}'.format(discounts))
        # discounts
        # returns = sum(item.amount for item in invoice.returns)
        # print('        returns:     {:8.2f}'.format(returns))
        # add up
        # print('    computed:        {:8.2f}'.format(items+corrections-discounts-returns))
        # print('    subtotal:        {:8.2f}'.format(amount))

        # all done
        return


    def total(self, invoice, amount, **kwds):
        """
        The invoice subtotal
        """
        # save the amount
        invoice.total = amount
        # show me
        # print('    total: {}'.format(amount))
        # all done
        return


    def total(self, invoice, amount, **kwds):
        """
        The invoice subtotal
        """
        # save the amount
        invoice.total = amount
        # show me
        # print('    total: {}'.format(amount))
        # all done
        return


    def tendered(self, invoice, amount, **kwds):
        """
        The total amount tendered before any change is given out
        """
        # save the amount
        invoice.tendered = amount
        # show me
        # print('    tendered: {}'.format(amount))
        # all done
        return


    def change(self, invoice, amount, **kwds):
        """
        The change due
        """
        # save the amount
        invoice.change = amount
        # show me
        # print('    change: {}'.format(amount))
        # all done
        return


    def prompt(self, invoice, match, **kwds):
        """
        Special prompts associated with open keys
        """
        # pull the info
        item, info = match.group(1,2)
        # add it to the pile
        invoice.prompts.append( (item, info) )
        # all done
        return


    def cardinfo(self, records, **kwds):
        """
        A card information section has just begin
        """
        # the next line is a blank
        info = next(records)

        # next, the card type and card holder name
        info = next(records)[self.OFFSET_DESCRIPTION]
	# attempt to match it as a card type
        match = self.CARD_TYPE.match(info)
        # if that fails
        if not match:
            # must be the cardholder's name
            cardholder = info
            # show me
            # print('    cardholder: {!r}'.format(cardholder))
            # the next line has the card type, so get it
            info = next(records)[self.OFFSET_DESCRIPTION]
            # and match it
            match = self.CARD_TYPE.match(info)
        # otherwise
        else:
             # we have no cardholder info
            cardholder = None
        # extract the card type and method
        kind, method = match.groups()
        # if we have a card holder
        if cardholder:
            # make sure the card was swiped
            assert method == 'Swiped'
        # show me
        # print('    kind: {!r}, method: {!r}'.format(kind, method))

        # next, the account number
        info = next(records)[self.OFFSET_DESCRIPTION]
        account = self.CARD_ACCOUNT.match(info).group(1)
        # print('    account: {!r}'.format(account))

        # expiration
        info = next(records)[self.OFFSET_DESCRIPTION]
        expiration = self.CARD_EXPIRATION.match(info).group(1)
        # print('    expiration: {!r}'.format(expiration))

        # the next line is a blank
        info = next(records)

        # charge amount
        info = next(records)[self.OFFSET_DESCRIPTION]
        amount = self.float(self.CARD_AMOUNT.match(info).group(1))
        # print('    amount: {!r}'.format(amount))

        # approvals only for credit cards
        if kind != 'DEBIT':
            # extract the number
            info = next(records)[self.OFFSET_DESCRIPTION]
            print(kind, info)
            approval = self.CARD_APPROVAL.match(info).group(1)
            # print('    approval: {!r}'.format(approval))
        # otherwise
        else:
            # no approval
            approval = None

        # date
        info = next(records)[self.OFFSET_DESCRIPTION]
        date = self.CARD_DATE.match(info).group(1)
        # print('    date: {!r}'.format(date))

        # the next line is a blank
        info = next(records)

        # reference number
        info = next(records)[self.OFFSET_DESCRIPTION]
        reference = self.CARD_REFERENCE.match(info).group(1)
        # print('    reference: {!r}'.format(reference))

        # if the card type is not debit
        if kind != 'DEBIT':
            # the next line is the signature
            next(records)

        # all done
        return


    def giftadd(self, invoice, item, action, amount, **kwds):
        """
        Information about a gift card account
        """
        transaction = self.model.transaction()
        transaction.item = item
        transaction.description = action
        transaction.amount = amount
        # add it to the regular items
        invoice.transactions.append(transaction)

        # all done
        return


    def giftinfo(self, records, **kwds):
        """
        Information about a gift card account
        """
        # balance info
        info = next(records)[self.OFFSET_DESCRIPTION]
        date, balance = self.GIFT_BALANCE.match(info).group(1,2)

        # authorization
        info = next(records)[self.OFFSET_DESCRIPTION]
        authorization = self.GIFT_AUTHORIZATION.match(info).group(1)

        # all done
        return


    def resume(self, match, invoice, **kwds):
        """
        This is invoice was resumed
        """
        # grab the cashier
        cashier = match.group('resumer')
        # and the timestamp
        stamp = match.group('resumed')
        # add them to the history
        invoice.history.append( ('resumed', cashier, stamp) )
        # show me
        # print('    resumed: {} on {}'.format(cashier, stamp))
        # all done
        return


    def suspend(self, match, invoice, **kwds):
        """
        This is invoice was suspended
        """
        # grab the cashier
        cashier = match.group('suspender')
        # and the timestamp
        stamp = match.group('suspended')
        # add them to the history
        invoice.history.append( ('suspended', cashier, stamp) )
        # show me
        # print('    suspended: {} on {}'.format(cashier, stamp))
        # all done
        return


    # constants -- for version 5.2.3 of the CATAPULT TJ-170 report
    OFFSET_START = 8
    OFFSET_FINISH = 10
    OFFSET_INVOICE = 12
    OFFSET_TERMINAL = 14
    OFFSET_CUSTOMER_NUMBER = 16
    OFFSET_RECEIPT = 18
    OFFSET_CUSTOMER_NAME = 20
    OFFSET_CASHIER = 22

    OFFSET_MODE = 23

    OFFSET_ITEMID = 31
    OFFSET_DESCRIPTION = OFFSET_ACTION = 32
    OFFSET_QUANTITY = 33
    OFFSET_PRICE = 34
    OFFSET_CHARGE = 35

    # the timestamp format
    TIME_FORMAT = "%m/%d/%Y %I:%M:%S%p"

    # the meta data scanner
    SCANNER = re.compile('|'.join([
        r'(?P<void>All Void)',

        # special items
        r'(?P<giftadd>Gift Card Add to)$',

        # tenders
        r'(?P<cash>(Removed >> )?Cash)$',
        r'(?P<credit>(Removed >> )?Credit)$',
        r'(?P<debit>(Removed >> )?Debit)$',
        r'(?P<gift>(Removed >> )?GIFTCARD)$',

        # markers
        r'(?P<subtotal>SUBTOTAL)$',
        r'(?P<total>TOTAL)$',
        r'(?P<tendered>TOTAL TENDERED)$',
        r'(?P<change>(Change)|(CHANGE))$',
        r'(?P<cardinfo>--- Card Information ---)$',
        r'(?P<giftinfo>Gift Card Account #{13})$',
        #
        r'(?P<suspend>Suspend by\s+(?P<suspender>.+)\s+@\s+(?P<suspended>.+)\s*)$',
        r'(?P<resume>Resumed by\s+(?P<resumer>.+)\s+@\s+(?P<resumed>.+)\s*)$',
        #
        r'(?P<prompt>Prompt (.+): (.+))$',

        # adjustments
        r'(?P<coupon>Mfr\. Coupon (?P<code>.+))$',
        r'(?P<refund>.* Refund|Softers Deposit Ref)',
        r'(?P<account>.*Paid on Account)$',
        r'(?P<discount>.*Discount)$',
        r'(?P<taxes>.*Tax)$',

        ]))

    CARD_TYPE = re.compile('Card Type:\s+([^\s]+)\s+\((Manual|Swiped)\)')
    CARD_ACCOUNT = re.compile('Account #: (.+)')
    CARD_EXPIRATION = re.compile('Exp Date : (\d\d/?\d\d)')
    CARD_AMOUNT = re.compile('(?:----\s)?Amount: (.+)')
    CARD_APPROVAL = re.compile('Approval #:\s+(.+)')
    CARD_DATE = re.compile('Date: (.+)')
    CARD_REFERENCE = re.compile('Reference #: (.+)')
    CARD_SIGNATURE = re.compile('Signature Captured')

    GIFT_BALANCE = re.compile('Bal @ (.*) = (.*)')
    GIFT_AUTHORIZATION = re.compile('Authorization # (.*)')


# end of file
