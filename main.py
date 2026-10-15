
import json
import re
import pytesseract
# Tesseract OCR installation path
pytesseract.pytesseract.tesseract_cmd = r"E:\OCR\tesseract.exe"
from pathlib import Path

from docx import Document
import pymupdf as fitz

BASE = Path(__file__).parent
INPUT = BASE / 'input'
OUTPUT = BASE / 'output'
OUTPUT.mkdir(exist_ok=True)
MAX_WORDS = 100


def pdf_text(path):
    pages = []
    with fitz.open(path) as pdf:
        for n, page in enumerate(pdf, 1):
            text = page.get_text(sort=True).strip()
            if not text:
                raise ValueError(f'Page {n} has no selectable text; OCR is required.')
            pages.append({'page': n, 'text': text})
    return pages


def docx_text(path):
    doc = Document(path)
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())


def read_source(path):
    if path.suffix.lower() == '.pdf':
        return '\n'.join(x['text'] for x in pdf_text(path))
    if path.suffix.lower() == '.docx':
        return docx_text(path)
    if path.suffix.lower() in ('.txt', '.md'):
        return path.read_text(encoding='utf-8')
    raise ValueError('Supported files: PDF, DOCX, TXT, MD, PNG/JPG invoices')


def split_long(text, limit=MAX_WORDS):
    """Keep sentences where possible; hard-split oversized sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    result, current = [], []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > limit:
            if current:
                result.append(' '.join(current)); current = []
            result.extend(' '.join(words[i:i+limit]) for i in range(0, len(words), limit))
        elif len(current) + len(words) > limit:
            result.append(' '.join(current)); current = words
        else:
            current.extend(words)
    if current:
        result.append(' '.join(current))
    return [x for x in result if x]


def section_chunks(text):
    """Use headings as section boundaries, then apply size limit."""
    sections, title, body = [], 'Introduction', []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('# ') or (line.endswith(':') and len(line.split()) <= 7):
            if body:
                sections.append((title, ' '.join(body)))
            title, body = line.lstrip('# ').rstrip(':'), []
        else:
            body.append(line)
    if body:
        sections.append((title, ' '.join(body)))
    return [{'section': title, 'text': part} for title, body in sections for part in split_long(body)]


def product_chunks(text):
    # Preserve fenced code blocks as atomic units; split surrounding prose.
    pieces = re.split(r'(```[\s\S]*?```)', text)
    result = []
    for piece in pieces:
        if not piece.strip():
            continue
        if piece.startswith('```'):
            result.append({'section': 'Code block', 'text': piece.strip(), 'oversize': len(piece.split()) > MAX_WORDS})
        else:
            result.extend(section_chunks(piece))
    return result


def troubleshooting_chunks(text):
    # A warning stays with its immediately preceding instruction block.
    blocks = re.split(r'(?=^Issue:)', text, flags=re.MULTILINE)
    result = []
    for block in blocks:
        if block.strip():
            result.append({'section': block.splitlines()[0].strip(), 'text': block.strip()})
    return result


def invoice_ocr(path):
    try:
        import pytesseract
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = (r"E:\OCR\tesseract.exe")
    
    
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError('Install pytesseract and Pillow for invoice OCR') from exc
    if path.suffix.lower() == '.pdf':
        with fitz.open(path) as pdf:
            images = [Image.frombytes('RGB', [p.width, p.height], p.samples)
                      for p in [page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False) for page in pdf]]
    else:
        images = [Image.open(path)]
    text = '\n'.join(pytesseract.image_to_string(im) for im in images)
    if not text.strip():
        raise ValueError('OCR returned no text; manually review invoice.')
    def field(pattern):
        match = re.search(pattern, text, re.I)
        return match.group(1).strip() if match else None
    record = {
        'invoice_number': field(r'Invoice\s*(?:No|Number|#)\s*[:#]?\s*([\w-]+)'),
        'date': field(r'Date\s*:\s*([^\n]+)'),
        'total': field(r'Total\s*:\s*([^\n]+)'),
        'raw_ocr_text': text.strip(),
        'review_required': True  # Demo: verify OCR manually before trusting amounts.
    }
    return [{'section': 'Invoice record', 'text': json.dumps(record, ensure_ascii=False)}]


def process(kind, filename):
    path = INPUT / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    if kind == 'invoice':
        chunks = invoice_ocr(path)
    else:
        text = read_source(path)
        strategies = {'employee': section_chunks, 'product': product_chunks,
                      'troubleshooting': troubleshooting_chunks}
        chunks = strategies[kind](text)
    return [{'chunk_id': f'{kind}_{i:03d}', 'source': filename,
             'document_type': kind, 'section': chunk['section'],
             'text': chunk['text'], 'word_count': len(chunk['text'].split()),
             'needs_review': bool(chunk.get('oversize', False)) or kind == 'invoice'}
            for i, chunk in enumerate(chunks, 1)]


def main():
    jobs = [('employee', 'employee_policy.pdf'),
            ('product', 'product_documentation.md'),
            ('invoice', 'scanned_invoice.png'),
            ('troubleshooting', 'troubleshooting_guide.txt')]
    all_chunks = []
    for kind, filename in jobs:
        try:
            chunks = process(kind, filename)
            all_chunks.extend(chunks)
            print(f'OK {kind}: {len(chunks)} chunks')
        except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
            print(f'SKIP {kind}: {exc}')
    target = OUTPUT / 'chunks.json'
    target.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Saved {len(all_chunks)} chunks to {target}')


if __name__ == '__main__':
    main()
