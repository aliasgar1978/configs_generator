configuration_generation Usage Guidelines!
============================================


Template Preparation
-----------------------

This is very important step in order to generate the configuration accurately.

Through out the template, we will have many variables which requires to be replaced with necessary values.  Such static one to one variable v/s value mappings we generally provide thru `var` tab of excel database.  There is no constraint on variable naming. Just remember it should match exactly and all match throughout documents will be process and replaced with values.

Apart from static variable/value replacement, we usually have code blocks in the configuration template. Which requires a different kind of treatment.

There are two main types of code blocks.
	
	#. **Conditional Block:** Section which appears in output after successful evaluation of a condition.	
	#. **Repeat Block:** Section which appears repeatatively in to output after successful evaluation of a condition.

#. Conditional Blocks
	
	* Such block usually starts with ``GOAHEAD FOR <conditions>``, and ends with ``GOAHEAD END``.
	* Block start/end string can be modified by providing ``condition_starter``, ``condition_stopper`` arguments while creating ``ConfGen`` object.
	* In case if condition matches more than one record in database, very first matching row will be considered and used.
	* There must be a conditional-block-end correspond to start, otherwise undesired result may produce.
	* Nested conditional blocks are permitted.

#. REPEAT BLOCK

	* Such block usually starts with ``REPEAT EACH <conditions>``, and ends with ``REPEAT STOP``.
	* Block start/end string can be modified by providing ``repeat_starter``, ``repeat_stopper`` arguments while creating ``ConfGen`` object.
	* Each condition matching row from database, will be selected and executed for repetitive config generation.
	* There must be a repeat-block-end correspond to start, otherwise undesired result may produce.
	* Nested repetitive conditional blocks are permitted.

Nesting of *Conditional block*  and *Repetitive block* inside each other permitted as well.



.. note::

	* **<condition>** can be a single match condition or multiple matches ( using condition separators either & or | )
	* Each condition should be defined within it's own bracket ().
	* Each conditions left portion denotes variable to be match in excel fact file, and right portion denotes value to be match with the variable.
	* Conditional operators allowed within a condition are  *%2==*, *%2!=*, *==*, *!=*, *>=*, *<=*, *>*, *<*		
	* **%2==**, **%2!=**  these are useful for matching odd / even number matching
	* String value match should be mentioned with Quote "", : ex: *( LINK_TYPE == "Downlink")*
	* Numeric value match should be mentioned without Qoute : ex: *( VLAN == 100 )*






Database Preparation
-----------------------

This is second very important step, and should be prepared accurately to get the output configuration correct.

.. note::

	``facts_finder`` project can be used to quickly draft the details out of any running device (if already available)


There are two main types of data with which configs_generator interact with. and we need to provide them in two tabs via excel database.
	
	#. **var**: All one to one variables v/s values to be replace in template
	#. **tables**: Rest of other matrix details in table format.

#. **var**

	* There should be a tab named ``var`` in Excel database.
	* There should be two columns named **FIND** and **REPLACE**, for mapping each variable v/s value
	* Column Header can be changed instead of FIND/REPLACE to any other name, but it needs to be declared via ``find_column_name`` and ``replace_column_name`` arguments while creating ConfGen object.
	* All variables defined here under `find_column_name` will get replaced with value mentioned in `replace_column_name` while generating configuration.

#. **tables**

	* There should be a tab named ``tables`` in Excel database
	* There can be any number of columns with any custom column names
	* Data defined here in this tab gets evaluated while executing the condition check during Conditional/Repeat block from template
	* Column header mentioned here in should refer to left portion of condition





Executions
------------------

There are three kinds of exection possible. 

	#. Run thru script.
	#. Passing necessary arguments via command line.
	#. Interactive command line mode.


.. Note::

	* Template file and database file are mandatory fields, rest of others are optional
	* So pre-requisite is: database and configuration template must be ready.


Execute via script : Step by step guide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is how to do via script

Step 1. Import necessary packages::

	import configs_generator as cg


Step 2. Define Inputs::

	db = "data.xlsx"
	template = "template.txt"
	output = "output.txt"


