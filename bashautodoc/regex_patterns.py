import logging
import re

LOG = logging.getLogger(__name__)

mdlink_patt = re.compile(r"[- ]*\[([*a-zA-Z0-9-_]*)\]\(([A-Za-z/-0-9_.]*)")

# 3 part match with an *optional capturing group* in angle brackets. i,e. {ref}`here<add_screenshot>`
ref_start_patt = re.compile(r"({ref})`([a-zA-Z0-9-. _]*)(:?<[a-zA-Z_]*>)?`")
anchor_end_pattern = re.compile(r"^(\([a-z.A-Z0-9-_]*\)=)$")
hxhash_patt = re.compile(r"^([#]* )([a-zA-Z0-9-_. ]*)$")
