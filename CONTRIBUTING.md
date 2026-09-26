# Quy ước commit

Repo sử dụng [Conventional Commits](https://www.conventionalcommits.org/), với tập `type` và `scope` được điều chỉnh cho việc viết report thay vì phát triển phần mềm. Commit message viết bằng tiếng Anh.

## Định dạng

```text
<type>(<scope>): <subject>

<body>
```

- `type`: bắt buộc, chọn một giá trị trong bảng bên dưới.
- `scope`: không bắt buộc, cho biết phần nào của report bị thay đổi.
- `subject`: mô tả ngắn thay đổi, viết ở thể mệnh lệnh (`add`, `fix`, `update`, không viết `added` hay `adds`), chữ thường ở đầu, không có dấu chấm cuối câu, tổng độ dài dòng đầu không quá 72 ký tự.
- `body`: không bắt buộc, cách dòng đầu một dòng trống, dùng để giải thích lý do thay đổi khi subject chưa đủ rõ. Mỗi dòng không quá 72 ký tự.

## Type

| Type | Dùng khi |
|---|---|
| `content` | Viết mới hoặc chỉnh sửa nội dung report: chapter, section, đoạn văn, bảng, abstract, lời cảm ơn |
| `fix` | Sửa lỗi trong nội dung hoặc lỗi compile: typo, số liệu sai, `\ref`/`\cite` hỏng, lỗi LaTeX |
| `figure` | Thêm hoặc sửa figure trong `figures/`, bao gồm cả file source trong `src/` |
| `ref` | Thêm, sửa hoặc xóa tài liệu tham khảo trong `refs.bib` |
| `style` | Thay đổi hình thức trình bày mà không đổi nội dung: preamble, layout trang, font, định dạng heading, trang bìa |
| `build` | Thay đổi cách build: `.latexmkrc`, `scripts/build.py` |
| `ci` | Thay đổi workflow GitHub Actions |
| `docs` | Thay đổi tài liệu của repo: `README.md`, `CONTRIBUTING.md` (không phải nội dung report) |
| `chore` | Các việc còn lại: `metadata.tex`, `.gitignore`, config editor, dọn file |
| `revert` | Hoàn tác một commit trước đó, subject là tiêu đề của commit bị hoàn tác |

Nếu một commit rơi vào nhiều type, nên tách thành nhiều commit. Trường hợp không tách được, chọn type ứng với thay đổi chính.

## Scope

Scope dùng tên chapter (bỏ phần số thứ tự trong tên folder) hoặc tên một khu vực cố định của repo:

| Scope | Phạm vi |
|---|---|
| `introduction`, `theoretical-background`, `related-work`, ... | Chapter tương ứng trong `chapters/<order>-<name>/` và folder `figures/<name>/` |
| `frontmatter` | Trang bìa, lời cam đoan, lời cảm ơn, abstract, file đính kèm |
| `appendix` | `backmatter/appendix.tex` |
| `metadata` | `metadata.tex` |

Scope có thể bỏ qua khi thay đổi không gắn với một phần cụ thể, ví dụ `ref`, `build`, `ci`, hoặc khi thay đổi trải trên nhiều chapter.

## Ví dụ

```text
content(introduction): add problem statement and research questions
content(related-work): compare role design in MetaGPT and ChatDev
fix(evaluation): correct precision values in table 5.2
fix: resolve broken references after renaming chapter 3 labels
figure(proposed-solution): add requirement elicitation workflow diagram
ref: add ISO/IEC/IEEE 29148 requirements engineering standard
style(frontmatter): align supervisor names on the title page
chore(metadata): set phase 2 and submission date
build: fail the build on undefined citations
ci: attach the PDF to published releases
docs: explain the checkpoint workflow in README
```

Ví dụ commit có body:

```text
content(proposed-solution): replace single-agent baseline with multi-agent setup

The phase 1 feedback asked for a comparison with a multi-agent
baseline, so section 4.2 now describes both setups and 4.3 reports
results for each.
```

## Pull request và checkpoint

- Khi merge pull request bằng **Squash and merge**, title của pull request trở thành commit message trên `main`. Vì vậy title của pull request cũng theo đúng định dạng trên.
- Trước khi tạo checkpoint cho một giai đoạn, cập nhật `\reportphase` và `\reportdate` trong một commit riêng, ví dụ `chore(metadata): set phase 1 and submission date`. Sau đó mới tạo release theo hướng dẫn trong [README](README.md#tạo-checkpoint-cho-từng-giai-đoạn).
