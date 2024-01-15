"""
This module contains the Launcher class which is used to generate a
MkDocs site. It is the main entry point for the code in this repo.
"""

import sentry_sdk
import yaml

from eyes3scribe.config import Config
from eyes3scribe.gen_mkdocs_nav_bar import GenMkdocsNavBar
from eyes3scribe.setup_docs_project import SetupDocsProject

sentry_sdk.init(
    dsn="https://4b9aa1ef8464e2e3522cc9dc3d4b5a19@o4506486318563328.ingest.sentry.io/4506486328655872",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    enable_tracing=True,
)

import argparse
import logging
import os
import sys

# TODO: sort out import Dotmap
from dotmap import DotMap
from rich import print as rprint

from eyes3scribe.gen_handwritten_docs import GenHandwrittenDocs
from eyes3scribe.helpo.coloured_log_formatter import ColouredLogFormatter
from eyes3scribe.helpo.hfile import write_dict_2yaml_file
from eyes3scribe.shell_src_preprocessor import ShellSrcPreProcessor

LOG = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(ColouredLogFormatter())

LOG.addHandler(ch)

# 1. copy bash src files to a temp directory
# 2. copy custom css assets to appropriate place
# 3. create mkdocs.yml file
# 4. find (filter appropriate markdown files)
# 5. add to mkdocs.yml file
# 6. subprocess mkdocs build


class Launcher:
    """
    The Launcher class takes a site configuration name and an optional
    debug flag as input. It provides methods to set up the docs project,
    process shell files, and create the MkDocs site.
    """

    def __init__(self, site_confname, build_serve, check_singlefile, debug=False):
        """
        Initialize the Launcher class.

        Args:
            site_confname (str): The name of the site configuration.
            build_serve (bool): Whether to build and serve the local MkDocs site.
            check_singlefile (str): The path of a single shell source file to debug.
            debug (bool, optional): If True, debug information will be printed. Defaults to False.
        """
        # self.site_confname = site_confname
        self.build_serve = build_serve
        self.check_singlefile = check_singlefile
        self.debug = debug

        self.cnf = Config(site_confname)

        rprint("conf: ", self.cnf)

        self.yaml_dict = {}
        for key, value in self.cnf.items():
            if key in self.cnf.eyes3scribe_keys:
                rprint("opassing key", key)
                pass
            else:
                if isinstance(value, DotMap):
                    self.yaml_dict[key] = value.toDict()
                else:
                    self.yaml_dict[key] = value

        rprint("self.yaml_dict", self.yaml_dict)
        # sys.exit(42)

    def main(self):
        """
        Main routine for setting up the docs project, processing shell files, and creating the MkDocs site.
        """

        ### Setup project & get file paths
        setup_docs_project = SetupDocsProject(
            cnf=self.cnf, check_singlefile=self.check_singlefile
        )
        rpaths = setup_docs_project.main()

        clean_hwdocs_rpaths = rpaths["clean_hwdocs_rpaths"]  # ????
        clean_srcfiles_rpaths = rpaths["clean_srcfiles_rpaths"]

        ### Process shell source files
        shell_src_preprocessor = ShellSrcPreProcessor(
            self.cnf,
            clean_srcfiles_rpaths,
            self.cnf.project_docs_dir,
            debug=self.debug,
        )
        catname_2mdfile_dict = shell_src_preprocessor.run()

        ###########################self.mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict)

        ### Generate Handwritten Docs
        gen_handwritten_docs = GenHandwrittenDocs(cnf=self.cnf)
        navbar_cleaned_dict = gen_handwritten_docs.gen_handwritten_docs()
        rprint("navbar_cleaned_dict", navbar_cleaned_dict)

        ###################################################################
        ### Generate MkDocs yaml
        navdict = GenMkdocsNavBar(
            cnf=self.cnf,
            catname_2mdfile_dict=catname_2mdfile_dict,
            navbar_cleaned_dict=navbar_cleaned_dict,
        )
        self.yaml_dict["nav"] = navdict["nav"]
        LOG.info("Writing mkdocs config yaml")
        LOG.debug("self.yaml_dict: %s", yaml.safe_dump(self.yaml_dict))

        write_dict_2yaml_file(
            filename=f"{self.cnf.project_reldir}/mkdocs.yml",
            yaml_dict=self.yaml_dict,
        )

        ### Build and serve local docs site
        if self.build_serve:
            LOG.warning("Building and serving local docs site")
            os.chdir(self.cnf.project_reldir)
            # TODO: use subprocess
            os.system("mkdocs build")
            os.system("mkdocs serve")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gen-Bash-MkDoc",
        usage="python launcher.py --site-confname config/bashrc_stablecaps.yaml",
    )

    parser.add_argument(
        "-s",
        "--site-confname",
        dest="site_confname",
        help="Location of Site conf in yaml format",
        type=str,
        default=None,
        required=True,
    )

    parser.add_argument(
        "-b",
        "---build-serve",
        dest="build_serve",
        help="Build & Serve local mkdocs site after generating docs site",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--check-singlefile",
        dest="check_singlefile",
        help="Pass the path of a single shell src file to debug",
        type=str,
        default=None,
        required=False,
    )

    parser.add_argument(
        "-d", "--debug", dest="debug", help="Turn debug logging on", action="store_true"
    )

    args = parser.parse_args()
    launcher = Launcher(
        site_confname=args.site_confname,
        build_serve=args.build_serve,
        check_singlefile=args.check_singlefile,
        debug=args.debug,
    )
    launcher.main()

    LOG.info("Program Finished")
