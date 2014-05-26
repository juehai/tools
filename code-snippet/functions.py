#!/usr/bin/env python2.7


def chunklist(target, num):
    def _chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
    return list(_chunks(target, num))

