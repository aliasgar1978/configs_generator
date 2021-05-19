__doc__ = '''Configuration Generation Tool'''

"""
Mandatory Required modules
==========================
pandas, nettoolkit


usage example:
==============

import configs_generator as cg

# -------- define inputs ----------
db = "data.xlsx"
template = "template.txt"
output = "output.txt"

# -------- ConfGen ----------
cfg = cg.ConfGen(
	# ~~~~~~~~~~ Mandatory Arguments ~~~~~~~~~~
	template_file=template,					# template
	db=db,									# database

	# ~~~~~~~~~~ Optional Arguments ~~~~~~~~~~
	output_file=output,						# output filename ( default: output.txt)
	confGen_minimal=True,					# execution of var sheet replacement only.( default: False)

	find_column_name="FIND_KEYS",			## FIND/REPLACE column headers from 'var' tab
	replace_column_name="REPLACE_VALUES",

	condition_starter="IF",					## conditional block identifiers
	condition_stopper="ENDIF",
	repeat_starter   ="FOR EACH",			## repeat block identifiers
	repeat_stopper   ="NEXT FOR",

	nested_section_var_identifier= "FROM_PARENT"	# nested section variable identifier string
	)

cfg.generate()
"""

__all__ = [
	"ConfGen", "Read", "Section", "Replicate"
	]

__version__ = "0.0.2"

from .confGen import ConfGen, Read, Section, Replicate

