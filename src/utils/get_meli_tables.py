from playwright.sync_api import Page

def get_meli_tables(page: Page):
    classes = {
        "andes": 'andes-table',
        "striped": 'ui-vpp-striped-specs__table'
    }

    tables = []

    try:
        andes_tables = page.query_selector_all(f'.{classes["andes"]}')
        tables.extend(andes_tables)
    except Exception:
        pass

    try:
        striped_tables = page.query_selector_all(f'.{classes["striped"]}')
        tables.extend(striped_tables)
    except Exception:
        pass

    return tables