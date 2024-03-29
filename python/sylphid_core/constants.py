# The following two tuples define how environment context maps to context field names.
CTX_ENV_KEY_ORDER = ("CTX_PRJ", "CTX_SEQ", "CTX_SHT", "CTX_TSK")
CTX_DICT_KEY_ORDER = ("project", "sequence", "shot", "task")

# regex to template references in unresolved template strings.
# eg. <root>, <project_name>, <ProjectName>
PATH_REFERENCE_REGEX = r"\<([A-Za-z0-9_]+)\>"
