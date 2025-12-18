"""Utils package."""
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    get_current_user,
    get_current_active_user,
)
from app.utils.docx_utils import (
    create_document,
    set_document_margins,
    add_styled_paragraph,
    add_heading,
    add_table_with_data,
    add_bullet_list,
    add_numbered_list,
    add_signature_block,
    save_document,
)
from app.utils.legal_refs import (
    CODE_TRAVAIL,
    get_code_article,
    format_legal_reference,
    get_all_nao_articles,
)
from app.utils.validators import (
    validate_email,
    validate_password_strength,
    validate_hex_color,
    validate_siret,
)

__all__ = [
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "get_current_active_user",
    "create_document",
    "set_document_margins",
    "add_styled_paragraph",
    "add_heading",
    "add_table_with_data",
    "add_bullet_list",
    "add_numbered_list",
    "add_signature_block",
    "save_document",
    "CODE_TRAVAIL",
    "get_code_article",
    "format_legal_reference",
    "get_all_nao_articles",
    "validate_email",
    "validate_password_strength",
    "validate_hex_color",
    "validate_siret",
]
