# Website

To build all, `uv run quarto render`. To locally show latest content without a full rebuild, it's `uv run quarto preview`. To publish, `uv run quarto publish`.

To convert images to webp, use `brew install webp` and then `cwebp input.png -o output.webp` on the command line. Can use `-resize <w> <h>` to get smaller / less big file.

To convert heic to jpg, use `magick IMG_7981.heic -quality 100% japanese_edition.jpg`
