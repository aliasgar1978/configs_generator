

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