Step 3. Create ConfGen object::

	cfg = cg.ConfGen(
		# ~~~~~~~~~~ Mandatory Arguments ~~~~~~~~~~
		template_file=template,			# template
		db=db,					# database

		# ~~~~~~~~~~ Optional Arguments ~~~~~~~~~~
		output_file=output,			# output filename ( default: output.txt)
		confGen_minimal=False,			# execution of var sheet replacement only.

		find_column_name="FIND",		# FIND/REPLACE column headers from 'var' tab
		replace_column_name="REPLACE",

		condition_starter="GOAHEAD FOR",	# conditional block identifiers
		condition_stopper="GOAHEAD END",
		repeat_starter   ="REPEAT EACH",	# repeat block identifiers
		repeat_stopper   ="REPEAT NEXT",

		nested_section_var_identifier= "PARENT"	# nested section variable identifier string
	)

Step 4. Generate configuration using created object::

	cfg.generate()


script will evaluate the template v/s database for the conditions defined in template and generates new configuarion file.



Execute via argument parsing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is how to do via arguments parsing

To Execute via passing arguments, all inputs should be passed along CLI at once.

Keys available are::

	python -m configs_generator -h
	-------------------------------
	usage: configs_generator [-h] [-i] [-t TEMPLATE_FILE] [-d DB] [-o OUTPUT_FILE]
                         [-m] [-f FIND_COLUMN_NAME] [-r REPLACE_COLUMN_NAME]
                         [-cs CONDITION_STARTER] [-ce CONDITION_STOPPER]
                         [-rs REPEAT_STARTER] [-re REPEAT_STOPPER]
                         [-nv NESTED_SECTION_VAR_IDENTIFIER]

	optional arguments:
	-h, --help            show this help message and exit
	-i, -interactive      run command interactive mode (default: False)
	-t TEMPLATE_FILE, -template TEMPLATE_FILE
	                    Template File (text file) (default: None)
	-d DB, -database DB   Database File (Excel file) (default: None)
	-o OUTPUT_FILE, -output OUTPUT_FILE
	                    output File (text file) (default: None)
	-m, -minimal          execution of var sheet replacement only.( default:
	                    False) (default: False)
	-f FIND_COLUMN_NAME, -find FIND_COLUMN_NAME
	                    FIND column headers from "var" tab: (default: FIND)
	-r REPLACE_COLUMN_NAME, -replace REPLACE_COLUMN_NAME
	                    REPLACe column headers from "var" tab: (default:
	                    REPLACE)
	-cs CONDITION_STARTER, -condition_start CONDITION_STARTER
	                    conditional block start identifier (default: GOAHEAD
	                    FOR)
	-ce CONDITION_STOPPER, -condition_end CONDITION_STOPPER
	                    conditional block end identifier (default: GOAHEAD
	                    END)
	-rs REPEAT_STARTER, -repeat_start REPEAT_STARTER
	                    repeat block start identifier (default: REPEAT EACH)
	-re REPEAT_STOPPER, -repeat_end REPEAT_STOPPER
	                    repeat block end identifier (default: REPEAT STOP)
	-nv NESTED_SECTION_VAR_IDENTIFIER, -nested_var NESTED_SECTION_VAR_IDENTIFIER
	                    nested section variable identifier string (default:
	                    PARENT)


Mandatory Inputs:

	* **-t TEMPLATE_FILE**: Configuration template text file must be passed along with ``-t`` key
	* **-d DB**: Excel Database file must be passed along with ``-d`` key

Optional Inputs:

	* Other optional arguments are required if there is any deviation from standard.


Execute via Interactive CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is how to do via interactive cli mode

To Execute via Interactive CLI, all inputs should be passed along on CLI while asked.

To start the Interactive mode - pass ``-i`` key while running the package.

.. code-block:: shell
	
	C:\..>python -m configs_generator -i
	Enter Template File (text file): template.txt
	Enter Database File (Excel file): data.xlsx
	Enter output File (text file): output.txt
	Do you want to execution of var sheet replacement only [yes/no] .(default: no)
	change FIND column headers on database "var" tab [default: FIND]:
	change REPLACE column headers on database "var" tab [default: REPLACE]:
	change conditional block start identifier in tempalte [default: GOAHEAD FOR]:
	change conditional block end identifier in tempalte [default: GOAHEAD END]:
	change repeat block start identifier in tempalte [default: REPEAT EACH]:
	change repeat block end identifier in tempalte [default: REPEAT STOP]:
	change nested section variable identifier string  in tempalte [default: PARENT]:
	Executing, please wait...



