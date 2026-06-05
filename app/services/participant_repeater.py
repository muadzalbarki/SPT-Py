import copy
import re
from lxml import etree
from pathlib import Path
import zipfile
import shutil
import tempfile


class ParticipantRepeater:
    NSMAP = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }
    W = NSMAP['w']

    def __init__(self, docx_path: str):
        self._path = Path(docx_path)

    def process(self, participants: list[dict]) -> str:
        if len(participants) <= 9:
            return self._truncate_rows(len(participants))
        return self._clone_rows(len(participants))

    def _truncate_rows(self, target_count: int) -> str:
        """Remove participant rows when fewer than 9 selected."""
        if target_count >= 9:
            return str(self._path)

        with zipfile.ZipFile(str(self._path), 'r') as z:
            doc_xml = z.read('word/document.xml')
            tree = etree.fromstring(doc_xml)

        # Find participant table (has rows with {nama} placeholder)
        tables = tree.findall(f'.//{{{self.W}}}tbl')
        target_table = None
        for table in tables:
            rows = table.findall(f'./{{{self.W}}}tr')
            if len(rows) >= 9:
                row_text = self._get_row_text(rows[1])
                if '{nama}' in row_text.lower():
                    target_table = table
                    break

        if target_table is None:
            return str(self._path)

        rows = target_table.findall(f'./{{{self.W}}}tr')
        # First row is header (Kepada:), rows 1-9 are participants
        # Keep header + target_count participants
        header_row = rows[0]
        participant_rows = rows[1:]

        # Remove rows beyond target_count
        for row in participant_rows[target_count:]:
            target_table.remove(row)

        # Renumber remaining
        remaining = participant_rows[:target_count]
        for i, row in enumerate(remaining, 1):
            self._update_numbering(row, i)

        self._write_xml(tree)
        return str(self._path)

    def _clone_rows(self, target_count: int) -> str:
        """Clone participant rows when more than 9 selected."""
        with zipfile.ZipFile(str(self._path), 'r') as z:
            doc_xml = z.read('word/document.xml')
            tree = etree.fromstring(doc_xml)

        tables = tree.findall(f'.//{{{self.W}}}tbl')
        target_table = None
        for table in tables:
            rows = table.findall(f'./{{{self.W}}}tr')
            if len(rows) >= 9:
                row_text = self._get_row_text(rows[1])
                if '{nama}' in row_text.lower():
                    target_table = table
                    break

        if target_table is None:
            return str(self._path)

        rows = target_table.findall(f'./{{{self.W}}}tr')
        header_row = rows[0]
        participant_rows = rows[1:]

        # Clone the last row as template
        template_row = copy.deepcopy(participant_rows[-1])

        # Remove existing participant rows
        for row in participant_rows:
            target_table.remove(row)

        # Add cloned rows
        total = target_count
        for i in range(total):
            new_row = copy.deepcopy(template_row)
            self._update_numbering(new_row, i + 1)
            target_table.append(new_row)

        self._write_xml(tree)
        return str(self._path)

    def _update_numbering(self, row, number: int):
        """Update the numbering paragraph (1., 2., etc.) in a row."""
        paras = row.findall(f'.//{{{self.W}}}p')
        for para in paras:
            texts = para.findall(f'.//{{{self.W}}}t')
            for t in texts:
                if t.text and t.text.strip().endswith('.'):
                    try:
                        old_num = int(t.text.strip().rstrip('.'))
                        t.text = f'{number}.'
                        break
                    except ValueError:
                        continue

    def _get_row_text(self, row) -> str:
        texts = []
        for t in row.iter(f'{{{self.W}}}t'):
            if t.text:
                texts.append(t.text)
        return ' '.join(texts)

    def _write_xml(self, tree):
        new_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_out = Path(tmpdir) / 'out.docx'
            with zipfile.ZipFile(str(self._path), 'r') as zin:
                with zipfile.ZipFile(str(tmp_out), 'w') as zout:
                    for item in zin.infolist():
                        if item.filename == 'word/document.xml':
                            zout.writestr(item, new_xml)
                        else:
                            zout.writestr(item, zin.read(item.filename))
            shutil.move(str(tmp_out), str(self._path))
