# gdb-pretty-frame-cpp
Pretty-printer for GDB frames in a backtrace, able to handle nested C++ template arguments. Originally developed for
use debugging [CGAL](http://www.cgal.org/), but is template-library agnostic.

Apache License except for CC-BY-SA files (marked in file)

![Pretty-printer in use with CGAL](https://raw.githubusercontent.com/philtweir/gdb-pretty-frame-cpp/master/doc/inuse.png)

To use without installation, to `.gdbinit` add:
```
add-auto-load-safe-path [PATHTOSOURCE]
python
import sys
sys.path.insert(0, [PATHTOSOURCE])

import framefilter
framefilter.CppFrameFilter()
end
```
where PATHTOSOURCE is the location of this directory.

(based on [GDB STLSupport](https://sourceware.org/gdb/wiki/STLSupport)'s approach)
