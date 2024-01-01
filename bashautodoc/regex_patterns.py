import logging
import re

LOG = logging.getLogger(__name__)

mdlink_patt = re.compile(r"\[([*a-zA-Z0-9-_]*)\]\(([#A-Za-z/-0-9_.]*)\)")

### Matches myst --> md patterns

# 3 part match with an *optional capturing group* in angle brackets. i,e. {ref}`here<add_screenshot>`
anchorstart_patt = re.compile(r"({ref})`([a-zA-Z0-9-. _]*)(:?<[a-zA-Z_]*>)?`")
anchorend_patt = re.compile(r"^(\([a-z.A-Z0-9-_]*\)=)$")
hxhash_patt = re.compile(r"^([#]* )([a-zA-Z0-9-_. ]*)$")


admon_patt_single_line = re.compile(
    r":::{(admonition|attention|caution|danger|error|hint|important|note|tip|warning|)}([a-z A-Z0-9!?.,;_]*):::"
)

admon_patt_multiline_start = re.compile(
    r":::{(admonition|attention|caution|danger|error|hint|important|note|tip|warning|)"
)
