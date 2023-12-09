import logging
from dataclasses import dataclass

from bashautodoc.helpo.hfile import mkdir_if_notexists
from bashautodoc.helpo.hstrops import does_string_contain_pattern, str_multi_replace

LOG = logging.getLogger(__name__)


# TODO: enable slots=True
# @dataclass(slots=True)
@dataclass()
class FileDataHolder:
    infile_relpath: str = None
    infile_path_split: list[str] = None
    infile_filename: str = None
    indir_relpath: str = None
    #
    category_names: list[str] = None
    glob_patterns: list[str] = None
    replace_str: str = None
    #
    # outdir_relpath: str = None
    out_filename: str = None
    outfile_relpath: str = None
    outfile_catname: str = None
    undef_category_dir: str = None


class FilepathDatahandler:
    def __new__(
        cls,
        infile_relpath: str,
        glob_patterns: list[str],
        replace_str: str,
        category_names: list[str],
        undef_category_dir: str,
        is_undef: bool = False,
    ):
        # https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
        cls.dh = FileDataHolder()
        #
        cls.dh.infile_relpath = infile_relpath
        cls.dh.infile_path_split = infile_relpath.split("/")
        cls.dh.infile_filename = cls.dh.infile_path_split.pop()
        cls.dh.indir_relpath = "/".join(cls.dh.infile_path_split)
        #
        cls.dh.glob_patterns = glob_patterns
        cls.dh.replace_str = replace_str

        ###
        cls.dh.category_names = category_names
        cls.dh.undef_category_dir = undef_category_dir
        cls.is_undef = is_undef
        return cls.main()

    @classmethod
    def get_out_filename(cls):
        cls.dh.out_filename = str_multi_replace(
            input_str=cls.dh.infile_filename,
            rm_patt_list=cls.dh.glob_patterns,
            replace_str=cls.dh.replace_str,
        )

    @classmethod
    def get_categorydir_and_outfilepath(cls):
        ### If no functions or aliases, then send to undef so user can fix

        if cls.is_undef:
            return ("undef", f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}")

        for catname in cls.dh.category_names:
            if catname in cls.dh.infile_path_split:
                catdir_relpath = f"{cls.dh.indir_relpath}/{catname}"
                mkdir_if_notexists(target=catdir_relpath)
                outfile_relpath = f"{catdir_relpath}/{cls.dh.out_filename}"
                LOG.debug("outfile_relpath: %s", outfile_relpath)

                return (catname, outfile_relpath)

        undef_outfile_relpath = f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}"
        return ("undef", undef_outfile_relpath)

    @classmethod
    def main(cls):
        cls.get_out_filename()

        # LOG.debug("infile_relpath: %s", cls.dh.infile_relpath)
        # LOG.debug("infile_path_split: %s", cls.dh.infile_path_split)
        # LOG.debug(
        #     "infile_filename: %s",
        #     cls.dh.infile_filename,
        # )
        # #
        # LOG.debug("glob_patterns: %s", cls.dh.glob_patterns)
        # LOG.debug("replace_str: %s", cls.dh.replace_str)
        # #
        # LOG.debug("outdir_relpath: %s", cls.dh.outdir_relpath)
        # LOG.debug("out_filename: %s", cls.dh.out_filename)
        # LOG.debug("undef_category_dir: %s", cls.dh.undef_category_dir)

        #############################################
        (
            cls.dh.outfile_catname,
            cls.dh.outfile_relpath,
        ) = cls.get_categorydir_and_outfilepath()

        LOG.debug("catname: %s", cls.dh.outfile_catname)
        LOG.debug("outfile_relpath: %s", cls.dh.outfile_relpath)

        return cls.dh
