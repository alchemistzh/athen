import logging

#----------------------------------------------------------------------
def add(x, y):
    """"""
    logger = logging.getLogger("other2.add")
    logger.critical("other2.add: added %s and %s to get %s" % (x, y, x+y))
    return x+y
