import re
import zipfile
import shutil
import os
import tempfile
import copy
from pathlib import Path
from lxml import etree


class TemplateEngine:
    NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    XML_NS = 'http://www.w3.org/XML/1998/namespace'

    def __init__(self, template_path: str):
        self._template_path = Path(template_path)

    def _extract_placeholders(self, text: str) -> list[str]:
        placeholders = set()
        i = 0
        while i < len(text):
            if text[i] == '{':
                depth = 1
                j = i + 1
                while j < len(text) and depth > 0:
                    if text[j] == '{':
                        depth += 1
                    elif text[j] == '}':
                        depth -= 1
                    j += 1
                if depth == 0:
                    placeholders.add(text[i + 1:j - 1])
                i = j
            else:
                i += 1
        return sorted(placeholders, key=str.lower)

    def detect_placeholders(self) -> list[str]:
        with zipfile.ZipFile(str(self._template_path), 'r') as z:
            doc_xml = z.read('word/document.xml')
        tree = etree.fromstring(doc_xml)
        self._merge_cross_run_placeholders(tree)
        full = ''.join(t.text or '' for t in tree.iter(f'{{{self.NS}}}t'))
        return self._extract_placeholders(full)

    def generate(self, output_path: str, context: dict):
        shutil.copy2(str(self._template_path), output_path)

        with zipfile.ZipFile(output_path, 'r') as z:
            doc_xml = z.read('word/document.xml')
        tree = etree.fromstring(doc_xml)

        resolved = self._resolve_nested(context)
        self._merge_cross_run_placeholders(tree)
        self._replace_placeholders(tree, resolved)
        self._expand_text_elements(tree)
        self._ensure_preserve_whitespace(tree)

        xml_bytes = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = os.path.join(tmpdir, 'out.docx')
            with zipfile.ZipFile(output_path, 'r') as zin:
                with zipfile.ZipFile(tmp_path, 'w') as zout:
                    for item in zin.infolist():
                        if item.filename == 'word/document.xml':
                            zout.writestr(item, xml_bytes)
                        else:
                            zout.writestr(item, zin.read(item.filename))
            shutil.move(tmp_path, output_path)

        return output_path

    def _resolve_nested(self, context: dict) -> dict:
        result = dict(context)
        changed = True
        max_iter = 10
        while changed and max_iter > 0:
            changed = False
            max_iter -= 1
            new_result = dict(result)
            for key, value in result.items():
                if isinstance(value, str) and '{' in value:
                    for k2, v2 in result.items():
                        placeholder = '{' + k2 + '}'
                        if placeholder in value:
                            new_result[key] = value.replace(placeholder, str(v2))
                            changed = True
                            value = new_result[key]
            result = new_result
        return result

    def _merge_cross_run_placeholders(self, tree):
        ns = f'{{{self.NS}}}'
        for p in tree.findall(f'.//{ns}p'):
            t_elements = p.findall(f'.//{ns}t')
            if len(t_elements) <= 1:
                continue

            positions = []
            offset = 0
            for t in t_elements:
                text_len = len(t.text or '')
                positions.append((t, offset, offset + text_len, t.getparent()))
                offset += text_len

            full_text = ''.join(t.text or '' for t in t_elements)
            if '{' not in full_text:
                continue

            spans = []
            i = 0
            while i < len(full_text):
                if full_text[i] == '{':
                    depth = 1
                    j = i + 1
                    while j < len(full_text) and depth > 0:
                        if full_text[j] == '{':
                            depth += 1
                        elif full_text[j] == '}':
                            depth -= 1
                        j += 1
                    if depth == 0:
                        spans.append((i, j))
                    i = j
                else:
                    i += 1

            if not spans:
                continue

            for span_start, span_end in spans:
                intersecting = []
                for t, t_start, t_end, run in positions:
                    if t_start < span_end and t_end > span_start:
                        intersecting.append((t, run))

                valid = [(t, run) for t, run in intersecting if t.getparent() is not None]
                if len(valid) <= 1:
                    continue

                first_t, first_run = valid[0]
                merged_text = ''.join(t.text or '' for t, _ in valid)
                first_t.text = merged_text

                for t, _ in valid[1:]:
                    t_parent = t.getparent()
                    if t_parent is not None:
                        t_parent.remove(t)
                        content_tags = {f'{ns}t', f'{ns}tab', f'{ns}br', f'{ns}drawing', f'{ns}pict'}
                        if not any(child.tag in content_tags for child in t_parent):
                            p.remove(t_parent)

                if first_run.find(f'{ns}rPr') is None:
                    for _, run in valid[1:]:
                        if run.getparent() is not None:
                            rpr = run.find(f'{ns}rPr')
                            if rpr is not None:
                                first_run.insert(0, copy.deepcopy(rpr))
                                break

                t_elements = p.findall(f'.//{ns}t')
                positions = []
                offset = 0
                for t in t_elements:
                    text_len = len(t.text or '')
                    positions.append((t, offset, offset + text_len, t.getparent()))
                    offset += text_len

    def _replace_placeholders(self, tree, resolved: dict):
        ns = f'{{{self.NS}}}'
        pattern = re.compile(r'\{([^{}]+)\}')
        max_iter = 10
        for _ in range(max_iter):
            changed = False
            for t in tree.iter(f'{ns}t'):
                if not t.text:
                    continue
                new_text = pattern.sub(lambda m: str(resolved.get(m.group(1), m.group(0))), t.text)
                if new_text != t.text:
                    t.text = new_text
                    changed = True
            if not changed:
                break

    def _build_run_lines(self, paragraph, run, rpr, text, ns, xml_ns):
        lines = text.split('\n')
        line_tokens = []
        for line in lines:
            tokens = []
            parts = line.split('\t')
            for j, part in enumerate(parts):
                if j > 0:
                    tokens.append(('tab', None))
                if part:
                    tokens.append(('text', part))
            line_tokens.append(tokens)

        runs_to_insert = []
        for i, tokens in enumerate(line_tokens):
            if i > 0:
                br_run = etree.Element(f'{ns}r')
                br_run.append(copy.deepcopy(rpr) if rpr is not None else etree.Element(f'{ns}rPr'))
                etree.SubElement(br_run, f'{ns}br')
                runs_to_insert.append(br_run)
            if not tokens and i > 0:
                continue
            crun = etree.Element(f'{ns}r')
            crun.append(copy.deepcopy(rpr) if rpr is not None else etree.Element(f'{ns}rPr'))
            for tok_type, tok_val in tokens:
                if tok_type == 'text':
                    el = etree.SubElement(crun, f'{ns}t')
                    el.set(f'{xml_ns}space', 'preserve')
                    if tok_val:
                        el.text = tok_val
                elif tok_type == 'tab':
                    etree.SubElement(crun, f'{ns}tab')
            runs_to_insert.append(crun)

        idx = list(paragraph).index(run)
        paragraph.remove(run)
        for j, re in enumerate(runs_to_insert):
            paragraph.insert(idx + j, re)

    def _expand_text_elements(self, tree):
        ns = f'{{{self.NS}}}'
        xml_ns = f'{{{self.XML_NS}}}'
        runs = list(tree.iter(f'{ns}r'))
        for run in runs:
            if run.getparent() is None:
                continue
            t_elements = list(run.iter(f'{ns}t'))
            full_text = ''.join(t.text or '' for t in t_elements)
            if '\t' not in full_text and '\n' not in full_text:
                continue

            rpr = run.find(f'{ns}rPr')
            p = run.getparent()
            parent = p.getparent()

            if '\n\n' in full_text:
                blocks = full_text.split('\n\n')
            else:
                blocks = [full_text]

            self._build_run_lines(p, run, rpr, blocks[0].rstrip('\n'), ns, xml_ns)

            if len(blocks) > 1:
                insert_idx = list(parent).index(p) + 1
                for block in blocks[1:]:
                    block = block.rstrip('\n')
                    if not block:
                        continue
                    sep = etree.Element(f'{ns}p')
                    parent.insert(insert_idx, sep)
                    insert_idx += 1

                    new_p = etree.Element(f'{ns}p')
                    ppr = p.find(f'{ns}pPr')
                    if ppr is not None:
                        new_p.insert(0, copy.deepcopy(ppr))
                    parent.insert(insert_idx, new_p)
                    insert_idx += 1

                    new_run = etree.SubElement(new_p, f'{ns}r')
                    if rpr is not None:
                        new_run.insert(0, copy.deepcopy(rpr))
                    self._build_run_lines(new_p, new_run, rpr, block, ns, xml_ns)

    def _ensure_preserve_whitespace(self, tree):
        xml_ns = f'{{{self.XML_NS}}}'
        for t in tree.iter(f'{{{self.NS}}}t'):
            if t.text and t.text != t.text.strip():
                t.set(f'{xml_ns}space', 'preserve')
