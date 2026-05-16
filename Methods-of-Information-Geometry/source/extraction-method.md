# DjVu Extraction Method

No `djvutxt`, `djvused`, `djvudump`, or `ddjvu` executable was available on the worker PATH. The course therefore vendors `vendor/djvu_text_extractor`, a read-only Rust command that uses `djvu-rs 0.17.0`. It opens the bundled DjVu document, decodes each page text layer from `TXTz` chunks, and writes UTF-8 page text plus a JSON manifest. The extractor does not render, crop, screenshot, or modify the source.

Observed result: 216 physical pages, 216 page text files, no NAVM bookmark entries. Physical page 10 begins printed page 1 of the main matter, matching the table of contents.
