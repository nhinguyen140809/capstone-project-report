# Report

Repo chứa source LaTeX của report capstone project. Mỗi khi branch `main` thay đổi, GitHub Actions compile lại report và cập nhật bản PDF mới nhất tại:

**PDF mới nhất:** https://github.com/nhinguyen140809/capstone-project-report/releases/download/latest/report.pdf

Submission/Release của từng giai đoạn được lưu tại trang [Releases](https://github.com/nhinguyen140809/capstone-project-report/releases), xem thêm mục [Tạo checkpoint cho từng giai đoạn](#tạo-checkpoint-cho-từng-giai-đoạn).

## Cấu trúc repo

```text
.
├── main.tex                  # file gốc, ghép các phần của report theo thứ tự
├── metadata.tex              # tên đề tài, giai đoạn, thông tin người thực hiện, ngày tháng
├── refs.bib                  # tài liệu tham khảo (biblatex + biber, style IEEE)
├── styles/
│   ├── preamble.tex          # khai báo package, layout trang, định dạng heading
│   └── usecase.tex           # environment cho use case detail
├── frontmatter/              # trang bìa, lời cam đoan, lời cảm ơn, tóm tắt
│   └── attachments/          # các file PDF được include nguyên trang (phiếu giao đề tài, trang chữ ký)
├── chapters/
│   ├── 1-introduction/
│   │   ├── main.tex          # \chapter{...} và \input các section của chapter
│   │   ├── motivation.tex
│   │   └── ...
│   ├── 2-theoretical-background/
│   └── ...
├── backmatter/appendix.tex
├── figures/                  # hình minh họa, chia folder theo chapter; file source nằm trong folder src/ của từng chapter
├── scripts/build.py          # script compile
├── .latexmkrc                # cấu hình build dùng chung cho local, VS Code và CI
├── CONTRIBUTING.md           # quy ước commit
└── .github/workflows/build.yml
```

Convention:

- Mỗi chương là một thư mục `chapters/<order>-<name>/`. File `main.tex` của chapter chứa lệnh `\chapter{}` và `\input` các section, mỗi section nằm trong một file riêng.
- Hình minh họa đặt trong `figures/<chapter name>/`. Preamble đã khai báo `\graphicspath{{figures/}}`, vì vậy đường dẫn trong `\includegraphics` chỉ cần tính từ `figures/`.
- Mọi đường dẫn trong `\input` và `\include` đều tính từ thư mục gốc của repo, kể cả khi lệnh nằm trong file của một chapter.
- Tên đề tài, giai đoạn, sinh viên, giảng viên và ngày tháng chỉ được khai báo tại `metadata.tex`. Trang bìa, lời cam đoan và PDF properties đều lấy thông tin từ file này. Chẳng hạn, trước khi nộp giai đoạn 2, chỉ cần sửa `\newcommand{\reportphase}{Phase 2}` và `\reportdate` thay vì tìm và sửa từng vị trí.
- Với hình vẽ bằng công cụ như draw.io hay Excalidraw, cần commit cả file source để có thể chỉnh sửa về sau (xem mục [Figures và file source của diagram](#figures-và-file-source-của-diagram)).
- Commit message theo Conventional Commits với tập `type` và `scope` riêng cho project, xem [CONTRIBUTING.md](CONTRIBUTING.md).

Ví dụ, để thêm chương 6 về evaluation:

```latex
% chapters/6-evaluation/main.tex
\chapter{Evaluation}
\input{chapters/6-evaluation/setup}
\input{chapters/6-evaluation/results}

% chapters/6-evaluation/results.tex
\section{Results}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\linewidth]{evaluation/accuracy.pdf} % file tại figures/evaluation/accuracy.pdf
    \caption{Accuracy theo từng agent}
\end{figure}
```

Sau đó, thêm `\include{chapters/6-evaluation/main}` vào phần Chapters của `main.tex` tại vị trí tương ứng.

### Figures và file source của diagram

Khi compile bằng `pdflatex`, LaTeX chỉ nhận hình ở định dạng PDF, PNG và JPG. Diagram nên được export sang PDF vì đây là định dạng vector, phóng to không bị vỡ. Tuy nhiên, file export không thể chỉnh sửa lại, nên file source của diagram cần được commit kèm theo (nếu có) và đặt trong thư mục `src/` của thư mục hình tương ứng:

```text
figures/evaluation/
├── agent-workflow.pdf          # file export, dùng trong \includegraphics{evaluation/agent-workflow.pdf}
└── src/
    └── agent-workflow.drawio   # file source, mở bằng draw.io để chỉnh sửa, sau đó export ghi đè file PDF
```

Một số lưu ý khi export:

- draw.io: chọn **File > Export as > PDF** và tick **Crop** để PDF vừa khít diagram, không thừa lề trắng.
- Excalidraw: export PNG với tùy chọn **Embed scene**. File PNG này vẫn có thể mở lại bằng Excalidraw để chỉnh sửa, nên không cần lưu file source riêng.
- Không dùng trực tiếp file SVG vì `pdflatex` không đọc được định dạng này. Cần export sang PDF trước.
- Ảnh chụp màn hình không có file source, chỉ cần đặt file PNG trong `figures/<chapter name>/`.

## Install compiler

Report được compile bằng `pdflatex` (do sử dụng `vntex` và font encoding `T5`), phần tài liệu tham khảo dùng `biblatex` + `biber`, và `latexmk` tự động chạy đủ số lượt compile cần thiết. Cần cài đặt:

- Một bản phân phối TeX: MiKTeX hoặc TeX Live. Cả hai đều có sẵn `pdflatex`, `biber` và `latexmk`.
- Perl, vì `latexmk` là một script Perl. TeX Live trên macOS và Linux đã kèm Perl, riêng Windows cần cài thêm.
- Python 3.9 trở lên để chạy `scripts/build.py`.

### Windows

1. Cài đặt [MiKTeX](https://miktex.org/download). Trong quá trình cài, chọn **Install missing packages on-the-fly: Yes** để MiKTeX tự tải các package còn thiếu ở lần build đầu tiên. Nếu đã cài trước đó, bật lại tùy chọn này bằng lệnh:

   ```powershell
   initexmf --set-config-value=[MPM]AutoInstall=1
   ```

   Sau khi cài xong, mở **MiKTeX Console** và chạy **Check for updates** một lần.

2. Cài đặt [Strawberry Perl](https://strawberryperl.com/).

3. Mở một cửa sổ terminal mới để biến môi trường PATH được cập nhật.

Có thể dùng TeX Live thay cho MiKTeX bằng cách cài đặt theo [hướng dẫn của TeX Live](https://tug.org/texlive/windows.html). Bản này đã kèm sẵn Perl.

### macOS

Cài đặt [MacTeX](https://tug.org/mactex/) (bản đầy đủ, dung lượng khoảng 5 GB) hoặc cài qua Homebrew:

```bash
brew install --cask mactex-no-gui
```

### Linux

Trên Ubuntu/Debian, cài đặt các package cần thiết bằng lệnh:

```bash
sudo apt install texlive-latex-extra texlive-lang-other texlive-bibtex-extra texlive-fonts-recommended texlive-science biber latexmk
```

Nếu quá trình build vẫn báo thiếu package, có thể cài `texlive-full` để có đầy đủ mọi package.

### Verify installation

```bash
latexmk -v
perl -v
biber --version
```

Nếu cả ba lệnh đều in ra version thì việc install đã hoàn tất.

## Compile trên máy local

Các lệnh dưới đây chạy từ thư mục gốc của repo. Trên macOS và Linux, thay `python` bằng `python3`.

```bash
python scripts/build.py          # build một lần, tạo main.pdf tại thư mục gốc
python scripts/build.py watch    # tự động build lại mỗi khi lưu file, nhấn Ctrl+C để stop
python scripts/build.py clean    # xóa thư mục build/ và main.pdf
```

File PDF được tạo tại `main.pdf` ở thư mục gốc để dễ tìm, còn các file trung gian trong quá trình compile (`.aux`, `.log`, `.bbl`, ...) nằm trong `build/` để source tree không lẫn các file sinh ra. Cả hai đều đã được đưa vào `.gitignore`.

Khi compile lỗi, script in ra các dòng lỗi kèm tên file và số dòng, ví dụ `chapters/1-introduction/goals.tex:12: Undefined control sequence`. Log đầy đủ nằm tại `build/main.log`.

Build cũng được xem là failed khi có `\ref` hoặc `\cite` không resolve được (hiển thị thành "??" trong PDF), label bị định nghĩa trùng, hoặc ký tự không có trong font. Khi đó PDF vẫn được tạo, nhưng cả script lẫn CI đều báo lỗi để những lỗi này không lọt vào submission. Ví dụ, nếu dùng `\cite{wang2024}` trong khi `refs.bib` không có key `wang2024`, script sẽ in ra `Citation 'wang2024' on page 12 undefined`.

Các option không thuộc script sẽ được chuyển nguyên cho `latexmk`. Ví dụ, để build lại từ đầu dù không có file nào thay đổi:

```bash
python scripts/build.py build -g
```

Lần build đầu tiên trên MiKTeX sẽ mất nhiều thời gian hơn do phải tải package.

### Sử dụng VS Code

Cài đặt extension [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop). File `.vscode/settings.json` đã cấu hình recipe `latexmk (latexmkrc)` và output dir là thư mục gốc của repo. Nhờ đó, mỗi khi lưu file, extension build theo đúng cấu hình của script và hiển thị PDF ở tab bên cạnh.

### Vì sao cấu hình build nằm trong `.latexmkrc`

`latexmk` tự động đọc file `.latexmkrc` trong working directory, vì vậy script, VS Code và CI đều build với cùng một cấu hình: dùng `pdflatex` và `biber`, xuất PDF ra thư mục gốc và đặt file trung gian vào `build/`. Khi cần thay đổi cách build, chỉ cần sửa file này.

Ngoài ra, file này tạo sẵn folder tree bên trong `build/`. Lệnh `\include{chapters/1-introduction/main}` ghi file `.aux` vào `build/chapters/1-introduction/`. `pdflatex` của MiKTeX tự tạo thư mục này, nhưng `pdflatex` của TeX Live (dùng trên CI, macOS và Linux) thì không, dẫn đến lỗi `I can't write on file`. Tương tự, TeX Live không hỗ trợ option `-aux-directory` để tách file trung gian khỏi PDF, nên `.latexmkrc` bật `$emulate_aux`: `latexmk` build toàn bộ vào `build/`, sau đó copy PDF ra thư mục gốc.

## CI/CD

Workflow `.github/workflows/build.yml` compile report bằng TeX Live bản mới nhất trong Docker ([xu-cheng/latex-action](https://github.com/xu-cheng/latex-action)) và dùng chung `.latexmkrc` với môi trường local.

Repo chỉ có một source và build ra một file PDF, trong khi project được nộp theo nhiều giai đoạn. Vì vậy, CI tạo ra ba loại PDF, khác nhau ở commit được build và thời gian lưu trữ:

- **Bản mới nhất của main:** luôn là file PDF của commit mới nhất trên `main` và được ghi đè mỗi khi `main` thay đổi. Dùng để đọc phiên bản hiện tại.
- **Bản checkpoint:** File PDF được chốt tại một thời điểm, chẳng hạn lúc nộp giai đoạn 1. Bản này không bị ghi đè và không hết hạn, kể cả khi giai đoạn 2 tiếp tục được viết trên `main`.
- **Bản xem nhanh:** File PDF của một pull request, một branch hoặc một lần chạy thủ công. Bản này tự động bị xóa sau 7 đến 30 ngày.

| Event | PDF location | Storage duration |
|---|---|---|
| Push hoặc merge vào `main` | `report.pdf` trong prerelease `latest` | Đến lần build `main` tiếp theo |
| Publish một release, ví dụ tag `phase-1` | `report-phase-1.pdf` trong release đó | Vĩnh viễn |
| Mở hoặc cập nhật pull request | Artifact `report-pr<PR number>-<commit>.pdf` | 7 ngày |
| Chạy thủ công bằng **Run workflow** trong tab Actions | Artifact `report-<branch>-<commit>.pdf` | 30 ngày |

Mọi file PDF do CI build đều ghi nguồn build, commit và thời điểm build vào field **Subject** trong PDF properties mà không in lên trang nào. Nhờ đó, ngay cả sau khi đã tải về máy (kể cả `report.pdf` của `latest`), vẫn có thể biết file PDF được build từ đâu bằng cách mở **File > Properties** trong application đọc PDF (trên Chrome và Edge là **Document properties**). Ví dụ:

```text
Subject: main, commit a1b2c3d, build 2026-10-12 08:30 UTC
Subject: phase-1, commit 9f8e7d6, build 2026-11-05 02:14 UTC
Subject: PR 12, commit 4c5d6e7, build 2026-10-20 15:02 UTC
```

File PDF build trên máy local không có field này.

Mỗi lần push vào `main` cũng tạo thêm một artifact, được lưu trong 30 ngày. Link đến mọi file PDF của một lần chạy action đều nằm trong phần summary của lần chạy đó (tab **Actions**, chọn lần chạy tương ứng). Artifact được upload dưới dạng file PDF. Nếu compile lỗi, CI upload thêm artifact `build-log` để tra cứu vị trí lỗi.

### Tải bản PDF mới nhất của main

Mỗi lần build, CI dời tag `latest` sang commit mới nhất của `main` và ghi đè file `report.pdf` trong release này. Có hai cách tải:

- Qua link cố định: `https://github.com/nhinguyen140809/capstone-project-report/releases/download/latest/report.pdf`. Nếu repo ở chế độ private, người tải cần đăng nhập GitHub và có quyền đọc repo.
- Qua GitHub CLI:

  ```bash
  gh release download latest --repo nhinguyen140809/capstone-project-report --pattern report.pdf --clobber
  ```

Commit và thời điểm build của bản hiện tại được ghi trong phần notes của release, hiển thị ngay dưới tên release **Latest build of main** tại trang **Releases** (hoặc xem bằng lệnh `gh release view latest`). Release này được đánh dấu là prerelease để nhãn **Latest** trên trang repo luôn chỉ đến bản nộp chính thức gần nhất.

### Tạo checkpoint cho từng giai đoạn

Mỗi checkpoint là một GitHub Release. Một release gắn với một tag, và tag trỏ đến đúng một commit. Khi release được publish, CI build commit đó và đính kèm file PDF vào release.

Ví dụ, khi nộp giai đoạn 1:

1. Trên trang repo, chọn **Releases** ở cột bên phải, sau đó chọn **Draft a new release**.
2. Tại **Choose a tag**, nhập `phase-1` và chọn **Create new tag: phase-1 on publish**. Để **Target** là `main`, hoặc chọn branch chứa phiên bản cần nộp.
3. Điền title (ví dụ `Giai đoạn 1`) và ghi chú nếu cần, sau đó chọn **Publish release**.
4. Sau vài phút, khi CI chạy xong, release sẽ có thêm file `report-phase-1.pdf` với link cố định:

   ```text
   https://github.com/nhinguyen140809/capstone-project-report/releases/download/phase-1/report-phase-1.pdf
   ```

Sau khi tạo checkpoint, giai đoạn 2 tiếp tục được viết trên `main` mà không ảnh hưởng đến PDF của `phase-1`. Khi nộp giai đoạn 2, lặp lại các bước trên với tag `phase-2`. Tất cả checkpoint đều được liệt kê tại trang **Releases**, người cần xem bản nộp của giai đoạn nào có thể tải trực tiếp tại đây.

Có thể thực hiện thao tác tương tự từ terminal bằng GitHub CLI:

```bash
gh release create phase-1 --target main --title "Giai đoạn 1" --notes "Submission giai đoạn 1"
```

Nếu cần chỉnh sửa bản giai đoạn 1 sau khi đã nộp, không nên sửa release cũ mà nên tạo release mới với tag khác, ví dụ `phase-1-rev2`, để giữ nguyên bản đã nộp. Tên tag không được chứa khoảng trắng, nên dùng kebab-case.

### Xem nhanh PDF của một branch

Cách này không cần tạo release:

1. Vào tab **Actions** và chọn workflow **Build PDF** ở cột bên trái.
2. Chọn **Run workflow**, chọn branch (hoặc tag) tại ô **Use workflow from**, sau đó chọn **Run workflow**.
3. Khi workflow chạy xong, mở lần chạy đó. Link tải PDF nằm trong phần summary và mục **Artifacts** bên dưới.

File PDF này tự động bị xóa sau 30 ngày. Nếu cần lưu trữ lâu dài, hãy tạo checkpoint như hướng dẫn ở mục trên.
