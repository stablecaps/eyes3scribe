import logging
from dataclasses import dataclass

from bashautodoc.helpo.hfile import mkdir_if_notexists
from bashautodoc.helpo.hstrops import does_string_contain_pattern, str_multi_replace

LOG = logging.getLogger(__name__)


# TODO: enable slots=True
# @dataclass(slots=True)
@dataclass()
class FileDataHolder:
    infile_rpath: str = None
    infile_path_split: list[str] = None
    infile_filename: str = None
    indir_rpath: str = None
    #
    category_names: list[str] = None
    glob_patterns: list[str] = None
    replace_str: str = None
    #
    # outdir_rpath: str = None
    out_filename: str = None
    outfile_rpath: str = None
    outfile_catname: str = None
    undef_category_dir: str = None


class FilepathDatahandler:
    def __new__(
        cls,
        infile_rpath: str,
        glob_patterns: list[str],
        replace_str: str,
        category_names: list[str],
        undef_category_dir: str,
        is_undef: bool = False,
        leave_original_dir_structure: bool = False,
    ):
        # https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
        cls.dh = FileDataHolder()
        #
        cls.dh.infile_rpath = infile_rpath
        cls.dh.infile_path_split = infile_rpath.split("/")
        cls.dh.infile_filename = cls.dh.infile_path_split.pop()
        cls.dh.indir_rpath = "/".join(cls.dh.infile_path_split)
        #
        cls.dh.glob_patterns = glob_patterns
        cls.dh.replace_str = replace_str

        ###
        cls.dh.category_names = category_names
        cls.dh.undef_category_dir = undef_category_dir
        cls.is_undef = is_undef
        cls.leave_original_dir_structure = leave_original_dir_structure
        return cls.main()

    @classmethod
    def _get_outfilename(cls):
        cls.dh.out_filename = str_multi_replace(
            input_str=cls.dh.infile_filename,
            rm_patt_list=cls.dh.glob_patterns,
            replace_str=cls.dh.replace_str,
        )

    @classmethod
    def _get_categorydir_and_outfilepath(cls):
        ### If no functions or aliases, then send to undef so user can fix

        if cls.is_undef:
            return ("undef", f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}")

        for catname in cls.dh.category_names:
            if catname in cls.dh.infile_path_split:
                catdir_rpath = f"{cls.dh.indir_rpath}/{catname}"
                mkdir_if_notexists(target=catdir_rpath)
                outfile_rpath = f"{catdir_rpath}/{cls.dh.out_filename}"
                LOG.debug("outfile_rpath: %s", outfile_rpath)

                return (catname, outfile_rpath)

        undef_outfile_rpath = f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}"
        return ("undef", undef_outfile_rpath)

    @classmethod
    def _get_original_outfilepath(cls):
        # if cls.is_undef:
        #     return ("undef", f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}")

        # for catname in cls.dh.category_names:
        #     if catname in cls.dh.infile_path_split:
        # catdir_rpath = f"{cls.dh.indir_rpath}/{catname}"
        # mkdir_if_notexists(target=catdir_rpath)
        outfile_rpath = cls.dh.infile_rpath
        LOG.debug("outfile_rpath: %s", outfile_rpath)

        return ("docshw", outfile_rpath)

        # undef_outfile_rpath = f"{cls.dh.undef_category_dir}/{cls.dh.out_filename}"
        # return ("undef", undef_outfile_rpath)

    @classmethod
    def main(cls):
        cls._get_outfilename()

        # LOG.debug("infile_rpath: %s", cls.dh.infile_rpath)
        # LOG.debug("infile_path_split: %s", cls.dh.infile_path_split)
        # LOG.debug(
        #     "infile_filename: %s",
        #     cls.dh.infile_filename,
        # )
        # #
        # LOG.debug("glob_patterns: %s", cls.dh.glob_patterns)
        # LOG.debug("replace_str: %s", cls.dh.replace_str)
        # #
        # LOG.debug("outdir_rpath: %s", cls.dh.outdir_rpath)
        # LOG.debug("out_filename: %s", cls.dh.out_filename)
        # LOG.debug("undef_category_dir: %s", cls.dh.undef_category_dir)

        #############################################

        if FilepathDatahandler.leave_original_dir_structure:
            (
                cls.dh.outfile_catname,
                cls.dh.outfile_rpath,
            ) = cls._get_original_outfilepath()
        else:
            (
                cls.dh.outfile_catname,
                cls.dh.outfile_rpath,
            ) = cls._get_categorydir_and_outfilepath()

        LOG.debug("catname: %s", cls.dh.outfile_catname)
        LOG.debug("outfile_rpath: %s", cls.dh.outfile_rpath)

        return cls.dh
