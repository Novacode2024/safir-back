
from deep_translator import GoogleTranslator
from django.core.paginator import Paginator

def translate_text(text: str, target_language: str) -> str:
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        return f"Error: {str(e)}"


def paginate_queryset(queryset, page_number, page_size):
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number)
    return {
        'items': page_obj,
        'page': page_number,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count,
    }