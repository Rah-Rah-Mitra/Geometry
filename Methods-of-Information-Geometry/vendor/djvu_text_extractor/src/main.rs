use djvu_rs::{DjVuBookmark, Document};
use serde_json::{json, Value};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};

fn bookmark_json(item: &DjVuBookmark) -> Value {
    json!({
        "title": item.title,
        "url": item.url,
        "children": item.children.iter().map(bookmark_json).collect::<Vec<_>>(),
    })
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let input = PathBuf::from(args.next().ok_or("usage: djvu_text_extractor <input.djvu> <output-dir>")?);
    let output = PathBuf::from(args.next().ok_or("usage: djvu_text_extractor <input.djvu> <output-dir>")?);
    fs::create_dir_all(&output)?;

    let doc = Document::open(&input)?;
    let page_count = doc.page_count();
    let mut pages = Vec::with_capacity(page_count);

    for index in 0..page_count {
        let page = doc.page(index)?;
        let text = page.text()?.unwrap_or_default();
        let filename = format!("page-{number:03}.txt", number = index + 1);
        fs::write(output.join(&filename), &text)?;
        pages.push(json!({
            "physical_page": index + 1,
            "text_file": filename,
            "width": page.width(),
            "height": page.height(),
            "dpi": page.dpi(),
            "char_count": text.chars().count(),
            "word_count": text.split_whitespace().count(),
            "first_line": text.lines().find(|line| !line.trim().is_empty()).unwrap_or("").trim(),
        }));
    }

    let bookmarks = match doc.bookmarks() {
        Ok(items) => items.iter().map(bookmark_json).collect::<Vec<_>>(),
        Err(_) => Vec::new(),
    };

    let manifest = json!({
        "source": Path::new(&input).file_name().and_then(|s| s.to_str()).unwrap_or(""),
        "extractor": "vendor/djvu_text_extractor using djvu-rs 0.17.0 read-only text/bookmark APIs",
        "page_count": page_count,
        "pages": pages,
        "bookmarks": bookmarks,
    });
    fs::write(output.join("djvu_text_manifest.json"), serde_json::to_string_pretty(&manifest)?)?;
    Ok(())
}
