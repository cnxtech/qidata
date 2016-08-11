# -*- coding: utf-8 -*-

from xmp.xmp import XMPFile, registerNamespace
from qidata.metadata_objects import makeMetadataObject
from qidata.files import getFileDataType
from qidata.types import CheckCompatibility, DataType
from qidata.qidataobject import QiDataObject
import __builtin__

QIDATA_NS=u"http://softbank-robotics.com/qidata/1"
registerNamespace(QIDATA_NS, "qidata")

def open(file_path, mode="r"):
    """
    Open a QiDataFile using the QiDataFile() type, returns a QiDataFile object.
    This is the preferred way to open a QiDatafile.
    """
    return QiDataFile(file_path, mode)

class QiDataFile(QiDataObject):

    # ───────────
    # Constructor

    def __init__(self, file_path, mode = "r"):
        """
        Create and open a QiDataFile.
        QiDataFile wraps the xmp library specifically to store QiDataObjects under the
        QiData namespace.

        :param file_path: path to the file to open (str)
        :param mode: opening mode, "r" for reading, "w" for writing (str)

        .. warnings:: The mode behavior is different from the regular Python file mode.
                      The file is NEVER created if it does not exist
        """

        self._type = getFileDataType(file_path)
        self.xmp_file = XMPFile(file_path, rw=(mode=="w"))
        self._raw_data = self._read_file_raw_data()
        self._annotations = None
        self.is_closed = True
        self.open()

    # ──────────
    # Properties

    @property
    def raw_data(self):
        """
        Object's raw data
        """
        return self._raw_data

    @property
    def metadata(self):
        """
        Return metadata content in the form of a dict containing MetadataObjects or built-in types.
        """
        return self._annotations

    @property
    def type(self):
        """
        Specify the type of data in the file (qidata.files.DataType)
        """
        return self._type

    @property
    def closed(self):
        """
        True if the file is closed
        """
        return self.is_closed

    @property
    def mode(self):
        """
        Specify the file mode

        "r" => read-only mode
        "w" => read/write mode
        """
        return "w" if self.xmp_file.rw else "r"

    @property
    def path(self):
        """
        Give the file path
        """
        return self.xmp_file.file_path

    @property
    def raw_metadata(self):
        """
        Return metadata content in raw form
        """
        return self.xmp_file.metadata[QIDATA_NS]

    @property
    def annotators(self):
        """
        Return the list of annotators for this file
        """
        out = []
        if self.raw_metadata.children:
            for qualifiedAnnotatorID in self.raw_metadata.children.keys():
                out.append(qualifiedAnnotatorID.split(":")[1])
        return out

    # ──────────
    # Public API

    def open(self):
        """
        Open the file
        """
        self.xmp_file.__enter__()
        self.is_closed = False
        self.load()
        return self

    def close(self):
        """
        Close the file
        """
        self.xmp_file.__exit__(None, None, None)
        self.is_closed = True

    def save(self):
        """
        Save changes made to annotations
        """
        for key in self.raw_metadata.children:
            self.raw_metadata.pop(key)
        for (annotation_maker, annotations) in self._annotations.iteritems():
            for (annotationClassName, typed_annotations) in annotations.iteritems():
                self.raw_metadata[annotation_maker] = dict()
                self.raw_metadata[annotation_maker][annotationClassName] = []
                for annotation in typed_annotations:
                    tmp_dict = dict(info=annotation[0].toDict())
                    if annotation[1] is not None:
                        tmp_dict["location"]=annotation[1]
                    tmp_dict["info"]["version"] = annotation[0].version
                    self.raw_metadata[annotation_maker].__getattr__(annotationClassName).append(tmp_dict)

    def load(self):
        """
        Load metadata from XMPFile into local `annotations` property
        """
        from collections import OrderedDict
        self._annotations = OrderedDict()
        if self.raw_metadata.children:
            data = self.raw_metadata.value
            self._removePrefix(data)
            for annotatorID in data.keys():
                self._annotations[annotatorID] = dict()
                for metadata_type in CheckCompatibility.getCompatibleMetadataTypes(self.type):
                    self._annotations[annotatorID][str(metadata_type)] = []
                    try:
                        print data[annotatorID]
                        for annotation in data[annotatorID][str(metadata_type)]:
                            obj = makeMetadataObject(str(metadata_type), annotation["info"])
                            if annotation.has_key("location"):
                                loc = annotation["location"]
                                self._unicodeListToBuiltInList(loc)
                                self._annotations[annotatorID][str(metadata_type)].append([obj, loc])
                            else:
                                self._annotations[annotatorID][str(metadata_type)].append([obj, None])

                    except KeyError, e:
                        # metadata_type does not exist in file => it's ok
                        pass

    # ───────────
    # Private API

    def _unicodeListToBuiltInList(self, list_to_convert):
        """
        Convert a list containing unicode values into a list of built-in types

        :param list_to_convert: list of unicode elements to convert (can be nested)

        :Example:

        >>> _unicodeListToBuiltInList(["1"])
        [1]
        >>> _unicodeListToBuiltInList(["1.0", "1"])
        [1.0, 1]
        >>> _unicodeListToBuiltInList(["a",["1","2.0"]])
        ["a", [1, 2.0]]
        """
        if type(list_to_convert) != list:
            raise TypeError("_unicodeListToBuiltInList can only hande lists")
        for i in range(0,len(list_to_convert)):
            if type(list_to_convert[i]) == list:
                self._unicodeListToBuiltInList(list_to_convert[i])
            elif type(list_to_convert[i]) in [unicode, str]:
                list_to_convert[i] = self._unicodeToBuiltInType(list_to_convert[i])

    def _unicodeToBuiltInType(self, input_to_convert):
        """
        Convert a string into a string, a float or an int depending on the string

        :param input_to_convert: unicode or string element to convert

        :Example:

        >>> _unicodeToBuiltInType("1")
        1
        >>> _unicodeToBuiltInType("1.0")
        1.0
        >>> _unicodeToBuiltInType("a")
        'a'
        """
        if type(input_to_convert) not in [str, unicode]:
            raise TypeError("Only unicode or string can be converted")

        try:
            output=int(input_to_convert)
            return output
        except ValueError, e:
            # input cannot be converted to int
            pass
        try:
            output=float(input_to_convert)
            return output
        except ValueError, e:
            # input cannot be converted to float
            pass

        # Input could not be converted so it's probably a string, return it as is.
        return input_to_convert

    def _removePrefix(self, data):
        """
        Removes prefix parts of keys imported from XMP files.

        This function is recursive
        """
        from collections import OrderedDict
        if isinstance(data, OrderedDict):
            keys = data.keys()
            for key in data.keys():
                self._removePrefix(data[key])
                data[key.split(":")[-1]] = data.pop(key)
        elif isinstance(data, list):
            for element in data:
                self._removePrefix(element)

    def _read_file_raw_data(self):
        if self._type == DataType.IMAGE:
            with __builtin__.open(self.path, "r") as tmp:
                return tmp.read()

    # ───────────────
    # Context Manager

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.xmp_file.__exit__(type, value, traceback)
        self.is_closed = True
