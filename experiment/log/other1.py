import logging

module_logger = logging.getLogger("example.other1")

#----------------------------------------------------------------------
def add(x, y):
    """"""
    logger = logging.getLogger("example.other1.add")
    logger.info("added %s and %s to get %s" % (x, y, x+y))
    return x+y
