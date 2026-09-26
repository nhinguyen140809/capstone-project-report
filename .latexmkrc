# latexmk config shared by scripts/build.py, VS Code (LaTeX Workshop) and CI.
# Change build behavior here instead of passing options in each place.

@default_files = ('main.tex');

$pdf_mode = 1;         # pdflatex, since the template uses vntex with T5 font encoding
$bibtex_use = 2;       # biblatex + biber; `latexmk -c` also removes the .bbl file
$out_dir = '.';        # main.pdf goes to the repo root
$aux_dir = 'build';    # intermediate files (.aux, .log, .bbl, ...) go to build/
$warnings_as_errors = 1;  # unresolved \ref/\cite, duplicate labels, missing glyphs: the PDF is still produced but the build fails
$emulate_aux = 1;      # TeX Live's pdflatex has no -aux-directory, so let latexmk separate intermediate files itself

set_tex_cmds('-interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S');

# \include{chapters/x/main} writes its .aux file to build/chapters/x/, but TeX Live's pdflatex
# does not create missing subdirectories. Mirror the source directory tree inside build/ up front.
use File::Find;
use File::Path qw(make_path);
find(
    {
        wanted => sub {
            if (-d $_ && $File::Find::name =~ m{^\./(build|\.[^/]+)$}) {
                $File::Find::prune = 1;
                return;
            }
            make_path("$aux_dir/$File::Find::name") if -d $_;
        },
        no_chdir => 1,
    },
    '.'
);
