include(RezBuild)


file(GLOB_RECURSE py_files python/*.py tests/*.py)

rez_install_python(
  py
  FILES ${py_files}
  DESTINATION .
  LOCAL_SYMLINK
)

