import re
import zipfile
import shutil
import copy
from pathlib import Path
from typing import Optional
from lxml import etree


class TemplateEngine:
    NSMAP = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    def __init__(self, template_path: str):
        self._template_path = Path(template_path)
        self._tmp_path = None

    def detect_placeholders(self) -> list[str]:
        placeholders = set()
        with zipfile.ZipFile(str(self._template_path), 'r') as z:
            doc_xml = z.read('word/document.xml').decode('utf-8')
            for m in re.finditer(r'\{([^}]+)\}', doc_xml):
                inner = m.group(1).strip()
                if re.match(r'^[A-F0-9-]{20,}$', inner):
                    continue
                if inner.startswith('#'):
                    continue
                placeholders.add(inner)
        return sorted(placeholders, key=str.lower)

    def generate(self, output_path: str, context: dict):
        shutil.copy2(str(self._template_path), output_path)

        with zipfile.ZipFile(output_path, 'r') as z:
            doc_xml = z.read('word/document.xml')
            tree = etree.fromstring(doc_xml)

        # Resolve nested placeholders first
        resolved_context = self._resolve_nested(context)

        # Replace all placeholders in XML
        xml_str = etree.tostring(tree, encoding='unicode')
        for key, value in resolved_context.items():
            placeholder = '{' + key + '}'
            xml_str = xml_str.replace(placeholder, str(value))

        # Handle nested patterns like {ketua_komisi_A} after resolution
        for key, value in resolved_context.items():
            # Second pass: handle any remaining brace patterns
            pass

        # Also replace placeholders with / character
        # These are stored differently - need exact match
        for key, value in resolved_context.items():
            if '/' in key:
                placeholder = '{' + key + '}'
                xml_str = xml_str.replace(placeholder, str(value))

        # Write back
        new_xml = etree.fromstring(xml_str.encode('utf-8'))
        new_xml_str = etree.tostring(new_xml, xml_declaration=True, encoding='UTF-8', standalone=True)

        import tempfile
        import os
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(output_path, 'r') as zin:
                with zipfile.ZipFile(os.path.join(tmpdir, 'out.docx'), 'w') as zout:
                    for item in zin.infolist():
                        if item.filename == 'word/document.xml':
                            zout.writestr(item, new_xml_str)
                        else:
                            zout.writestr(item, zin.read(item.filename))

            shutil.move(os.path.join(tmpdir, 'out.docx'), output_path)

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

    def duplicate_participant_rows(self, output_path: str, participants: list[dict]):
        pass  # Will be implemented in Phase 5

    def cleanup(self):
        if self._tmp_path and self._tmp_path.exists():
            self._tmp_path.unlink()
