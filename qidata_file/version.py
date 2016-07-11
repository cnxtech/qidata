# -*- coding: utf-8 -*-

# Standard library
from argparse import Action
# qidata
from qidata import VERSION

# ──────────────────────
# Package version action

class VersionAction(Action):
	def __init__(self, option_strings, dest, nargs, **kwargs):
		super(VersionAction, self).__init__(option_strings, dest, nargs=0, **kwargs)
	def __call__(self, parser, namespace, values, option_string):
		version_string = VERSION + "\n"
		parser.exit(message=version_string)

# ────────────────
# File versionning

QIDATA_NS = [u"http://aldebaran.com/xmp/1",
                u"http://softbank-robotics.com/qidata/1"]

def identifyFileAnnotationVersion(file_path):
    """
    Identify the annotated file version by looking its inner structure

    @file_path : File to analyze
    @return    : Version number or None if file is not annotated
    """
    version = None
    from qidata_objects import DataObjectTypes
    from xmp.xmp import XMPFile

    # Open file through XMP
    xmp_file = XMPFile(file_path)
    try:
        xmp_file.open()
    except RuntimeError, e:
        # File is not XMP and cannot be opened, it cannot be an annotated file
        return None
    else:
        xmp_file.close()

    with XMPFile(file_path) as xmp_file:
        # Retrieve its namespaces
        namespaces = xmp_file.metadata.namespaces

        for ns in namespaces:
            if ns.uid in QIDATA_NS:
                if QIDATA_NS[0] == ns.uid:
                    # Version is 1 or 2 (old namespace is used)
                    # Mark as version 2 and check if version is actually 1
                    version = 2

                    if(xmp_file.metadata[QIDATA_NS[0]].children):
                        for child in xmp_file.metadata[QIDATA_NS[0]].children.keys():
                            if child.split(":")[-1] in DataObjectTypes:
                                # First child level is QiDataObject type, not annotator ID
                                # => Version 1
                                version = 1
                                break
                    else:
                        # If there is no children, then there is no data
                        # This should usually not happen, but file can be considered as version 2
                        pass
                elif QIDATA_NS[1] == ns.uid:
                    # Version is 3
                    version = 3
                else:
                    # File is not annotated
                    version = None
                break
    return version
