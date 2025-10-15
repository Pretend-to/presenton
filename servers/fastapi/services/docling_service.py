from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    PowerpointFormatOption,
    WordFormatOption,
)
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# 文档处理服务
class DoclingService:
    def __init__(self):
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_ocr = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PPTX, InputFormat.PDF, InputFormat.DOCX],
            format_options={
                InputFormat.DOCX: WordFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.PPTX: PowerpointFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=self.pipeline_options,
                ),
            },
        )

    def parse_to_markdown(self, file_path: str) -> str:
        """
        将文档转换为markdown格式
        """
        result = self.converter.convert(file_path)
        return result.document.export_to_markdown()
