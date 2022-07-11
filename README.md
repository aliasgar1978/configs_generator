Configuration Generation Tool

===========================
Mandatory Required packages
===========================
pandas, nettoolkit

For the documentation kindly refer to 
https://configs_generator.readthedocs.io

# ======== OPTION 1 =========== #
import configs_generator as cg

db = "data.xlsx"
template = "template.txt"
output = "output.txt"


cfg = cg.ConfGen(
    template_file=template,
    output_file=output,
    db=db,

    # ~~~~~~~~~~~~ OPTIONAL ARGUMENTS ~~~~~~~~~~~~
    confGen_minimal=True,   # default False

    # ~~~~~~~~~~~~ ADVANCE OPTIONAL ARGUMENTS FOR CUSTOMIZATION ~~~~~~~~~~~~
    find_column_name="FIND",     # default
    replace_column_name="REPLACE",   # default
    condition_starter="GOAHEAD FOR",    # default
    condition_stopper="GOAHEAD END",    # default
    repeat_starter="REPEAT EACH",       # default
    repeat_stopper="REPEAT STOP",       # default
    nested_section_var_identifier="PARENT",     # default
)
cfg.generate()



# ============ OPTION 2 =========== #
usage: configs_generator [-h] [-i] [-t TEMPLATE_FILE] [-d DB] [-o OUTPUT_FILE] [-m] [-f FIND_COLUMN_NAME]
                         [-r REPLACE_COLUMN_NAME] [-cs CONDITION_STARTER] [-ce CONDITION_STOPPER] [-rs REPEAT_STARTER]
                         [-re REPEAT_STOPPER] [-nv NESTED_SECTION_VAR_IDENTIFIER]

Made for Networking Geeks

optional arguments:
  -h, --help            show this help message and exit
  -i, -interactive      run command interactive mode (default: False)
  -t TEMPLATE_FILE, -template TEMPLATE_FILE
                        Template File (text file) (default: None)
  -d DB, -database DB   Database File (Excel file) (default: None)
  -o OUTPUT_FILE, -output OUTPUT_FILE
                        output File (text file) (default: None)
  -m, -minimal          execution of var sheet replacement only.( default: False) (default: False)
  -f FIND_COLUMN_NAME, -find FIND_COLUMN_NAME
                        FIND column headers from "var" tab: (default: FIND)
  -r REPLACE_COLUMN_NAME, -replace REPLACE_COLUMN_NAME
                        REPLACe column headers from "var" tab: (default: REPLACE)
  -cs CONDITION_STARTER, -condition_start CONDITION_STARTER
                        conditional block start identifier (default: GOAHEAD FOR)
  -ce CONDITION_STOPPER, -condition_end CONDITION_STOPPER
                        conditional block end identifier (default: GOAHEAD END)
  -rs REPEAT_STARTER, -repeat_start REPEAT_STARTER
                        repeat block start identifier (default: REPEAT EACH)
  -re REPEAT_STOPPER, -repeat_end REPEAT_STOPPER
                        repeat block end identifier (default: REPEAT STOP)
  -nv NESTED_SECTION_VAR_IDENTIFIER, -nested_var NESTED_SECTION_VAR_IDENTIFIER
                        nested section variable identifier string (default: PARENT)

And that's how you'd use the tool