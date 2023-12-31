import logging
import re

LOG = logging.getLogger(__name__)

mdlink_pattern = re.compile(r"[- ]*\[([*a-zA-Z0-9-_]*)\]\(([A-Za-z/-0-9_.]*)")

# 3 part match with an *optional capturing group* in angle brackets. i,e. {ref}`here<add_screenshot>`
anchorstart_pattern = re.compile(r"({ref})`([a-zA-Z0-9-. _]*)(:?<[a-zA-Z_]*>)?`")
anchorend_pattern = re.compile(r"^(\([a-z.A-Z0-9-_]*\)=)$")
hxhash_pattern = re.compile(r"^([#]* )([a-zA-Z0-9-_. ]*)$")
