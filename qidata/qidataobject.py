# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard libraries
from collections import OrderedDict
import copy
import abc

# Local modules
from qidata import MetadataType
from qidata.metadata_objects import MetadataObject
from textualize import textualize_metadata

class ReadOnlyException(Exception):pass

def throwIfReadOnly(f):
	def wraps(*args):
		self=args[0]
		if self.read_only:
			raise ReadOnlyException("This method cannot be used in read-only")
		return f(*args)

	# Keep the function docstring
	wraps.__doc__ = f.__doc__
	return wraps

class QiDataObject(object):
	"""
	Interface class representing a generic "data" element.

	Data can be any piece of raw data (image, audio, text, whatever)
	carrying annotations.
	"""
	__metaclass__ = abc.ABCMeta

	# ──────────
	# Properties

	@abc.abstractproperty
	def raw_data(self):
		"""
		Object's raw data
		"""

	@property
	def annotations(self):
		"""
		Return metadata content in the form of a ``collections.OrderedDict`` containing
		metadata object instances or built-in types.
		The returned object is a copy of the real metadata, therefore modifying it has no
		impact on the underlying object.

		:return: Copy of the registered annotations
		:rtype: ``collections.OrderedDict``
		"""
		if not hasattr(self, "_annotations"):
			self._annotations = OrderedDict()
		return copy.deepcopy(self._annotations)

	@property
	def annotators(self):
		"""
		Return the list of annotators for this object
		"""
		return self.annotations.keys()

	@abc.abstractproperty
	def read_only(self):
		"""
		States if the object is protected against modification

		:return: True if the object is read-only (cannot be modified)
		"""

	# ──────────
	# Public API

	@throwIfReadOnly
	def addAnnotation(self, annotator, annotation, location=None):
		"""
		Adds an annotation

		:param annotator: The identifier of the annotations' maker
		:type annotator: str
		:param annotation: The annotation to add
		:type annotation: ``qidata.metadata_objects.MetadataObject``
		:param location: The area of the annotation

		:raises: TypeError if ``annotation`` is not a
		         ``qidata.metadata_objects.MetadataObject``
		:raises: Exception if ``_isLocationValid(location)`` returns False

		.. note::
			The location might have no sense, depending on your data, and it is
			also really dependant of the type of data you annotate. Which is
			why the location must be validated by the ``_isLocationValid``
			method, which must be overriden by any subclass.
		"""
		# Make sure self._annotations exists
		assert(hasattr(self, "_annotations") or self.annotations is not None)

		# Check given annotation is a proper metadata objects
		annotation_name = type(annotation).__name__
		try:
			MetadataType[annotation_name]
			if not isinstance(annotation, MetadataObject):
				raise KeyError
		except KeyError:
			raise TypeError("annotation is not a proper MetadataObject")

		# Check if location is valid
		if not self._isLocationValid(location):
			raise Exception("Location %s is invalid"%str(location))

		# Create a new annotator if unknown
		if not self._annotations.has_key(annotator):
			self._annotations[annotator] = dict()

		# Add annotation
		if not self._annotations[annotator].has_key(annotation_name):
			self._annotations[annotator][annotation_name] = list()

		self._annotations[annotator][annotation_name].append(
		  [annotation, location]
		)

	def getAnnotations(self, annotator, annotation_type=None):
		"""
		Return the list of annotations made by ``annotator`` of type
		``annotation_type``
		"""
		# Make sure self._annotations exists
		assert(hasattr(self, "_annotations") or self.annotations is not None)

		if not self._annotations.has_key(annotator):
			return []

		if annotation_type is not None:
			# Check given type
			try:
				annotation_type = MetadataType[annotation_type]
			except KeyError:
				try:
					annotation_type = MetadataType(annotation_type)
				except ValueError:
					raise TypeError(
					          "%s is not a valid MetadataType"%annotation_type
					      )

			if not self._annotations[annotator].has_key(str(annotation_type)):
				return []
			else:
				out = self._annotations[annotator][str(annotation_type)]
		else:
			out = [a for b in self._annotations[annotator].values() for a in b]

		if self.read_only:
			return copy.deepcopy(out)
		else:
			return out

	@throwIfReadOnly
	def removeAnnotation(self, annotator, annotation, location=None):
		"""
		Removes an annotation

		:param annotator: The identifier of the annotation to remove
		:type annotator: str
		:param annotation: The annotation to remove
		:type annotation: ``qidata.metadata_objects.MetadataObject``
		:param location: The area of the annotation

		:raises: TypeError if ``annotation`` is not a
		         ``qidata.metadata_objects.MetadataObject``
		:raises: ValueError if there is no annotation recorded for ``annotator``
		:raises: ValueError if nothing is found to be removed

		.. note::
			To be removed, an annotation must match with ``annotation`` and its
			location must also match ``location``.
			The only exception is when ``location`` is None, and matching
			annotations are found, but they all have a location different than
			``None``. In that case, the first matching annotation is removed.
			If several annotations match with ``annotation`` and ``location``,
			then the first one only is removed.
		"""
		# Make sure self._annotations exists
		assert(hasattr(self, "_annotations") or self.annotations is not None)

		# Check given annotation is a proper metadata objects
		annotation_name = type(annotation).__name__
		try:
			MetadataType[annotation_name]
			if not isinstance(annotation, MetadataObject):
				raise KeyError
		except KeyError:
			raise TypeError("annotation is not a proper MetadataObject")

		# Do we know the annotator ?
		if not self._annotations.has_key(annotator):
			raise ValueError("Annotator %s is unknown"%annotation_name)

		# Search for a matching annotation, remove it if one is found
		# Otherwise, raise
		if self._annotations[annotator].has_key(annotation_name):
			first_matching = None
			for annot, loc in self._annotations[annotator][annotation_name]:
				if annot == annotation and loc == location:
					self._annotations[annotator][annotation_name].remove(
					    [annot, loc]
					)
					if len(self._annotations[annotator][annotation_name])==0:
						self._annotations[annotator].pop(annotation_name)
						if len(self._annotations[annotator])==0:
							self._annotations.pop(annotator)
					return
				elif annot == annotation\
				  and first_matching is None\
				  and location is None:
					first_matching = [annot, loc]
			if first_matching is not None:
				self._annotations[annotator][annotation_name].remove(first_matching)
				if len(self._annotations[annotator][annotation_name])==0:
					self._annotations[annotator].pop(annotation_name)
					if len(self._annotations[annotator])==0:
						self._annotations.pop(annotator)
				return

		raise ValueError(
		  "Could not remove annotation %s for %s at location %s"%(
		    str(annotation),
		    str(annotator),
		    str(location)
		  )
		)


	# ───────────
	# Private API

	@abc.abstractmethod
	def _isLocationValid(self, location):
		"""
		Determines if the location given to ``addAnnotation`` is correct.

		:param location: The location to test
		:return: True if location is valid, False otherwise

		.. warning::
			A ``None`` location must always be considered as valid.
		"""

	# ──────────────
	# Textualization

	def __str__(self):
		return unicode(self).encode(encoding="utf-8")

	def __unicode__(self):
		res_str = ""
		for annotator in self.annotators:
			annotator_str = "Annotator: " + unicode(annotator)
			res_str += annotator_str
			res_str += textualize_metadata(self.annotations[annotator])
			res_str += "\n"
		return res_str